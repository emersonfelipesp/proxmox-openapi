# Security Review: proxmox-openapi

**Date:** April 2026
**Status:** Post-hardening review with 10 initial fixes applied

---

## Overview

This document outlines remaining security vulnerabilities and issues identified after implementing 10 initial security improvements. The review covers cryptography, access control, input validation, API design, deployment, and dependency management.

---

## CRITICAL Issues

### 1. SSRF Vulnerability in /codegen/generate Endpoint

**Severity:** CRITICAL
**File:** `proxmox_openapi/routes/codegen.py` (lines 17-58) and `proxmox_openapi/proxmox_codegen/crawler.py` (line 54)
**Status:** ⚠️ NOT FIXED

**Problem:**
The `/codegen/generate` endpoint accepts a user-provided `source_url` parameter that is passed directly to Playwright's `page.goto()` without validation. An attacker can exploit this to:
- Scan internal network ranges (localhost, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- Port scan internal services
- Trigger requests to internal APIs
- Read local file:// URLs if Playwright is misconfigured

**Current Code:**
```python
# crawler.py:54
page.goto(url, wait_until="networkidle")  # url is unvalidated source_url parameter
```

**Attack Vector:**
```
POST /codegen/generate?source_url=http://localhost:8006/api2/json
POST /codegen/generate?source_url=http://169.254.169.254/  # AWS metadata service
POST /codegen/generate?source_url=file:///etc/passwd
```

**Recommended Fix:**
```python
from urllib.parse import urlparse
import ipaddress

def validate_source_url(url: str) -> None:
    """Validate that source_url is safe for external requests."""
    parsed = urlparse(url)

    # Only allow HTTPS for public URLs
    if parsed.scheme not in ("https", "http"):
        raise ValueError(f"Invalid scheme: {parsed.scheme}")

    # Reject private IP ranges
    private_ranges = [
        ipaddress.IPv4Network("10.0.0.0/8"),
        ipaddress.IPv4Network("172.16.0.0/12"),
        ipaddress.IPv4Network("192.168.0.0/16"),
        ipaddress.IPv4Network("127.0.0.0/8"),
        ipaddress.IPv4Network("169.254.0.0/16"),  # Link-local
    ]

    try:
        host_addr = ipaddress.IPv4Address(parsed.hostname)
        for private_range in private_ranges:
            if host_addr in private_range:
                raise ValueError(f"SSRF attempt to private range: {url}")
    except (ipaddress.AddressValueError, TypeError):
        # Not an IPv4 address, check domain allowlist
        if not parsed.hostname or not parsed.hostname.endswith(".proxmox.com"):
            # Allow only official Proxmox domains by default
            pass
```

Then call `validate_source_url(source_url)` at the start of `generate_proxmox_codegen_bundle_async()`.

**Workaround:**
If the codegen endpoint is only used by trusted administrators in development, restrict it to an internal network via nginx/firewall rules.

---

### 2. Missing SSRF Protection on Custom Version Tags

**Severity:** CRITICAL
**File:** `proxmox_openapi/proxmox_codegen/pipeline.py` (lines 71-73)
**Status:** ⚠️ PARTIALLY MITIGATED

**Problem:**
The version tag validation only applies when `version_tag="latest"`. For any custom version tag, the source URL is accepted without validation. This bypasses the existing check.

**Current Code:**
```python
def _validate_source_for_version_tag(source_url: str, version_tag: str) -> None:
    """Reject non-official viewer URLs when using the reserved latest tag."""
    if version_tag != LATEST_VERSION_TAG:
        return  # ← No validation for custom tags!
    if _normalized_viewer_url(source_url) != _normalized_viewer_url(PROXMOX_API_VIEWER_URL):
        raise ValueError("Version tag 'latest' is reserved for official Proxmox API viewer URL.")
```

**Recommended Fix:**
Apply SSRF validation to ALL source URLs regardless of version tag:
```python
def _validate_source_for_version_tag(source_url: str, version_tag: str) -> None:
    """Always validate source URL; enforce latest tag restriction."""
    validate_source_url(source_url)  # Always validate

    if version_tag == LATEST_VERSION_TAG:
        if _normalized_viewer_url(source_url) != _normalized_viewer_url(PROXMOX_API_VIEWER_URL):
            raise ValueError("Version tag 'latest' is reserved for official Proxmox API viewer URL.")
```

---

## HIGH Issues

### 3. Missing CORS Configuration

**Severity:** HIGH
**File:** `proxmox_openapi/main.py`
**Status:** ⚠️ NOT FIXED

**Problem:**
The FastAPI application has no CORS (Cross-Origin Resource Sharing) middleware configured. If deployed behind a reverse proxy without CORS headers, browser-based clients from different origins can access sensitive endpoints.

**Recommended Fix:**
```python
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    # ... existing code ...
    app = FastAPI(...)

    # Add CORS middleware with restrictive defaults
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.environ.get("CORS_ORIGINS", "").split(",") if os.environ.get("CORS_ORIGINS") else [],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        max_age=86400,
    )

    return app
```

And in nginx config or environment, set:
```
CORS_ORIGINS=https://your-domain.com,https://api.your-domain.com
```

---

### 4. Directory Traversal in version_tag Parameter

**Severity:** HIGH
**File:** `proxmox_openapi/proxmox_codegen/pipeline.py` (line 220)
**Status:** ⚠️ PARTIALLY MITIGATED

**Problem:**
The `version_tag` parameter is used to construct file paths without sanitization. While we fixed path traversal in the CLI, the codegen endpoint accepts version tags that could escape the output directory.

**Current Code:**
```python
base = Path(output_dir) / cleaned_version_tag  # cleaned_version_tag could contain ../
```

**Attack:**
```
POST /codegen/generate?version_tag=../../../tmp/pwned
```

**Recommended Fix:**
Add path traversal validation to version_tag:
```python
def _validate_version_tag(tag: str) -> str:
    """Validate version tag doesn't contain path traversal."""
    tag = tag.strip()
    if not tag:
        raise ValueError("version_tag cannot be empty")

    # Reject path traversal patterns
    if ".." in tag or "/" in tag or "\\" in tag:
        raise ValueError("version_tag must not contain path separators or '..'")

    # Only allow alphanumeric, dash, underscore, dot
    import re
    if not re.match(r"^[a-zA-Z0-9._-]+$", tag):
        raise ValueError("version_tag contains invalid characters")

    return tag
```

Then use it in pipeline.py:
```python
cleaned_version_tag = _validate_version_tag(version_tag)
```

---

### 5. Unauthenticated Access to /codegen/generate Endpoint

**Severity:** HIGH
**File:** `proxmox_openapi/routes/codegen.py`
**Status:** ⚠️ NOT FIXED

**Problem:**
The `/codegen/generate` endpoint is a resource-intensive operation (headless browser crawl, parsing, code generation) with NO authentication or rate limiting. Anyone with access to the API can trigger expensive operations repeatedly, causing DoS.

**Recommended Fix:**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredential

security = HTTPBearer()

@router.post("/generate")
async def generate_viewer_codegen_artifacts(
    credentials: HTTPAuthCredential = Depends(security),
    persist: bool = Query(...),
    # ... other params ...
) -> dict[str, object]:
    """Run Proxmox API Viewer to OpenAPI and Pydantic generation pipeline (admin only)."""
    # Validate bearer token against configured API key
    if credentials.credentials != os.environ.get("CODEGEN_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    # ... rest of function ...
```

Or use environment-based access controls:
```python
if os.environ.get("PROXMOX_API_MODE") != "development":
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="/codegen endpoints require PROXMOX_API_MODE=development"
    )
```

---

## MEDIUM Issues

### 6. No Rate Limiting on Resource-Intensive Endpoints

**Severity:** MEDIUM
**File:** `proxmox_openapi/routes/codegen.py`, `proxmox_openapi/routes/mock.py`
**Status:** ⚠️ NOT FIXED

**Problem:**
Endpoints that perform intensive operations (codegen, mock data generation) have no rate limiting, allowing DoS attacks.

**Recommended Fix:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("1/hour")  # One codegen per hour per IP
@router.post("/generate")
async def generate_viewer_codegen_artifacts(...):
    ...
```

Add to `pyproject.toml`:
```toml
dependencies = [
    ...
    "slowapi>=0.1.9",
]
```

---

### 7. Proxy Authentication Credentials in Environment Variables

**Severity:** MEDIUM
**File:** `proxmox_openapi/sdk/backends/https.py` and proxy handling
**Status:** ⚠️ PARTIALLY MITIGATED

**Problem:**
HTTP proxy authentication may be passed via environment variables (HTTP_PROXY, HTTPS_PROXY) which are visible in process listings and logs.

**Recommended Fix:**
If proxy auth is needed, use a separate config file instead of environment variables:
```python
# In config file: /etc/proxmox-cli/.proxy.conf (mode 0o600)
[proxy]
url=http://proxy.internal.example.com:3128
user=proxy_user
password=<redacted>
```

And load it with proper permission checks:
```python
def load_proxy_config() -> dict | None:
    proxy_config_file = Path("~/.proxmox-cli/.proxy.conf").expanduser()

    # Check file permissions (must be 0o600)
    if proxy_config_file.exists():
        stat_info = proxy_config_file.stat()
        if stat_info.st_mode & 0o077:  # Check if group/other readable
            logger.warning(
                f"Proxy config file has overly permissive permissions: "
                f"oct({stat_info.st_mode}). Should be 0o600."
            )

    # ... load from file ...
```

---

### 8. Missing Authentication on Mock Endpoints

**Severity:** MEDIUM
**File:** `proxmox_openapi/routes/mock.py`
**Status:** ⚠️ PARTIALLY MITIGATED

**Problem:**
Mock endpoints don't require authentication even if `PROXMOX_API_MODE=real` is used elsewhere, potentially exposing API structure in production.

**Recommended Fix:**
```python
@router.get("/mock/schema")
async def get_mock_schema() -> dict:
    if os.environ.get("PROXMOX_API_MODE") == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Mock endpoints disabled in production mode"
        )
    return {...}
```

---

### 9. Information Disclosure: Detailed Error Messages

**Severity:** MEDIUM
**File:** Various route handlers
**Status:** ⚠️ PARTIALLY MITIGATED

**Problem:**
Error responses may leak internal structure (file paths, Python stack traces, internal hostnames).

**Example:**
```
$ curl https://api.example.com/codegen/generate?source_url=invalid
{"detail": "Traceback (most recent call last):\n  File \"/root/nms/proxmox-openapi/..."}
```

**Recommended Fix:**
Add a global exception handler to FastAPI:
```python
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    # Log full exception internally
    logger.exception("Unhandled exception", exc_info=exc)

    # Return generic error to client
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

# Only expose details if DEBUG mode is enabled
if os.environ.get("DEBUG", "false").lower() == "true":
    # return detailed error response with traceback
    pass
```

---

### 10. Credentials Visible in Environment Variables

**Severity:** MEDIUM
**File:** `proxmox_openapi/main.py` and `proxmox_openapi/proxmox/config.py`
**Status:** ⚠️ PARTIALLY MITIGATED

**Problem:**
Proxmox credentials (`PROXMOX_API_USERNAME`, `PROXMOX_API_PASSWORD`, `PROXMOX_API_TOKEN_*`) are read from environment variables and may be visible via `env`, `ps aux`, and process inspection tools.

**Recommended Fix:**
Add runtime masking of sensitive environment variables:
```python
def mask_sensitive_env_vars() -> None:
    """Replace sensitive env vars with placeholder values in os.environ."""
    sensitive_keys = [
        "PROXMOX_API_PASSWORD",
        "PROXMOX_API_TOKEN_SECRET",
        "PROXMOX_CLI_PASSWORD",
    ]
    for key in sensitive_keys:
        if key in os.environ:
            # Keep the original value for auth, but mask for display
            _original_env[key] = os.environ[key]
            os.environ[key] = "***REDACTED***"

mask_sensitive_env_vars()
```

And log a warning during startup:
```python
logger.warning("Sensitive environment variables detected. Consider using .env files or secret management.")
```

---

## LOW Issues

### 11. No Timeout on Playwright Browser Operations

**Severity:** LOW
**File:** `proxmox_openapi/proxmox_codegen/crawler.py` (line 56)
**Status:** ⚠️ NOT FIXED

**Problem:**
If the remote website is slow or intentionally delays responses, Playwright may hang indefinitely or for very long periods.

**Recommended Fix:**
```python
page.goto(url, wait_until="networkidle", timeout=30_000)  # 30 seconds
page.wait_for_selector("nav", timeout=10_000)  # 10 seconds
```

---

### 12. No Validation of JSON in Config Files

**Severity:** LOW
**File:** `proxmox_openapi/proxmox_cli/config.py` (line 104)
**Status:** ⚠️ PARTIALLY MITIGATED

**Problem:**
Config JSON is loaded without schema validation, allowing malformed configs to cause crashes.

**Recommended Fix:**
```python
from pydantic import BaseModel, ValidationError

class ConfigSchema(BaseModel):
    version: str
    default_profile: str
    profiles: dict[str, dict]  # with nested validation
    global: dict

def load_config() -> ConfigManager:
    # ... existing code ...
    try:
        data = json.loads(content)
        ConfigSchema(**data)  # Validate schema
    except ValidationError as e:
        raise ConfigError(f"Invalid config schema: {e}")
```

---

### 13. Potential Symlink Attack on Config Directory

**Severity:** LOW
**File:** `proxmox_openapi/proxmox_cli/config.py` (lines 200-220)
**Status:** ⚠️ PARTIALLY MITIGATED

**Problem:**
If an attacker can create symlinks in the home directory before the config file is created, they could redirect the config write to a different location.

**Recommended Fix:**
```python
import os

def save_config(self) -> None:
    path = self._config_path()

    # Ensure path is not a symlink
    if path.exists() and path.is_symlink():
        raise ConfigError(f"Config file is a symlink, refusing to overwrite: {path}")

    # Ensure parent directory is not a symlink
    if path.parent.exists() and path.parent.is_symlink():
        raise ConfigError(f"Config directory is a symlink: {path.parent}")

    # ... rest of function ...
```

---

### 14. Missing Telemetry/Security Event Logging

**Severity:** LOW
**File:** All route handlers
**Status:** ⚠️ NOT FIXED

**Problem:**
No audit logging for:
- Failed authentication attempts
- Unauthorized access to /codegen
- Large or unusual requests
- Configuration changes

**Recommended Fix:**
```python
import logging

audit_logger = logging.getLogger("audit")

@router.post("/codegen/generate")
async def generate_viewer_codegen_artifacts(request: Request, ...):
    audit_logger.info(
        "codegen_request",
        extra={
            "client_ip": request.client.host,
            "source_url": source_url,
            "version_tag": version_tag,
            "workers": workers,
        }
    )
    # ... rest of function ...
```

---

### 15. No Health Check Authentication

**Severity:** LOW
**File:** `proxmox_openapi/main.py` (lines 61-62)
**Status:** ⚠️ NOT FIXED

**Problem:**
The `/health` endpoint exposes the API is running without authentication, potentially leaking that the service exists.

**Recommended Fix:**
```python
@app.get("/health", include_in_schema=False)  # Hide from OpenAPI docs
async def health(request: Request) -> dict[str, str]:
    # Require internal IP or authorization
    if request.client.host not in ("127.0.0.1", "::1"):
        raise HTTPException(status_code=404)  # Pretend endpoint doesn't exist
    return {"status": "ready"}
```

---

## Summary Table

| Issue | Severity | Type | Status |
|-------|----------|------|--------|
| 1. SSRF in /codegen/generate | CRITICAL | Access Control | ⚠️ Not Fixed |
| 2. SSRF with custom version tags | CRITICAL | Access Control | ⚠️ Partial |
| 3. Missing CORS config | HIGH | API Security | ⚠️ Not Fixed |
| 4. Directory traversal in version_tag | HIGH | Input Validation | ⚠️ Partial |
| 5. Unauthenticated /codegen access | HIGH | Access Control | ⚠️ Not Fixed |
| 6. No rate limiting | MEDIUM | DoS Prevention | ⚠️ Not Fixed |
| 7. Proxy auth in env vars | MEDIUM | Secret Management | ⚠️ Partial |
| 8. Mock endpoints unauth'd | MEDIUM | Access Control | ⚠️ Partial |
| 9. Detailed error messages | MEDIUM | Info Disclosure | ⚠️ Partial |
| 10. Credentials in env vars | MEDIUM | Secret Management | ⚠️ Partial |
| 11. No Playwright timeout | LOW | Resource Limits | ⚠️ Not Fixed |
| 12. No JSON schema validation | LOW | Input Validation | ⚠️ Partial |
| 13. Symlink attacks on config | LOW | File Handling | ⚠️ Partial |
| 14. No audit logging | LOW | Observability | ⚠️ Not Fixed |
| 15. Health check unauth'd | LOW | Info Disclosure | ⚠️ Not Fixed |

---

## Priority Remediation Order

1. **CRITICAL (Implement First)**
   - Fix SSRF vulnerability in /codegen/generate with URL validation
   - Apply SSRF protection to custom version tags
   - Add authentication to /codegen endpoints

2. **HIGH (Implement Second)**
   - Add CORS middleware with restrictive defaults
   - Sanitize version_tag parameter
   - Add rate limiting to resource-intensive endpoints

3. **MEDIUM (Implement Third)**
   - Add generic error handler to prevent info disclosure
   - Implement audit logging for security events
   - Add proxy config file support instead of env vars

4. **LOW (Nice to Have)**
   - Add timeouts to Playwright operations
   - Add JSON schema validation
   - Add symlink attack protection
   - Restrict health endpoint access

---

## Verification Checklist

After implementing fixes:

```bash
# Test SSRF rejection
curl "http://localhost:8000/codegen/generate?source_url=http://127.0.0.1:6379"
# Should reject with 400 Bad Request, not attempt connection

# Test version_tag validation
curl "http://localhost:8000/codegen/generate?version_tag=../etc/passwd"
# Should reject with 400 Bad Request

# Test unauthenticated access rejection
curl -X POST "http://localhost:8000/codegen/generate"
# Should reject with 401/403 Unauthorized

# Test CORS headers
curl -H "Origin: https://evil.com" http://localhost:8000/
# Should not have CORS headers allowing cross-origin access

# Check for info disclosure in errors
curl "http://localhost:8000/nonexistent"
# Should return generic 404, not stack trace
```

---

**End of Security Review**

# SDK Implementation Plan

**Goal:** Evolve `proxmox-openapi` into a first-class Python SDK that works standalone (no FastAPI required), while keeping FastAPI as an optional layer for users who want an HTTP server.

**Reference:** [`proxmoxer`](../reference/proxmoxer.md) is the feature baseline. This plan does not copy proxmoxer as-is — every design decision is adapted to the existing architecture (async-first, aiohttp, OpenAPI-schema-aware, multi-version Proxmox support).

---

## Current Architecture (Baseline)

```
proxmox_openapi/
├── proxmox/
│   ├── client.py        # ProxmoxClient — async aiohttp HTTP client (real mode)
│   ├── config.py        # ProxmoxConfig — dataclass, env-var loader, validation
│   └── routes.py        # FastAPI route registration (real mode, schema-driven)
├── mock/                # In-memory CRUD mock server
├── proxmox_codegen/     # Proxmox API Viewer crawler + OpenAPI/Pydantic generators
├── routes/              # FastAPI routers (codegen, mock, versions)
├── schema.py            # Load/save generated OpenAPI schemas (versioned)
├── main.py              # Full FastAPI app (real + mock modes)
├── mock_main.py         # Standalone mock FastAPI app
└── __init__.py          # Exports: app, mock_app, run
```

**Key constraints to respect:**
- Async-first (aiohttp for HTTP, not requests)
- OpenAPI-schema-aware (generated schemas drive everything)
- Multi-version Proxmox support via `schema.py` version tagging
- `ProxmoxConfig` is the configuration contract
- FastAPI is an optional delivery mechanism, not a hard dependency of the SDK

---

## Target Architecture

```
proxmox_openapi/
├── sdk/                          # NEW: standalone SDK layer
│   ├── __init__.py               # SDK public exports
│   ├── api.py                    # ProxmoxSDK — main entry point
│   ├── resource.py               # ProxmoxResource — dynamic attribute navigation
│   ├── backends/                 # Backend abstraction layer
│   │   ├── __init__.py
│   │   ├── base.py               # AbstractBackend protocol/ABC
│   │   ├── https.py              # Async HTTPS backend (evolves ProxmoxClient)
│   │   ├── ssh_paramiko.py       # SSH backend using paramiko
│   │   ├── openssh.py            # SSH backend using openssh_wrapper
│   │   └── local.py              # Local pvesh backend
│   ├── auth/                     # Authentication strategies
│   │   ├── __init__.py
│   │   ├── ticket.py             # Password/ticket auth with auto-renewal
│   │   └── token.py              # API token auth
│   ├── services.py               # SERVICES registry (PVE, PMG, PBS)
│   ├── exceptions.py             # SDK exceptions (ResourceException, AuthenticationError)
│   └── tools/                    # High-level utilities
│       ├── __init__.py
│       ├── tasks.py              # Task/UPID tracking utilities
│       └── files.py              # File upload/download utilities
├── proxmox/                      # EXISTING: adapted (not replaced)
│   ├── client.py                 # Refactored → thin wrapper over sdk/backends/https.py
│   ├── config.py                 # Extended to cover all backends
│   └── routes.py                 # Unchanged: FastAPI real-mode routes
├── mock/                         # Unchanged
├── proxmox_codegen/              # Unchanged
├── routes/                       # Unchanged
├── schema.py                     # Unchanged
├── main.py                       # Unchanged (optionally gains SDK helpers)
├── mock_main.py                  # Unchanged
└── __init__.py                   # Extended: also exports ProxmoxSDK
```

**FastAPI is never imported inside `sdk/`.** The SDK has zero FastAPI dependency.

---

## Implementation Phases

### Phase 1 — Service Registry & Exceptions

**Files:** `sdk/services.py`, `sdk/exceptions.py`

#### 1.1 `sdk/services.py`

Centralize service metadata so all backends and the entry point share one source of truth.

```python
SERVICES: dict[str, ServiceConfig] = {
    "PVE": ServiceConfig(
        supported_backends=["https", "ssh_paramiko", "openssh", "local"],
        supported_auth_methods=["password", "token"],
        default_port=8006,
        token_separator="=",
        auth_cookie_name="PVEAuthCookie",
        api_path_prefix="/api2/json",
        cli_name="pvesh",
        cli_extra_options=["--output-format", "json"],
    ),
    "PMG": ServiceConfig(
        supported_backends=["https", "ssh_paramiko", "openssh", "local"],
        supported_auth_methods=["password"],
        default_port=8006,
        token_separator="=",
        auth_cookie_name="PMGAuthCookie",
        api_path_prefix="/api2/json",
        cli_name="pmgsh",
        cli_extra_options=["--output-format", "json"],
    ),
    "PBS": ServiceConfig(
        supported_backends=["https"],
        supported_auth_methods=["password", "token"],
        default_port=8007,
        token_separator=":",
        auth_cookie_name="PBSAuthCookie",
        api_path_prefix="/api2/json",
        cli_name=None,
        cli_extra_options=[],
    ),
}
```

**Adaptation note:** proxmoxer stores this as a plain dict of dicts. Here we use a `ServiceConfig` dataclass for type safety and IDE support — consistent with the existing `ProxmoxConfig` dataclass pattern.

#### 1.2 `sdk/exceptions.py`

Replace the current `proxmox_openapi/exception.py` `ProxmoxOpenAPIException` usage inside the SDK with typed exceptions. The existing `ProxmoxOpenAPIException` stays for FastAPI layer errors.

```python
class ProxmoxSDKError(Exception):
    """Base SDK exception."""

class ResourceException(ProxmoxSDKError):
    """API returned HTTP >= 400."""
    status_code: int
    status_message: str
    content: str
    errors: dict | None
    exit_code: int | None  # Only set for CLI backends

class AuthenticationError(ProxmoxSDKError):
    """Authentication failed."""

class BackendNotAvailableError(ProxmoxSDKError):
    """Requested backend dependency not installed."""
```

**Adaptation note:** proxmoxer's `ResourceException` is preserved as-is in naming — it is the de-facto standard for Proxmox Python libraries. `BackendNotAvailableError` is new: it gives a clear message when optional backend deps (paramiko, openssh_wrapper) are missing.

---

### Phase 2 — Backend Abstraction Layer

**Files:** `sdk/backends/base.py`, `sdk/backends/https.py`, `sdk/backends/ssh_paramiko.py`, `sdk/backends/openssh.py`, `sdk/backends/local.py`

#### 2.1 `sdk/backends/base.py` — Abstract Backend Protocol

```python
from typing import Protocol, Any

class AbstractBackend(Protocol):
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any: ...

    async def close(self) -> None: ...
```

**Adaptation note:** proxmoxer's backend contract uses three sync methods (`get_base_url`, `get_session`, `get_serializer`). Here we keep the existing async `request` interface from `ProxmoxClient` — it is a better fit for an async-first codebase.

#### 2.2 `sdk/backends/https.py` — Async HTTPS Backend

This is a **refactor** of the existing `proxmox_openapi/proxmox/client.py`, not a replacement. It moves the logic into the SDK and adds missing features.

**Features to add over existing `ProxmoxClient`:**

| Feature | Current `ProxmoxClient` | SDK HTTPS Backend |
|---|---|---|
| Password auth | ✅ | ✅ (unchanged) |
| API token auth | ✅ | ✅ (unchanged) |
| Auto ticket renewal (1h) | ❌ | ✅ NEW |
| Two-factor auth (TOTP/OTP) | ❌ | ✅ NEW |
| File upload (small) | ❌ | ✅ NEW |
| File upload (large, streaming) | ❌ | ✅ NEW (aiohttp multipart) |
| IPv6 address normalization | ❌ | ✅ NEW |
| Path prefix support | ❌ | ✅ NEW |
| HTTP proxy support | ❌ | ✅ NEW (aiohttp ProxyConnector) |
| Configurable timeout | ❌ | ✅ NEW |
| None-value filtering | Partial | ✅ full |
| FastAPI dependency | ✅ (raises HTTPException) | ❌ raises ResourceException |

**Ticket Renewal Strategy:**

```python
# Proxmoxer renews at 3600s (1h). PVE tickets valid 2h.
# This project adopts the same strategy: renew before expiry.
TICKET_RENEW_INTERVAL = 3600  # seconds

async def _maybe_renew_ticket(self) -> None:
    if self._ticket_acquired_at is None:
        return
    age = time.monotonic() - self._ticket_acquired_at
    if age >= TICKET_RENEW_INTERVAL:
        await self._authenticate_with_password()
```

**Two-Factor Auth Flow:**

```python
# Step 1: POST /access/ticket → may return NeedTFA in data
# Step 2: If NeedTFA, POST /access/ticket again with:
#   tfa-challenge=<challenge_from_step1>&password=<otp_code>
```

**Large File Upload (aiohttp streaming):**

```python
# Unlike proxmoxer which uses requests_toolbelt, we use aiohttp's
# native FormData with async file reading.
# Threshold: same 10 MiB as proxmoxer for API consistency.
STREAMING_SIZE_THRESHOLD = 10 * 1024 * 1024  # 10 MiB

async def upload(self, path: str, *, content_type: str, filename: str, file: IO) -> Any:
    form = aiohttp.FormData()
    form.add_field("content", content_type)
    form.add_field("filename", file, filename=filename)
    # aiohttp streams the file automatically
```

**IPv6 Normalization (new utility in `sdk/backends/https.py`):**

```python
def _normalize_host(host: str, default_port: int) -> str:
    """Wrap bare IPv6 addresses in brackets and append default port if missing."""
    # "2001:db8::1"        → "https://[2001:db8::1]:8006"
    # "[2001:db8::1]:8007" → "https://[2001:db8::1]:8007" (unchanged)
    # "pve.example.com"   → "https://pve.example.com:8006"
```

#### 2.3 `sdk/backends/ssh_paramiko.py` — SSH Paramiko Backend

**Dependencies:** `paramiko` (optional, install extra: `pip install proxmox-openapi[ssh]`)

**Features:**
- Pure Python SSH using `paramiko.SSHClient` with `AutoAddPolicy`
- Password or private key authentication
- File upload via SFTP (`putfo`)
- Inherits command building from `CommandBaseBackend` (see Phase 2.5)

**Adaptation note:** proxmoxer's ssh_paramiko is sync. Since SSH execution is inherently blocking (subprocess-like), this backend wraps calls in `asyncio.get_event_loop().run_in_executor()` to remain non-blocking in an async context — consistent with the async-first project design.

#### 2.4 `sdk/backends/openssh.py` — OpenSSH Backend

**Dependencies:** `openssh_wrapper` (optional, install extra: `pip install proxmox-openapi[ssh]`)

**Features:**
- Uses `openssh_wrapper.SSHConnection`
- Respects `~/.ssh/config`
- SSH agent forwarding
- Identity file support
- File upload via SCP
- `run_in_executor` wrapping same as paramiko

#### 2.5 `sdk/backends/local.py` — Local pvesh Backend

**Dependencies:** None (stdlib only — `subprocess`, `shutil`)

**Features:**
- Executes `pvesh` (or `pmgsh`) locally via `subprocess.Popen`
- Direct file copy via `shutil.copyfileobj`
- No authentication needed
- `run_in_executor` wrapping for async compatibility

#### 2.6 Shared CLI Backend Mixin: `CommandBaseBackend`

A mixin (not an ABC) shared by `ssh_paramiko`, `openssh`, and `local` backends.

**Responsibilities (adapted from proxmoxer's `CommandBaseSession`):**

```
HTTP method → pvesh command:
  GET    → get
  POST   → create
  PUT    → set
  DELETE → delete

Command template:
  {cli_name} {verb} {url} [--output-format json] [-key value ...]

Special handling:
  - QEMU agent exec: auto-split command strings via shlex.split()
    (Windows: skip split, pass as-is)
  - File upload workaround: write temp file on host, pass path to pvesh
  - sudo prefix: optional for non-root callers
  - Response parsing: detect HTTP status codes in stderr
  - UPID detection: task creation succeeds even if stderr shows error
```

**Response Object:**

```python
@dataclass
class CliResponse:
    status_code: int
    exit_code: int
    content: bytes

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")
```

---

### Phase 3 — Authentication Layer

**Files:** `sdk/auth/ticket.py`, `sdk/auth/token.py`

These are strategy objects consumed by `sdk/backends/https.py`.

#### 3.1 `sdk/auth/ticket.py` — Password/Ticket Auth

```python
class TicketAuth:
    """
    Async auth handler for username/password flow.

    - Authenticates via POST /access/ticket
    - Stores PVE/PMG/PBSAuthCookie and CSRFPreventionToken
    - Supports TOTP/OTP two-factor challenge
    - Auto-renews ticket after TICKET_RENEW_INTERVAL seconds
    """

    async def authenticate(self, session: aiohttp.ClientSession) -> None: ...
    async def maybe_renew(self, session: aiohttp.ClientSession) -> None: ...
    def build_headers(self, method: str) -> dict[str, str]: ...
    def build_cookies(self) -> dict[str, str]: ...
```

**2FA flow:**

```
POST /access/ticket {username, password}
  → if data["NeedTFA"]:
      POST /access/ticket {username, password=otp_code, tfa-challenge=challenge}
  → store ticket + CSRFPreventionToken
```

#### 3.2 `sdk/auth/token.py` — API Token Auth

```python
class TokenAuth:
    """
    Stateless auth handler for API token flow.

    Token format:
      PVE/PMG: PVEAPIToken={user}!{token_name}={token_value}
      PBS:     PBSAPIToken={user}!{token_name}:{token_value}

    The separator difference (= vs :) is resolved from SERVICES registry.
    """

    def build_headers(self, method: str) -> dict[str, str]: ...
```

---

### Phase 4 — ProxmoxResource (Dynamic Navigation)

**File:** `sdk/resource.py`

The centerpiece of the SDK's user-facing API.

#### Design

```python
class ProxmoxResource:
    """
    Provides dynamic Proxmox API navigation via attribute access.

    Each attribute access or call returns a new ProxmoxResource
    with an extended URL path. HTTP methods execute the request.

    Navigation styles supported:
        proxmox.nodes.get()
        proxmox.nodes('pve1').qemu.get()
        proxmox.nodes('pve1').qemu(100).status.current.get()
        proxmox.nodes('pve1/qemu/100').status.current.get()
        proxmox.nodes(['pve1', 'qemu', '100']).status.current.get()
    """

    def __init__(self, base_url: str, backend: AbstractBackend) -> None: ...

    def __getattr__(self, item: str) -> ProxmoxResource:
        if item.startswith("_"):
            raise AttributeError(item)
        return ProxmoxResource(
            base_url=_url_join(self._base_url, item),
            backend=self._backend,
        )

    def __call__(self, resource_id: str | int | list | tuple | None = None) -> ProxmoxResource:
        if resource_id is None:
            return self
        if isinstance(resource_id, (list, tuple)):
            return ProxmoxResource(
                base_url=_url_join(self._base_url, *[str(r) for r in resource_id]),
                backend=self._backend,
            )
        return ProxmoxResource(
            base_url=_url_join(self._base_url, str(resource_id)),
            backend=self._backend,
        )

    # HTTP methods
    async def get(self, *args, **params) -> Any: ...
    async def post(self, *args, **data) -> Any: ...
    async def put(self, *args, **data) -> Any: ...
    async def delete(self, *args, **params) -> Any: ...

    # Aliases (proxmoxer compatibility)
    async def create(self, *args, **data) -> Any: ...   # alias for post
    async def set(self, *args, **data) -> Any: ...      # alias for put
```

**URL Building (adapted from proxmoxer, using existing stdlib):**

```python
import posixpath
from urllib.parse import urlsplit, urlunsplit

def _url_join(base: str, *args: str) -> str:
    scheme, netloc, path, query, fragment = urlsplit(base)
    path = path or "/"
    path = posixpath.join(path, *args)
    return urlunsplit((scheme, netloc, path, query, fragment))
```

**None-value filtering (applied before every request):**

```python
def _filter_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}
```

**Adaptation note:** proxmoxer uses positional `*args` in HTTP methods to extend the path before the call. This project keeps the same pattern for API compatibility.

---

### Phase 5 — ProxmoxSDK Entry Point

**File:** `sdk/api.py`

The main user-facing class. No FastAPI dependency.

```python
class ProxmoxSDK:
    """
    Entry point for the Proxmox OpenAPI SDK.

    Usage (async):
        async with ProxmoxSDK(
            host="pve.example.com",
            user="admin@pam",
            password="secret",
            service="PVE",
            verify_ssl=False,
        ) as proxmox:
            nodes = await proxmox.nodes.get()
            await proxmox.nodes("pve1").qemu.post(vmid=100, name="test")

    Usage (sync convenience wrapper — see Phase 6):
        proxmox = ProxmoxSDK.sync(host=..., user=..., password=...)
        nodes = proxmox.nodes.get()

    Multi-service:
        pve = ProxmoxSDK(host="pve.example.com", user="admin@pam", ...)
        pmg = ProxmoxSDK(host="mail.example.com", user="admin@pmg", ..., service="PMG")
        pbs = ProxmoxSDK(host="backup.example.com", user="admin@pbs", ..., service="PBS")

    Token auth:
        proxmox = ProxmoxSDK(
            host="pve.example.com",
            user="monitoring@pve",
            token_name="api-token",
            token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            service="PVE",
        )

    Mock mode (no real Proxmox):
        proxmox = ProxmoxSDK.mock(schema_version="latest")
        nodes = await proxmox.nodes.get()  # returns mock data

    SSH backend:
        proxmox = ProxmoxSDK(
            host="pve.example.com",
            user="root",
            password="secret",
            backend="ssh_paramiko",
            service="PVE",
        )

    Local backend (on Proxmox host):
        proxmox = ProxmoxSDK(backend="local", service="PVE")
    """

    def __init__(
        self,
        host: str | None = None,
        *,
        user: str | None = None,
        password: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        otp: str | None = None,
        otptype: str = "totp",
        service: Literal["PVE", "PMG", "PBS"] = "PVE",
        backend: str = "https",
        port: int | None = None,
        path_prefix: str = "",
        verify_ssl: bool = True,
        cert: str | None = None,
        timeout: int = 5,
        proxies: dict[str, str] | None = None,
        sudo: bool = False,
        private_key_file: str | None = None,
        identity_file: str | None = None,
        forward_ssh_agent: bool = False,
        config_file: str | None = None,
    ) -> None: ...

    # Async context manager
    async def __aenter__(self) -> ProxmoxResource: ...
    async def __aexit__(self, *args) -> None: ...

    # get_tokens() — returns (ticket, csrf_token) for https backend
    async def get_tokens(self) -> tuple[str, str]: ...

    # Class methods for common configurations
    @classmethod
    def mock(cls, schema_version: str = "latest") -> ProxmoxSDK: ...

    @classmethod
    def from_config(cls, config: ProxmoxConfig) -> ProxmoxSDK: ...

    @classmethod
    def sync(cls, **kwargs) -> SyncProxmoxSDK: ...
```

**Initialization logic:**

```
1. Validate service in SERVICES registry
2. Validate backend is supported for that service
3. Validate auth method (password vs token vs local)
4. Resolve port (kwargs > service default)
5. Normalize host (IPv6 bracket wrapping)
6. Select and instantiate backend
7. Wrap backend in ProxmoxResource (dynamic navigation)
```

---

### Phase 6 — Sync Wrapper

**File:** `sdk/sync.py`

Users who don't want async can use the sync wrapper. It is a thin layer over the async API using `asyncio.run()`.

```python
class SyncProxmoxSDK:
    """
    Synchronous wrapper around ProxmoxSDK for scripts that cannot use async/await.

    Usage:
        proxmox = SyncProxmoxSDK(
            host="pve.example.com",
            user="admin@pam",
            password="secret",
        )
        nodes = proxmox.nodes.get()
        proxmox.close()

    Context manager:
        with SyncProxmoxSDK(...) as proxmox:
            nodes = proxmox.nodes.get()
    """
```

**Adaptation note:** proxmoxer is sync-only (requests-based). This project is async-first, but a sync wrapper preserves compatibility for users coming from proxmoxer. The `SyncProxmoxSDK` wraps each `await` call in `asyncio.run()` (or a persistent event loop in `__enter__`). This is the correct approach for a project that already runs aiohttp.

---

### Phase 7 — Tools: Task Management

**File:** `sdk/tools/tasks.py`

```python
class Tasks:
    """
    Utility class for Proxmox task (UPID) management.

    Usage:
        task_id = await proxmox.nodes("pve1").qemu(100).status.start.post()
        status = await Tasks.blocking_status(proxmox, task_id, timeout=300, polling_interval=2)
        info = Tasks.decode_upid(task_id)
        log_text = Tasks.decode_log(await proxmox.nodes("pve1").tasks(task_id).log.get())
    """

    @staticmethod
    async def blocking_status(
        proxmox: ProxmoxResource,
        task_id: str,
        *,
        timeout: float = 300,
        polling_interval: float = 2.0,
    ) -> dict[str, Any]:
        """Poll task until completion or timeout. Raises TimeoutError."""
        ...

    @staticmethod
    def decode_upid(upid: str) -> dict[str, Any]:
        """
        Parse UPID string into components.

        Format: UPID:{node}:{pid}:{pstart}:{starttime}:{type}:{id}:{user}:{comment}

        Returns:
            {
                "upid": str,
                "node": str,
                "pid": int,
                "pstart": int,
                "starttime": datetime,
                "type": str,
                "id": str,
                "user": str,
                "comment": str,
            }
        """
        ...

    @staticmethod
    def decode_log(log_data: list[dict]) -> str:
        """Convert Proxmox task log entries to human-readable text."""
        ...
```

**Adaptation note:** proxmoxer's `Tasks.blocking_status` is sync and uses `time.sleep`. This project uses `asyncio.sleep` for non-blocking polling. The same `polling_interval` and `timeout` API is preserved.

---

### Phase 8 — Tools: File Utilities

**File:** `sdk/tools/files.py`

```python
class Files:
    """
    High-level file operations against Proxmox storage.

    Usage:
        files = Files(proxmox, node="pve1", storage="local")

        # Upload local ISO
        status = await files.upload_local_file_to_storage(
            "/path/to/debian.iso",
            do_checksum_check=True,
            blocking_status=True,
        )

        # Download from URL to Proxmox storage
        status = await files.download_file_to_storage(
            "https://cdimage.debian.org/debian-12.0.0-amd64-netinst.iso",
            blocking_status=True,
        )
    """

    CHECKSUM_ALGORITHMS = ["sha512", "sha256", "sha224", "sha384", "md5", "sha1"]

    # Checksum discovery strategies (same as proxmoxer):
    #   1. {url}.{algo}           e.g. file.iso.sha512
    #   2. {url}.{ALGO}           e.g. file.iso.SHA512
    #   3. {base_url}/SHA512SUMS  (containing filename)
    #   4. {base_url}/sha512sums  (containing filename)

    async def upload_local_file_to_storage(
        self,
        local_path: str,
        *,
        do_checksum_check: bool = False,
        blocking_status: bool = True,
    ) -> dict[str, Any]: ...

    async def download_file_to_storage(
        self,
        url: str,
        *,
        blocking_status: bool = True,
    ) -> dict[str, Any]: ...

    async def _discover_checksum(self, url: str) -> tuple[str, str] | None:
        """Try to find checksum for a URL. Returns (algo, hash) or None."""
        ...
```

**Adaptation note:** proxmoxer's `Files` utility is sync and uses `requests`. This project uses `aiohttp` for HTTP and `asyncio` for file I/O. The checksum discovery logic and algorithm priority are preserved identically.

---

### Phase 9 — Mock Backend Integration

**File:** `sdk/backends/mock.py`

Expose the existing in-memory mock store (`proxmox_openapi/mock/state.py`) as an SDK backend. This means `ProxmoxSDK.mock()` works without starting a FastAPI server.

```python
class MockBackend:
    """
    In-memory mock backend — wraps the existing mock store.

    No network required. Reads schema from generated OpenAPI files.
    Supports full CRUD on mock data (same as the mock FastAPI server).

    Usage:
        proxmox = ProxmoxSDK.mock(schema_version="latest")
        nodes = await proxmox.nodes.get()       # returns mock data
        await proxmox.nodes.post(node="test")   # mutates mock store
    """

    def __init__(self, schema_version: str = "latest") -> None:
        # Load schema from existing schema.py
        # Initialize mock state from existing mock/state.py
        ...

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        data: dict | None = None,
    ) -> Any:
        # Delegate to existing mock/routes.py logic
        # (extracted into a callable form, no HTTP layer)
        ...
```

**Adaptation note:** This is entirely new to proxmoxer (which has no mock concept). It reuses the existing mock infrastructure without running FastAPI.

---

### Phase 10 — `ProxmoxConfig` Extension

**File:** `proxmox/config.py` (extend existing, no breaking changes)

Add SDK-relevant fields while keeping all existing fields and the `from_env()` method.

```python
@dataclass(frozen=True)
class ProxmoxConfig:
    # Existing fields (unchanged):
    api_mode: str
    api_url: str | None
    token_id: str | None
    token_secret: str | None
    username: str | None
    password: str | None
    verify_ssl: bool

    # New fields for SDK:
    service: str = "PVE"
    backend: str = "https"
    timeout: int = 5
    otp: str | None = None
    otptype: str = "totp"
    cert: str | None = None
    proxies: dict[str, str] | None = None
    path_prefix: str = ""
    port: int | None = None

    @classmethod
    def from_env(cls) -> ProxmoxConfig:
        # Existing env vars preserved + new ones:
        # PROXMOX_API_SERVICE (default: "PVE")
        # PROXMOX_API_BACKEND (default: "https")
        # PROXMOX_API_TIMEOUT (default: "5")
        ...

    def to_sdk_kwargs(self) -> dict:
        """Convert config to ProxmoxSDK constructor kwargs."""
        ...
```

---

### Phase 11 — Public API & Package Exports

**File:** `proxmox_openapi/__init__.py` (extend, no breaking changes)

```python
# Existing exports (unchanged):
from proxmox_openapi.main import app
from proxmox_openapi.mock_main import app as mock_app, run

# New SDK exports:
from proxmox_openapi.sdk.api import ProxmoxSDK
from proxmox_openapi.sdk.sync import SyncProxmoxSDK
from proxmox_openapi.sdk.exceptions import ResourceException, AuthenticationError
from proxmox_openapi.sdk.tools.tasks import Tasks
from proxmox_openapi.sdk.tools.files import Files

__all__ = [
    # Existing
    "app", "mock_app", "run",
    # SDK
    "ProxmoxSDK", "SyncProxmoxSDK",
    "ResourceException", "AuthenticationError",
    "Tasks", "Files",
    "__version__",
]
```

---

### Phase 12 — Optional Dependencies & Extras

**File:** `pyproject.toml`

```toml
[project.optional-dependencies]
ssh = ["paramiko>=3.0", "openssh-wrapper>=0.7"]
all = ["paramiko>=3.0", "openssh-wrapper>=0.7"]
```

The `https` backend (aiohttp) is already a required dependency, so no new extra is needed for it. SSH backends are truly optional and imported lazily:

```python
# In sdk/backends/ssh_paramiko.py
try:
    import paramiko
except ImportError as exc:
    raise BackendNotAvailableError(
        "paramiko is required for the ssh_paramiko backend. "
        "Install it with: pip install proxmox-openapi[ssh]"
    ) from exc
```

---

## Refactoring Plan for Existing Code

### `proxmox_openapi/proxmox/client.py`

**Current role:** Full async HTTP client, raises `fastapi.HTTPException`.
**Post-refactor role:** Thin adapter — delegates to `sdk/backends/https.py`, translates `ResourceException` → `HTTPException` for the FastAPI layer.

```python
# After refactor:
class ProxmoxClient:
    """FastAPI adapter over the SDK HTTPS backend."""

    def __init__(self, config: ProxmoxConfig) -> None:
        from proxmox_openapi.sdk.backends.https import HttpsBackend
        self._backend = HttpsBackend.from_config(config)

    async def request(self, method, path, *, params=None, json=None) -> Any:
        try:
            return await self._backend.request(method, path, params=params, data=json)
        except ResourceException as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.content)
```

This approach:
- Keeps `proxmox/routes.py` working unchanged
- Removes code duplication (auth, SSL, etc. live only in the SDK layer)
- FastAPI layer stays clean: it only does HTTP translation

---

## Usage Examples (Post-Implementation)

### Async SDK Usage

```python
import asyncio
from proxmox_openapi import ProxmoxSDK

async def main():
    # Password auth
    async with ProxmoxSDK(
        host="pve.example.com",
        user="admin@pam",
        password="secret",
        verify_ssl=False,
    ) as proxmox:
        nodes = await proxmox.nodes.get()
        print(nodes)

        # Create VM
        await proxmox.nodes("pve1").qemu.post(
            vmid=101, name="test-vm", memory=2048, cores=2
        )

        # Wait for task
        from proxmox_openapi import Tasks
        task_id = await proxmox.nodes("pve1").qemu(101).status.start.post()
        await Tasks.blocking_status(proxmox, task_id, timeout=60)

asyncio.run(main())
```

### Sync SDK Usage

```python
from proxmox_openapi import SyncProxmoxSDK

with SyncProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="secret",
    verify_ssl=False,
) as proxmox:
    nodes = proxmox.nodes.get()
    vms = proxmox.nodes("pve1").qemu.get()
```

### Token Auth

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="monitoring@pve",
    token_name="read-only",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### Multi-Service

```python
from proxmox_openapi import ProxmoxSDK

pve = ProxmoxSDK(host="pve.example.com", user="admin@pam", password="s3cr3t")
pmg = ProxmoxSDK(host="mail.example.com", user="admin@pmg", password="s3cr3t", service="PMG")
pbs = ProxmoxSDK(host="backup.example.com", user="admin@pbs", password="s3cr3t", service="PBS")
```

### SSH Backend

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="root",
    password="secret",
    backend="ssh_paramiko",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### Local Backend (on Proxmox host)

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(backend="local", service="PVE") as proxmox:
    nodes = await proxmox.nodes.get()
```

### Mock Mode (no server, no real Proxmox)

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK.mock(schema_version="latest") as proxmox:
    nodes = await proxmox.nodes.get()   # returns generated mock data
```

### File Upload

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(host="pve.example.com", user="admin@pam", password="s") as proxmox:
    with open("/path/to/debian.iso", "rb") as f:
        await proxmox.nodes("pve1").storage("local").upload.post(
            content="iso",
            filename=f,
        )
```

### File Utilities

```python
from proxmox_openapi import ProxmoxSDK, Files

async with ProxmoxSDK(...) as proxmox:
    files = Files(proxmox, node="pve1", storage="local")
    await files.upload_local_file_to_storage("/path/to/debian.iso", do_checksum_check=True)
    await files.download_file_to_storage("https://cdimage.debian.org/debian-12.0.0-amd64-netinst.iso")
```

### Error Handling

```python
from proxmox_openapi import ProxmoxSDK, ResourceException, AuthenticationError

try:
    async with ProxmoxSDK(host="pve.example.com", user="admin@pam", password="wrong") as proxmox:
        pass
except AuthenticationError as e:
    print(f"Auth failed: {e}")

async with ProxmoxSDK(...) as proxmox:
    try:
        await proxmox.nodes("pve1").qemu(999).status.current.get()
    except ResourceException as e:
        print(f"HTTP {e.status_code}: {e.content}")
```

### FastAPI is still optional and unchanged

```python
# Still works exactly as before — zero breaking changes
import uvicorn
from proxmox_openapi import app

uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Implementation Order

| Phase | File(s) | Priority | Notes |
|---|---|---|---|
| 1 | `sdk/services.py`, `sdk/exceptions.py` | **High** | Foundation — everything depends on this |
| 2.1 | `sdk/backends/base.py` | **High** | Protocol definition |
| 2.2 | `sdk/backends/https.py` | **High** | Core backend; refactors existing `client.py` |
| 4 | `sdk/resource.py` | **High** | Dynamic navigation — main user-facing primitive |
| 5 | `sdk/api.py` | **High** | Entry point |
| 6 | `sdk/sync.py` | **Medium** | Sync wrapper |
| 3 | `sdk/auth/ticket.py`, `sdk/auth/token.py` | **Medium** | Auth strategies (used by https backend) |
| 7 | `sdk/tools/tasks.py` | **Medium** | Task utilities |
| 10 | `proxmox/config.py` extension | **Medium** | Non-breaking extension |
| 9 | `sdk/backends/mock.py` | **Medium** | Reuse existing mock infra |
| 11 | `__init__.py` extension | **Medium** | Public exports |
| 2.5 | `CommandBaseBackend` mixin | **Low** | Required for SSH/local |
| 2.3 | `sdk/backends/ssh_paramiko.py` | **Low** | Optional dep |
| 2.4 | `sdk/backends/openssh.py` | **Low** | Optional dep |
| 2.6 | `sdk/backends/local.py` | **Low** | Optional (needs Proxmox host) |
| 8 | `sdk/tools/files.py` | **Low** | Advanced utility |
| 12 | `pyproject.toml` extras | **Low** | Packaging |

---

## Design Decision Summary

| Decision | Choice | Rationale |
|---|---|---|
| Async or sync? | Async-first (`async/await`, aiohttp) | Consistent with existing architecture; sync wrapper provided for scripts |
| HTTP library? | aiohttp (existing) | Not requests (proxmoxer) — project is already aiohttp, no reason to add requests |
| Entry point name? | `ProxmoxSDK` | `ProxmoxAPI` is proxmoxer's name; distinct name avoids confusion in environments where both are installed |
| FastAPI dependency in SDK? | None | SDK is completely independent; FastAPI uses SDK via thin adapter |
| Breaking changes to existing API? | None | All existing exports and behavior preserved |
| Mock mode? | SDK backend wrapping existing mock store | Unique feature of this project; no FastAPI needed for mock |
| Service support? | PVE + PMG + PBS | Feature parity with proxmoxer |
| SSH backends? | Optional extras | Matches proxmoxer's optional dependency model |
| CLI backend abstraction? | `CommandBaseBackend` mixin | DRY — same pattern as proxmoxer's `CommandBaseSession` |
| Ticket renewal? | Same 3600s interval as proxmoxer | PVE tickets valid 2h; renew at 1h is safe and well-proven |
| None filtering? | Applied in `ProxmoxResource._request` | Single place, consistent for all HTTP methods |

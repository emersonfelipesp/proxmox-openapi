# Security Hardening

This document describes the security controls implemented in proxmox-openapi, including what is protected, how each control works, and how to verify it.

---

## SSRF Protection

All user-supplied URLs passed to the codegen pipeline are validated by `validate_source_url()` in `proxmox_codegen/security.py` before any outbound request is made.

### What is blocked

| Category | Examples | Error |
|---|---|---|
| Non-HTTPS schemes | `file://`, `gopher://`, `http://` (default) | `Invalid URL scheme` |
| Private IPv4 ranges | `10.x.x.x`, `192.168.x.x`, `172.16–31.x.x`, `127.x.x.x`, `169.254.x.x` | `SSRF attempt blocked: private IP range` |
| Private IPv6 ranges | `::1`, `fe80::`, `fc00::` | `SSRF attempt blocked: private IPv6 range` |
| IPv4-mapped IPv6 | `::ffff:127.0.0.1`, `::ffff:10.0.0.1` | `SSRF attempt blocked: IPv6-mapped address` |
| 6to4 addresses | `2002:7f00::1` (encodes 127.0.0.1) | `SSRF attempt blocked: IPv6-mapped address` |
| Localhost strings | `localhost`, `127.` prefix patterns | `SSRF attempt blocked: localhost` |
| Non-Proxmox domains | Any hostname not under `*.proxmox.com` | `not in the allowed domains list` |

### Domain allowlist

By default only official Proxmox documentation domains are permitted:

```
pve.proxmox.com
pmg.proxmox.com
pbs.proxmox.com
proxmox.com
```

To allow other domains (e.g. a self-hosted API viewer), pass `allow_any_domain=True` explicitly in code. The API endpoint does **not** expose this flag to callers.

### HTTP opt-in

Plain HTTP is blocked by default. Pass `allow_http=True` to `validate_source_url()` in trusted internal tooling only.

### Version tag validation

Version tags used in codegen URLs and file paths are validated by `validate_version_tag()`:

- Only `[a-zA-Z0-9._-]` characters are permitted
- `..`, `/`, and `\` are rejected (prevents path traversal)
- Empty strings are rejected

---

## Codegen Endpoint Authentication

`POST /codegen/generate` and related endpoints require a Bearer token set via the `CODEGEN_API_KEY` environment variable.

```bash
export CODEGEN_API_KEY=your-secret-key

curl -H "Authorization: Bearer your-secret-key" \
     -X POST "http://localhost:8000/codegen/generate?..."
```

Missing or wrong credentials return `401 Unauthorized`. The endpoint is also rate-limited to **1 request per hour per IP** to prevent abuse.

---

## Rate Limiting

SlowAPI rate limits are applied to resource-intensive endpoints:

| Endpoint | Limit |
|---|---|
| `POST /codegen/generate` | 1 / hour |
| `GET /codegen/openapi` | 5 / hour |
| `GET /codegen/pydantic` | 5 / hour |

Rate limiting uses the direct client IP. Behind a trusted reverse proxy, configure `X-Forwarded-For` forwarding at the proxy layer.

---

## CORS

CORS is disabled by default (no origins allowed). Enable it by setting `CORS_ORIGINS`:

```bash
export CORS_ORIGINS=https://your-app.example.com,https://staging.example.com
```

When set, allowed headers are restricted to:

```
Content-Type, Authorization, X-Requested-With
```

Wildcards (`*`) are never used for headers or origins.

---

## Health Endpoint Restriction

`GET /health` returns `404 Not Found` for any client not connecting from localhost. This prevents the endpoint from being used as a service-discovery probe.

Allowed hosts: `127.0.0.1`, `::1`, `localhost`.
`testclient` (Starlette test helper) is only added when `TESTING=1` is set.

---

## Error Responses

Unhandled exceptions are caught by a global handler and returned as a generic `500` response:

```json
{"detail": "An internal server error occurred."}
```

Stack traces, file paths, and internal state are never sent to clients. Full exception details are logged server-side at `ERROR` level.

---

## Credential Handling

### Environment variables

Proxmox credentials (`PROXMOX_API_TOKEN_SECRET`, `PROXMOX_API_PASSWORD`, `PROXMOX_API_OTP`) are read once at startup and then overwritten with `"********"` in `os.environ`. Subsequent code cannot accidentally read the raw values from the environment.

### CLI config file

The CLI stores credentials in `~/.proxmox-cli/config.json`. On write:

- The config directory is set to `0700`
- The config file is set to `0600`
- Writing is refused if the file or its parent directory is a symbolic link

On load, a warning is emitted if the file has group or other read/write permissions.

### Log sanitization

A `SensitiveDataFilter` is applied to all log output. It redacts values following these patterns before anything reaches stdout:

```
password=…   token_value=…   token_secret=…
PVEAuthCookie=…   PMGAuthCookie=…   PBSAuthCookie=…
CSRFPreventionToken=…   Authorization=…
```

---

## SSH Backend Security

### Host key verification (Paramiko)

The Paramiko SSH backend uses `WarningPolicy` (logs unknown host keys) instead of `AutoAddPolicy` (silently accepts any key). System `known_hosts` is loaded automatically.

To enforce strict verification, pass a custom policy at construction:

```python
from paramiko import RejectPolicy
from proxmox_openapi.sdk.backends.ssh_paramiko import SshParamikoBackend

backend = SshParamikoBackend(
    host="pve.example.com",
    user="root",
    service_config=...,
    host_key_policy=RejectPolicy(),
)
```

### Shell injection prevention

SSH command execution uses `shlex.join()` to properly quote all arguments. Remote temp file cleanup uses `shlex.quote()` on each path. The OpenSSH backend uses `shlex.join()` natively.

### Temp file names

Uploaded temp files on the remote host use `secrets.token_hex(8)` (64-bit random) instead of `id(object)` (predictable memory address).

### Remote cleanup

Both SSH backends clean up temp files uploaded to the remote host in a `finally` block, preventing data leakage from failed transfers.

---

## SSL/TLS

### Real API mode

SSL certificate verification is enabled by default (`PROXMOX_API_VERIFY_SSL=true`). Disable only in trusted internal networks:

```bash
export PROXMOX_API_VERIFY_SSL=false
```

### Ticket authentication

The `TicketAuth` handler uses the same SSL context configured for the backend when making the `/access/ticket` POST. This ensures that `verify_ssl=False` applies consistently across both auth and API requests rather than silently defaulting to system CAs for the auth step.

---

## Security Checklist for Deployment

```bash
# Verify SSRF protection rejects private IPs
curl "http://localhost:8000/codegen/generate?source_url=http://169.254.169.254/"
# → 400 Bad Request

# Verify codegen requires auth
curl -X POST "http://localhost:8000/codegen/generate"
# → 401 Unauthorized

# Verify health endpoint is hidden
curl "http://external-host:8000/health"
# → 404 Not Found

# Verify error responses don't leak internals
curl "http://localhost:8000/nonexistent-path-xyz"
# → 404 with {"detail": "Not Found"} — no stack trace
```

---

## Environment Variables Reference

| Variable | Purpose | Default |
|---|---|---|
| `CODEGEN_API_KEY` | Bearer token for `/codegen/*` endpoints | — (required for codegen) |
| `CORS_ORIGINS` | Comma-separated list of allowed origins | `""` (disabled) |
| `PROXMOX_API_VERIFY_SSL` | Enable SSL certificate verification | `true` |
| `PROXMOX_API_TOKEN_SECRET` | API token secret (cleared from env after read) | — |
| `PROXMOX_API_PASSWORD` | Password auth (cleared from env after read) | — |
| `TESTING` | Add `testclient` to health endpoint allow-list | `""` (disabled) |

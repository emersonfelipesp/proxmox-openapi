# Performance

This document describes the performance characteristics of proxmox-openapi and the optimisations applied to startup time, per-request throughput, and the SDK hot paths.

---

## Startup Time

### Lazy package imports

`import proxmox_openapi` no longer constructs any FastAPI app or imports the SDK. All top-level exports are resolved on first attribute access via `__getattr__`. This means:

- CLI tools that `import proxmox_openapi` for `__version__` or SDK classes start without paying the FastAPI app construction cost.
- The `app` and `mock_app` attributes are only materialised when accessed (e.g. by uvicorn).

### Route registration

646 mock routes are registered at startup. The critical path includes:

| Step | Before | After |
|---|---|---|
| Child path discovery | O(P²) scan — ~417K iterations for 646 paths | O(P) single-pass index, ~646 iterations |
| Schema fingerprint | `model_dump` + `json.dumps` + `sha256` on every call | Computed once, cached as `@cached_property` |

The `_build_direct_child_index()` function builds a `{parent_path → child_info}` dict in one pass over all paths. This index is reused for all 646 `_build_topology()` calls instead of re-scanning every time.

---

## Per-Request Throughput (Mock Mode)

### Shared-memory locking

The mock state is backed by a shared-memory segment protected by a filesystem lock (`fcntl.flock`).

| Operation | Before | After |
|---|---|---|
| Read (GET) | `LOCK_EX` — serialises all readers | `LOCK_SH` — concurrent reads allowed |
| Write (POST/PUT/DELETE) | `LOCK_EX` | `LOCK_EX` (unchanged) |

Concurrent GET requests no longer block each other.

### Deleted-item tracking

The set of deleted keys was stored as a JSON list (O(n) membership checks). It is now materialised as a Python `set` during each request (O(1) checks) and serialised back to a list only when writing state.

---

## SDK Hot Paths

### URL construction (`https.py`)

`_url_for()` is called on every API request to join the base URL with the request path. Previously it re-parsed `self._base_url` with `urlsplit`/`urlunsplit` on every call.

Now the components `(scheme, netloc, base_path)` are parsed once in `__init__` and reused:

```python
# __init__
_parsed = urlsplit(self._base_url)
self._base_scheme = _parsed.scheme
self._base_netloc = _parsed.netloc
self._base_path = _parsed.path or "/"

# _url_for (called per-request)
joined = posixpath.join(self._base_path, path.lstrip("/"))
return urlunsplit((self._base_scheme, self._base_netloc, joined, "", ""))
```

`posixpath` is now a top-level module import instead of a deferred `import posixpath` inside the method.

### Path joining (`resource.py`)

`_url_join()` is called on every attribute navigation step (`proxmox.nodes`, `.qemu`, etc.). A fast path now avoids `urlsplit`/`urlunsplit` for plain path strings (no `://`), which is the common case for SDK usage:

```python
def _url_join(base: str, *args: str) -> str:
    if "://" not in base:
        return posixpath.join(base or "/", *[str(a) for a in args])
    # full URL parsing only for absolute URLs
    ...
```

### None filtering (`resource.py`)

`_filter_none()` is called once per HTTP method to strip `None` values from params/data dicts. A fast path skips the dict comprehension when no `None` values are present (common for well-formed requests):

```python
def _filter_none(d: dict) -> dict:
    if all(v is not None for v in d.values()):
        return d  # avoid allocation
    return {k: v for k, v in d.items() if v is not None}
```

---

## Task Polling

`Tasks.blocking_status()` previously polled at a fixed interval (2 s), which means:

- Short tasks were checked 2 s late on average.
- Long tasks (VM migrations, backups) generated many unnecessary API calls.

It now uses **exponential backoff**:

```
1s → 2s → 4s → 8s → 16s → 30s (cap)
```

Timeout tracking uses `time.monotonic()` for accurate wall-clock measurement instead of cumulative addition (which underestimates actual elapsed time by the duration of each HTTP request).

---

## Config Loading

`ProxmoxConfig.from_env()` previously copied the entire `os.environ` dict (50–200+ keys) on every call. It now reads only the ~20 specific keys it needs:

```python
_KEYS = (
    "PROXMOX_API_MODE", "PROXMOX_API_URL", "PROXMOX_API_TOKEN_ID", ...
)
env_config = {k: v for k in _KEYS if (v := os.environ.get(k)) is not None}
```

`yaml` (PyYAML) is only imported when a YAML config file is actually present, avoiding a heavy import on every startup.

---

## Dead Code Removed

`mock/schema_helpers.py` previously contained ~200 lines of private functions (`_seed_int`, `_field_hint`, `_semantic_string_value`, etc.) that duplicated the same logic inside `ProxmoxSchemaValue` in `schema.py`. None of the module's public functions called these copies — they all delegated directly to `ProxmoxSchemaValue`. The dead code was removed, reducing module load time and memory footprint.

---

## Regex Pre-compilation

The pattern `r"(^|_)name$"` used in semantic mock value generation was previously compiled on every call via `re.search(pattern, hint)`. It is now compiled once at module load:

```python
_RE_NAME_HINT = re.compile(r"(^|_)name$")
```

---

## Performance Characteristics (Updated)

### Mock Mode

| Metric | Value |
|---|---|
| Startup (schema load + route registration) | ~1 s |
| Request latency (in-memory, no lock contention) | < 5 ms |
| Concurrent read throughput | Parallel GETs (shared lock) |
| Memory (schema + state) | ~100 MB |

### Real Mode

| Metric | Value |
|---|---|
| Startup | ~500 ms |
| Request latency | Proxmox latency + ~10–20 ms validation overhead |
| Memory | ~80 MB |

### SDK

| Operation | Notes |
|---|---|
| First request | One SSL context build + one session open |
| Subsequent requests | Connection reused from aiohttp pool |
| Ticket renewal | Automatic, uses same SSL context as API requests |
| Task polling | Exponential backoff, accurate monotonic timeout |

---

## Profiling Tips

To measure startup time:

```bash
python -c "
import time
t0 = time.perf_counter()
from proxmox_openapi.main import app
print(f'app ready in {time.perf_counter() - t0:.3f}s')
"
```

To measure mock route registration specifically:

```bash
python -c "
import time, json
from proxmox_openapi.mock.routes import register_generated_proxmox_mock_routes
from proxmox_openapi.schema import load_proxmox_generated_openapi
from fastapi import FastAPI

doc = load_proxmox_generated_openapi()
app = FastAPI()
t0 = time.perf_counter()
register_generated_proxmox_mock_routes(app, openapi_document=doc)
print(f'route registration: {time.perf_counter() - t0:.3f}s')
"
```

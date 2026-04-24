# proxmox-sdk Agent Index

## Overview

`proxmox-sdk` is a schema-driven FastAPI package for Proxmox API that provides:

1. **Dual-mode operation** - Mock mode (default, in-memory CRUD) or Real mode (proxy to actual Proxmox)
2. **Standalone Python SDK** - Production-ready SDK without FastAPI server (async + sync)
3. **CLI + TUI** - Typer CLI and Textual terminal UI for interactive use
4. **Codegen pipeline** - Automatically crawl Proxmox API Viewer and convert to OpenAPI schema
5. **646 endpoints** - Pre-generated Proxmox VE 8.1 API with full OpenAPI schema
6. **Rate limiting** - Built-in protection via SlowAPI

## Package Structure

```
proxmox_sdk/
├── __init__.py               # Package exports and public API
├── main.py                   # Full API server (mock OR real mode)
├── mock_main.py              # Standalone mock-only server entrypoint
├── schema.py                 # Schema management (load/save OpenAPI)
├── rate_limit.py             # SlowAPI rate limiting configuration
├── exception.py              # Exception classes
├── logger.py                 # Logging utilities
├── routes/
│   ├── codegen.py            # Code generation endpoints (protected)
│   ├── mock.py               # Mock route handlers
│   └── versions.py           # Version management endpoints
├── proxmox/                  # Real API proxy
│   ├── routes.py             # Proxmox API proxy routes with validation
│   ├── config.py             # ProxmoxConfig dataclass
│   └── client.py             # FastAPI adapter wrapping the SDK HTTPS backend
├── proxmox_cli/              # CLI + TUI application
│   ├── app.py                # Typer app construction and setup_logging
│   ├── batch.py              # Batch request execution
│   ├── cache.py              # Response caching layer
│   ├── cli.py                # CLI entrypoint (proxmox, pbx, proxmox-cli)
│   ├── completion.py         # Shell completion helpers
│   ├── config.py             # Config file management
│   ├── config_commands.py    # `config` subcommand group
│   ├── doc_commands.py       # `docs` subcommand group
│   ├── docgen_capture.py     # CLI docs capture pipeline
│   ├── error_suggestions.py  # User-friendly error hints
│   ├── exceptions.py         # CLI-specific exceptions
│   ├── install.py            # Self-install helpers
│   ├── output.py             # Shared output formatting
│   ├── performance.py        # Performance profiling helpers
│   ├── release.py            # Release tooling
│   ├── sdk_bridge.py         # Bridge between CLI and ProxmoxSDK
│   ├── tui_app.py            # Textual TUI application
│   ├── tui_runner.py         # TUI launch wrapper
│   ├── utils.py              # Path/param parsing utilities
│   ├── commands/             # Subcommands
│   │   ├── _common.py        # Shared command utilities
│   │   ├── create.py         # `create` subcommand
│   │   ├── delete.py         # `delete` subcommand
│   │   ├── get.py            # `get` subcommand
│   │   ├── help.py           # `help` subcommand
│   │   ├── ls.py             # `ls` subcommand
│   │   ├── set.py            # `set` subcommand
│   │   ├── tui.py            # `tui` subcommand
│   │   └── usage.py          # `usage` subcommand
│   ├── docgen/               # CLI docs generation
│   │   ├── discovery.py      # Command discovery
│   │   ├── engine.py         # Doc generation engine
│   │   ├── models.py         # Doc data models
│   │   └── specs.py          # OpenAPI spec helpers
│   ├── plugins/              # Plugin extension point
│   └── themes/               # TUI themes
├── proxmox_codegen/          # Proxmox API Viewer crawler
│   ├── apidoc_parser.py      # Parse Proxmox apidoc.js
│   ├── crawler.py            # Playwright-based crawler
│   ├── normalize.py          # Normalize captured endpoints
│   ├── openapi_generator.py # Generate OpenAPI schema
│   ├── pydantic_generator.py # Generate Pydantic models
│   ├── pipeline.py           # Generation pipeline orchestration
│   ├── security.py           # SSRF protection, URL validation
│   ├── models.py
│   ├── utils.py
│   └── cli.py                # Codegen CLI commands
├── sdk/                      # Standalone Python SDK
│   ├── api.py                # ProxmoxSDK main class
│   ├── sync.py               # SyncProxmoxSDK wrapper
│   ├── resource.py           # Resource navigation (attribute-based)
│   ├── services.py           # Service configs (PVE, PMG, PBS)
│   ├── exceptions.py         # SDK-specific exceptions
│   ├── backends/             # Transport backends
│   │   ├── base.py           # AbstractBackend protocol
│   │   ├── _cli_base.py      # Shared base for pvesh/openssh CLI backends
│   │   ├── https.py          # aiohttp HTTPS backend (default)
│   │   ├── mock.py           # In-memory mock backend
│   │   ├── local.py          # Local pvesh CLI backend
│   │   ├── ssh_paramiko.py   # SSH via Paramiko
│   │   └── openssh.py        # SSH via openssh-wrapper
│   ├── auth/                 # Authentication handlers
│   │   ├── base.py           # BaseAuth abstract protocol
│   │   ├── token.py          # API token auth
│   │   └── ticket.py         # Password/ticket auth + TOTP
│   └── tools/                # Helper tools
│       ├── files.py          # File upload/download
│       └── tasks.py          # Task monitoring
└── mock/                     # Mock API implementation
    ├── app.py                # Mock FastAPI app
    ├── routes.py             # Dynamic route registration with CRUD
    ├── state.py              # SharedMemoryMockStore (in-memory persistence)
    ├── schema_helpers.py     # Mock value generation
    └── loader.py             # Mock data loading from JSON/YAML
```

## Required Checks

```bash
# Install dependencies
uv sync

# Install git hooks (one-time setup)
uv run pre-commit install --hook-type pre-commit --hook-type pre-push

# Run pre-commit checks (required before commit and push)
uv run pre-commit run --all-files

# Run linting
ruff check .
ruff format --check .

# Compile package
uv run python -m compileall proxmox_sdk

# Test core imports
uv run python -c "import proxmox_sdk.main"
uv run python -c "import proxmox_sdk.mock_main"

# Test SDK imports
uv run python -c "from proxmox_sdk.sdk import ProxmoxSDK"
uv run python -c "from proxmox_sdk.sdk.sync import SyncProxmoxSDK"

# Test CLI imports
uv run python -c "from proxmox_sdk.proxmox_cli.cli import cli"

# Run tests
pytest
```

## Security Controls

See [docs/security.md](docs/security.md) for the full reference. Key patterns to follow:

- **SSRF protection** — All user-supplied URLs must be passed through `validate_source_url()` in `proxmox_codegen/security.py` before any outbound request. Non-Proxmox domains are blocked by default (`allow_any_domain=False`). Private IPv4, private IPv6, IPv4-mapped IPv6 (`::ffff:`), and 6to4 addresses are all blocked.
- **Codegen auth** — `POST /codegen/generate` and related endpoints require a `Bearer` token via `CODEGEN_API_KEY`. Rate-limited to 1 req/hour.
- **CORS** — Disabled by default. Enable via `CORS_ORIGINS`. Allowed headers are restricted to `Content-Type`, `Authorization`, `X-Requested-With`. Wildcards are never used.
- **Health endpoint** — Returns `404` for non-localhost callers. `testclient` is only added to the allowlist when `TESTING=1`.
- **SSH backends** — `SshParamikoBackend` defaults to `WarningPolicy` (not `AutoAddPolicy`). All SSH commands use `shlex.join()`/`shlex.quote()` to prevent shell injection. Temp files use `secrets.token_hex(8)`.
- **Log sanitization** — `SensitiveDataFilter` in `logger.py` redacts credentials (`password=`, `token_value=`, `PVEAuthCookie=`, `CSRFPreventionToken=`, `Authorization=`) from all log output.
- **Credential clearing** — `PROXMOX_API_TOKEN_SECRET`, `PROXMOX_API_PASSWORD`, `PROXMOX_API_OTP` are overwritten with `"********"` in `os.environ` after being read.
- **Config symlink protection** — `save_config()` refuses to write if the config file or its parent directory is a symlink.
- **SSL context** — `TicketAuth` receives the same `ssl` context as the main HTTPS backend, so `verify_ssl=False` applies consistently to both auth and API requests.
- **Proxy threading** — `TicketAuth._request_ticket()` forwards `proxy=` to `session.post()` so authentication requests go through the same proxy as all other API calls. Omitting this would cause auth to bypass the proxy in proxy-only networks.

## Performance Patterns

See [docs/performance.md](docs/performance.md) for the full reference. Key patterns to be aware of:

- **Lazy package imports** — `proxmox_sdk/__init__.py` uses `__getattr__` to defer app construction. `import proxmox_sdk` alone does not build any FastAPI app.
- **Route registration** — `_build_direct_child_index()` in `mock/routes.py` builds a `{parent→child}` index in one O(P) pass before the registration loop, avoiding O(P²) re-scanning.
- **Schema fingerprint** — `ProxmoxSchemaValue.fingerprint` is a `@cached_property`; the JSON hash is computed once per object.
- **Shared read locks** — Mock state reads use `LOCK_SH` (shared); only writes use `LOCK_EX`. Concurrent GETs no longer block each other.
- **Deleted-item set** — Mock `state["deleted"]` is materialised as a Python `set` during each request for O(1) membership checks; serialised back to `list` on write.
- **URL construction** — `HttpsBackend` caches `(scheme, netloc, base_path)` in `__init__`; `_url_for()` uses `posixpath.join` with cached components instead of calling `urlsplit` on every request.
- **Path joining fast path** — `_url_join()` in `resource.py` skips `urlsplit`/`urlunsplit` for plain paths (no `://`).
- **None filtering fast path** — `_filter_none()` in `resource.py` returns the original dict unchanged when no `None` values are present.
- **Task polling** — `Tasks.blocking_status()` uses exponential backoff (1s→2s→4s→8s→16s→30s cap) with `time.monotonic()` for accurate timeout tracking.
- **Request retry** — `HttpsBackend.request()` retries GET/HEAD requests on 502/503/504 and transport errors with exponential backoff (base × 2ⁿ, capped at 30s). POST/PUT/DELETE never retry to prevent double-mutation. `max_retries=0` by default keeps existing behaviour.
- **Config loading** — `ProxmoxConfig.from_env()` reads only the ~20 specific env keys it needs. `yaml` is only imported when a YAML config file is present.
- **Regex pre-compilation** — `_RE_NAME_HINT` in `schema.py` is compiled once at module load.

## Commit and Push Policy

Before every `git commit` and every `git push`, run:

```bash
uv run pre-commit run --all-files
```

If any hook fails, fix the issues and rerun until all hooks pass.

## Release Process

A release publishes the package to PyPI and pushes all three Docker image variants (`raw`, `nginx`, `granian`) to Docker Hub with both versioned and `latest` tags.

### Steps

1. **Bump the version** in `pyproject.toml` (`[project] version`). Use PEP 440 — e.g. `0.0.2.post4`, `0.0.3`, `0.1.0`.

2. **Run pre-commit and tests** to confirm the tree is clean:
   ```bash
   uv run pre-commit run --all-files
   uv run pytest
   ```

3. **Commit the version bump**:
   ```bash
   git add pyproject.toml
   git commit -m "chore: bump version to <new-version>"
   ```

4. **Push the commit**:
   ```bash
   git push origin main
   ```

5. **Create and push the annotated tag** (must match `v<pyproject-version>`):
   ```bash
   git tag v<new-version>
   git push origin v<new-version>
   ```

6. **Create the GitHub release** (triggers `publish-testpypi.yml` which publishes to PyPI and Docker Hub):
   ```bash
   gh release create v<new-version> \
     --title "v<new-version>" \
     --notes "Release notes here."
   ```

7. **Update downstream consumers** — bump `proxmox-sdk==<new-version>` in `proxbox-api/pyproject.toml` and any other dependents, commit, and push.

### What CI does on release

`publish-testpypi.yml` runs when a GitHub Release is published:
- Validates that the tag matches `pyproject.toml` version
- Builds and uploads `dist/` to TestPyPI
- Validates the install on Python 3.11, 3.12, 3.13
- Publishes to PyPI (`--skip-existing`)
- Builds and pushes all three Docker images with `<version>` and `latest` tags

`ci.yml` `docker-images` job also fires and pushes the same images via `docker-hub-publish.yml`.

## Key Endpoints

### Core
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /version` - Version info
- `GET /mode` - Current mode (mock/real)
- `GET /docs` - Swagger documentation
- `GET /redoc` - ReDoc documentation

### Codegen (Protected)
- `POST /codegen/generate` - Generate OpenAPI schema from Proxmox API Viewer (requires auth, rate-limited 1/hour)
- `GET /codegen/openapi` - Get generated OpenAPI schema (requires auth)
- `GET /codegen/pydantic` - Get generated Pydantic v2 models (requires auth, rate-limited 5/hour)
- `GET /codegen/versions` - List available versions (requires auth)

### Mock
- `GET /versions/` - List available Proxmox OpenAPI versions
- `GET /mock/openapi` - Mock mode OpenAPI schema
- `POST /mock/reset` - Reset mock data to defaults
- `GET /mock/state` - Get current mock state

## Environment Variables

### Mock Mode (Default)
- `PROXMOX_API_MODE` - Set to "mock" (default) or "real"
- `PROXMOX_MOCK_SCHEMA_VERSION` - Version tag for mock (default: "latest")
- `PROXMOX_MOCK_DATA_PATH` - Path to custom mock data JSON/YAML file

### Real Mode
- `PROXMOX_API_MODE` - Set to "real" to enable Proxmox integration
- `PROXMOX_URL` - Proxmox server URL (e.g., "https://proxmox.example.com:8006")
- `PROXMOX_API_TOKEN` - API token (recommended, format: "PVEAPIToken=user@realm!tokenid=uuid")
- `PROXMOX_USERNAME` - Username (fallback, format: "user@realm")
- `PROXMOX_PASSWORD` - Password (fallback)
- `PROXMOX_API_VERIFY_SSL` - Verify SSL certificates (default: true)

### Connection Tuning
- `PROXMOX_API_TIMEOUT` - Total request timeout in seconds (default: `"5"`)
- `PROXMOX_API_CONNECT_TIMEOUT` - TCP connection timeout in seconds, separate from total (default: unset)
- `PROXMOX_API_RETRIES` - Max retry attempts for GET/HEAD on 502/503/504 or transport errors (default: `"0"`)
- `PROXMOX_API_RETRY_BACKOFF` - Exponential backoff base in seconds for retries (default: `"0.5"`)

### Proxy Configuration
- `HTTP_PROXY` - HTTP proxy URL
- `HTTPS_PROXY` - HTTPS proxy URL
- `PROXMOX_API_HTTP_PROXY` - Override HTTP proxy for SDK
- `PROXMOX_API_HTTPS_PROXY` - Override HTTPS proxy for SDK

### Server
- `HOST` - Host to bind to (default: "0.0.0.0")
- `PORT` - Port to bind to (default: "8000")
- `CORS_ORIGINS` - Comma-separated CORS origins

### Logging
- `LOG_LEVEL` - Logging level (default: "INFO")

### Security / Auth
- `CODEGEN_API_KEY` - Bearer token required for all `/codegen/*` endpoints (`POST /codegen/generate`, `GET /codegen/openapi`, `GET /codegen/pydantic`, `GET /codegen/versions`)
- `TESTING` - Set to `1` or `true` to add `testclient` to the health endpoint's localhost allowlist (test use only)

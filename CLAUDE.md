# proxmox-openapi Agent Index

## Overview

`proxmox-openapi` is a schema-driven FastAPI package for Proxmox API that provides:

1. **Dual-mode operation** - Mock mode (default, in-memory CRUD) or Real mode (proxy to actual Proxmox)
2. **Standalone Python SDK** - Production-ready SDK without FastAPI server (async + sync)
3. **CLI + TUI** - Typer CLI and Textual terminal UI for interactive use
4. **Codegen pipeline** - Automatically crawl Proxmox API Viewer and convert to OpenAPI schema
5. **646 endpoints** - Pre-generated Proxmox VE 8.1 API with full OpenAPI schema
6. **Rate limiting** - Built-in protection via SlowAPI

## Package Structure

```
proxmox_openapi/
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
│   └── config.py             # ProxmoxConfig dataclass
├── proxmox_cli/              # CLI + TUI application
│   ├── cli.py                # Typer CLI entrypoint (proxmox, pbx)
│   ├── commands/             # Subcommands (get, create, set, delete, ls)
│   ├── tui_app.py            # Textual TUI application
│   ├── config.py             # Config file management
│   ├── themes/               # TUI themes
│   └── docgen/               # CLI docs generation
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
│   │   ├── https.py          # aiohttp HTTPS backend (default)
│   │   ├── mock.py           # In-memory mock backend
│   │   ├── local.py          # Local pvesh CLI backend
│   │   ├── ssh_paramiko.py   # SSH via Paramiko
│   │   └── openssh.py        # SSH via openssh-wrapper
│   ├── auth/                 # Authentication handlers
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
uv run python -m compileall proxmox_openapi

# Test core imports
uv run python -c "import proxmox_openapi.main"
uv run python -c "import proxmox_openapi.mock_main"

# Test SDK imports
uv run python -c "from proxmox_openapi.sdk import ProxmoxSDK"
uv run python -c "from proxmox_openapi.sdk.sync import SyncProxmoxSDK"

# Test CLI imports
uv run python -c "from proxmox_openapi.proxmox_cli.cli import cli"

# Run tests
pytest
```

## Commit and Push Policy

Before every `git commit` and every `git push`, run:

```bash
uv run pre-commit run --all-files
```

If any hook fails, fix the issues and rerun until all hooks pass.

## Key Endpoints

### Core
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /version` - Version info
- `GET /mode` - Current mode (mock/real)
- `GET /docs` - Swagger documentation
- `GET /redoc` - ReDoc documentation

### Codegen (Protected)
- `POST /codegen/generate` - Generate OpenAPI schema from Proxmox API Viewer (requires auth)
- `GET /codegen/openapi` - Get generated OpenAPI schema
- `GET /codegen/versions` - List available versions

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

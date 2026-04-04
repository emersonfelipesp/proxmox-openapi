# proxmox-openapi Agent Index

## Overview

`proxmox-openapi` is a standalone FastAPI package that provides:

1. **Crawler of Proxmox API Viewer** - Automatically crawl Proxmox API Viewer and convert to OpenAPI schema
2. **Mock data** - Automatically generate mock data for all endpoints
3. **In-Memory CRUD** - Allow users to modify mock data through create, update, and patch operations
4. **Multi-version Support** - Select multiple Proxmox versions with `latest` mapped to official Proxmox API viewer
5. **Swagger Docs** - FastAPI auto-generates OpenAPI documentation

## Package Structure

```
proxmox_openapi/
├── __init__.py           # Package exports
├── main.py               # Full API server (connects to real Proxmox)
├── mock_main.py          # Standalone mock API server
├── exception.py          # Exception classes
├── logger.py             # Logging utilities
├── schema.py             # Schema management (load/save OpenAPI)
├── routes/
│   ├── codegen.py        # Code generation endpoints
│   ├── mock.py           # Mock route handlers
│   └── versions.py       # Version management endpoints
├── proxmox_codegen/      # Proxmox API Viewer crawler
│   ├── apidoc_parser.py  # Parse Proxmox apidoc.js
│   ├── crawler.py        # Playwright-based crawler
│   ├── normalize.py      # Normalize captured endpoints
│   ├── openapi_generator.py
│   ├── pydantic_generator.py
│   ├── pipeline.py       # Generation pipeline
│   ├── utils.py
│   ├── models.py
│   └── cli.py
└── mock/                 # Mock API implementation
    ├── app.py
    ├── routes.py         # Dynamic route generation with CRUD
    ├── state.py          # Shared-memory in-memory store
    └── schema_helpers.py
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

# Test imports
uv run python -c "import proxmox_openapi.main"
uv run python -c "import proxmox_openapi.mock_main"

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

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /version` - Version info
- `GET /docs` - Swagger documentation
- `POST /codegen/generate` - Generate OpenAPI schema from Proxmox API Viewer
- `GET /codegen/openapi` - Get generated OpenAPI schema
- `GET /codegen/versions` - List available versions
- `GET /versions/` - List available Proxmox OpenAPI versions

## Environment Variables

- `PROXMOX_MOCK_SCHEMA_VERSION` - Specify version tag for mock (default: "latest")
- `PROXMOX_MOCK_DATA_PATH` - Path to custom mock data file (default: "/etc/proxmox-openapi/mock-data.json")
- `HOST` - Host to bind to (default: "0.0.0.0")
- `PORT` - Port to bind to (default: "8000")

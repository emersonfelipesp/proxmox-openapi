# Development Guide

This guide explains how to contribute to the Proxmox OpenAPI project, set up your development environment, and understand the codebase architecture.

## Getting Started

### Prerequisites

- **Python 3.11+** (required)
- **uv** (recommended) or pip
- **Git** for version control
- **Make** (optional, for convenience commands)

### Development Installation

1. **Clone the repository:**

```bash
git clone https://github.com/emersonfelipesp/proxmox-sdk.git
cd proxmox-sdk
```

2. **Install in development mode:**

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e ".[dev]"
```

This installs the package in editable mode with all development dependencies.

3. **Install git hooks (one-time):**

```bash
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

4. **Verify installation:**

```bash
# Check that imports work
python -c "from proxmox_sdk import __version__; print(__version__)"

# Run the server
uvicorn proxmox_sdk.main:app --reload
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Make Your Changes

Edit the code, add tests, update documentation.

### 3. Run Quality Checks

```bash
# Run all pre-commit hooks (required before every commit)
uv run pre-commit run --all-files

# Or run tools individually:
ruff format .
ruff check .
ruff check --fix .
uv run ty check proxmox_sdk tests --output-format concise
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=proxmox_sdk --cov-report=html

# Run specific test file
pytest tests/test_schema.py

# Run with verbose output
pytest -v
```

### 5. Update Documentation

If you changed the API or added features:

```bash
# Build docs locally
mkdocs serve

# View at http://127.0.0.1:8000
```

### 6. Commit and Push

```bash
# Hooks run automatically on commit and push (installed in step 3 above)
git add .
git commit -m "feat: add new feature"
git push origin feature/my-new-feature
```

### 7. Create Pull Request

Open a PR on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots/examples if applicable

## Project Structure

```
proxmox-sdk/
├── proxmox_sdk/                  # Main package
│   ├── __init__.py               # Package exports and public API
│   ├── main.py                   # Full API server (mock OR real mode)
│   ├── mock_main.py              # Standalone mock-only server entrypoint
│   ├── schema.py                 # Schema management (load/save OpenAPI)
│   ├── rate_limit.py             # SlowAPI rate limiting configuration
│   ├── exception.py              # Exception classes
│   ├── logger.py                 # Logging utilities
│   │
│   ├── routes/                   # Management API routes
│   │   ├── codegen.py            # Code generation endpoints (protected)
│   │   ├── helpers.py            # Shared route utilities
│   │   ├── mock.py               # Mock route handlers
│   │   └── versions.py           # Version management endpoints
│   │
│   ├── proxmox/                  # Real API proxy
│   │   ├── config.py             # ProxmoxConfig dataclass
│   │   ├── client.py             # FastAPI adapter wrapping the SDK HTTPS backend
│   │   └── routes.py             # Proxmox API proxy routes with validation
│   │
│   ├── sdk/                      # Standalone Python SDK
│   │   ├── api.py                # ProxmoxSDK main class
│   │   ├── sync.py               # SyncProxmoxSDK wrapper
│   │   ├── resource.py           # Resource navigation (attribute-based)
│   │   ├── services.py           # Service configs (PVE, PMG, PBS)
│   │   ├── exceptions.py         # SDK-specific exceptions
│   │   ├── backends/             # Transport backends
│   │   │   ├── base.py           # AbstractBackend protocol
│   │   │   ├── https.py          # aiohttp HTTPS backend (default)
│   │   │   ├── mock.py           # In-memory mock backend
│   │   │   ├── local.py          # Local pvesh CLI backend
│   │   │   ├── ssh_paramiko.py   # SSH via Paramiko
│   │   │   └── openssh.py        # SSH via openssh-wrapper
│   │   ├── auth/                 # Authentication handlers
│   │   │   ├── base.py           # BaseAuth abstract protocol
│   │   │   ├── token.py          # API token auth
│   │   │   └── ticket.py         # Password/ticket auth + TOTP
│   │   └── tools/                # Helper tools
│   │       ├── files.py          # File upload/download
│   │       └── tasks.py          # Task monitoring
│   │
│   ├── proxmox_cli/              # CLI + TUI application
│   │   ├── cli.py                # CLI entrypoint (proxmox, pbx, proxmox-cli)
│   │   ├── app.py                # Typer app construction and setup_logging
│   │   ├── config.py             # Config file management
│   │   ├── sdk_bridge.py         # Bridge between CLI and ProxmoxSDK
│   │   ├── tui_app.py            # Textual TUI application
│   │   ├── commands/             # Subcommands (get, set, create, delete, ls, …)
│   │   ├── docgen/               # CLI docs generation
│   │   └── themes/               # TUI themes
│   │
│   ├── proxmox_codegen/          # Proxmox API Viewer crawler
│   │   ├── crawler.py            # Playwright-based crawler
│   │   ├── apidoc_parser.py      # Parse Proxmox apidoc.js
│   │   ├── normalize.py          # Normalize captured endpoints
│   │   ├── openapi_generator.py  # Generate OpenAPI schema
│   │   ├── pydantic_generator.py # Generate Pydantic models
│   │   ├── pipeline.py           # Generation pipeline orchestration
│   │   └── security.py           # SSRF protection, URL validation
│   │
│   ├── mock/                     # Mock API implementation
│   │   ├── app.py                # Mock FastAPI app
│   │   ├── routes.py             # Dynamic route registration with CRUD
│   │   ├── state.py              # SharedMemoryMockStore (in-memory)
│   │   ├── schema_helpers.py     # Mock value generation
│   │   └── loader.py             # Mock data loading from JSON/YAML
│   │
│   └── generated/                # Pre-generated schemas (committed)
│       └── proxmox/
│           └── latest/
│               ├── openapi.json        # 5.2MB OpenAPI 3.1 schema
│               └── pydantic_models.py  # Generated Pydantic v2 models
│
├── tests/                        # Test suite
├── docs/                         # MkDocs documentation
├── pyproject.toml                # Project config and dependencies
├── mkdocs.yml                    # Documentation config
├── Dockerfile                    # Container image
├── README.md                     # Main README
└── CLAUDE.md                     # Agent index and contributor guide
```

## Key Modules

### `main.py` — Dual-mode FastAPI app

Serves both mock and real modes. Start it with:

```bash
uvicorn proxmox_sdk.main:app --reload
```

Select mode via `PROXMOX_API_MODE=mock` (default) or `PROXMOX_API_MODE=real`.

### `sdk/api.py` — ProxmoxSDK

The standalone Python SDK class. Supports async, sync, and mock construction:

```python
from proxmox_sdk import ProxmoxSDK

# Async (real Proxmox)
async with ProxmoxSDK(host="pve.example.com", user="root@pam", password="…") as pve:
    nodes = await pve.nodes.get()

# Sync wrapper
with ProxmoxSDK.sync(host="pve.example.com", user="root@pam", password="…") as pve:
    nodes = pve.nodes.get()

# Mock (no Proxmox server needed)
async with ProxmoxSDK.mock() as pve:
    nodes = await pve.nodes.get()

# From environment / config file
config = ProxmoxConfig.from_env()
pve = ProxmoxSDK.from_config(config)
```

### `mock/routes.py` — Mock Route Builder

`register_generated_proxmox_mock_routes()` dynamically generates 646 CRUD endpoints from the bundled OpenAPI schema at startup. Each route operates on `SharedMemoryMockStore`.

### `schema.py` — Schema Utilities

`load_proxmox_schema(version)` loads the pre-generated OpenAPI JSON from `generated/proxmox/<version>/openapi.json`.

## Code Generation Pipeline

The project includes a powerful code generation pipeline that converts the Proxmox API into OpenAPI schemas:

### Architecture

```
Proxmox VE API
      ↓
[1. Crawler] - Fetch API structure
      ↓
raw_capture.json (646 endpoints)
      ↓
[2. Pipeline] - Normalize & enrich
      ↓
normalized data
      ↓
[3. OpenAPI Builder] - Generate OpenAPI schema
      ↓
openapi.json (5.2MB)
      ↓
[4. Pydantic Builder] - Generate models
      ↓
pydantic_models.py
```

### Running Code Generation

```python
from proxmox_sdk.proxmox_codegen import ProxmoxCodegenPipeline

# Initialize pipeline
pipeline = ProxmoxCodegenPipeline(
    proxmox_url="https://proxmox.example.com:8006",
    username="root@pam",
    password="password",
    verify_ssl=False,
)

# Run full pipeline
await pipeline.run_full_pipeline(
    output_dir="./output",
    version_tag="8.1",
)

# Output:
# - output/raw_capture.json
# - output/openapi.json
# - output/pydantic_models.py
```

## Testing

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_schema.py           # Schema loading
├── test_mock_routes.py      # Mock CRUD operations
├── test_main_app.py         # App startup, mode switching
├── test_proxmox_client.py   # Real API client (mocked)
├── test_codegen.py          # Code generation pipeline
└── test_custom_mock_data.py # Custom data loading
```

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient
from proxmox_sdk.main import app

def test_version_endpoint():
    """Test /version endpoint."""
    client = TestClient(app)
    response = client.get("/version")

    assert response.status_code == 200
    data = response.json()
    assert "version" in data

@pytest.mark.asyncio
async def test_proxmox_client_auth(mock_proxmox_server):
    """Test ProxmoxClient authentication."""
    from proxmox_sdk.proxmox import ProxmoxClient, ProxmoxConfig

    config = ProxmoxConfig(
        url=mock_proxmox_server.url,
        api_token="test-token",
    )

    client = ProxmoxClient(config)
    result = await client.request("GET", "/version")

    assert result["version"] == "8.1"
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=proxmox_sdk --cov-report=html
open htmlcov/index.html

# Specific module
pytest tests/test_mock_routes.py

# With markers
pytest -m "not slow"

# Verbose
pytest -vv

# Stop on first failure
pytest -x
```

## Code Style

We use **Ruff** for linting and formatting:

```bash
# Format all code
ruff format .

# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Style Rules

- Line length: 100 characters
- Indentation: 4 spaces
- Quotes: Double quotes for strings
- Imports: Sorted and grouped (standard lib, third-party, local)
- Type hints: Required for function signatures
- Docstrings: Required for public functions/classes (Google style)

### Example

```python
"""Module description."""

from proxmox_sdk import ProxmoxSDK
from proxmox_sdk.proxmox.config import ProxmoxConfig


async def get_cluster_nodes(config: ProxmoxConfig) -> list[dict]:
    """
    Return a list of nodes from the Proxmox cluster.

    Args:
        config: A ProxmoxConfig loaded from environment variables.

    Returns:
        List of node dicts from the Proxmox API.
    """
    async with ProxmoxSDK.from_config(config) as pve:
        return await pve.nodes.get()
```

## Documentation

We use **MkDocs Material** for documentation:

```bash
# Serve docs locally
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Writing Docs

- Use Markdown
- Add code examples
- Include links to related pages
- Keep language clear and concise

## Pull Request Guidelines

### Before Submitting

- ✅ All tests pass (`uv run pytest`)
- ✅ All pre-commit hooks pass (`uv run pre-commit run --all-files`)
- ✅ Documentation updated if needed
- ✅ Commit messages follow convention

### Commit Message Format

```
type(scope): short description

Longer description if needed.

Fixes #123
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style (formatting, no logic change)
- `refactor` - Code restructuring (no behavior change)
- `perf` - Performance improvement
- `test` - Add/update tests
- `chore` - Maintenance (dependencies, config)

**Examples:**
```
feat(mock): add custom mock data loader

Add support for loading custom mock data from JSON/YAML files.
Users can now provide their own test data via PROXMOX_MOCK_DATA_PATH.

Fixes #45
```

```
fix(client): handle connection timeout properly

ProxmoxClient now catches aiohttp.ClientTimeout and returns
proper 504 Gateway Timeout response.
```

## Release Process

1. **Bump the version** in `pyproject.toml` (`[project] version`). Use PEP 440 — e.g. `0.0.3`, `0.0.3.post1`, `0.1.0`.
2. **Run pre-commit and tests** to confirm the tree is clean:
   ```bash
   uv run pre-commit run --all-files
   uv run pytest
   ```
3. **Commit the version bump:**
   ```bash
   git add pyproject.toml
   git commit -m "chore: bump version to <new-version>"
   git push origin main
   ```
4. **Create and push an annotated tag** (must match `v<pyproject-version>`):
   ```bash
   git tag v<new-version>
   git push origin v<new-version>
   ```
5. **Create the GitHub release** (triggers CI to publish to PyPI and Docker Hub):
   ```bash
   gh release create v<new-version> \
     --title "v<new-version>" \
     --notes "Release notes here."
   ```

## Getting Help

- **Issues:** https://github.com/emersonfelipesp/proxmox-sdk/issues
- **Discussions:** https://github.com/emersonfelipesp/proxmox-sdk/discussions
- **Documentation:** https://emersonfelipesp.github.io/proxmox-sdk/

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/emersonfelipesp/proxmox-sdk/blob/main/LICENSE) file for details.

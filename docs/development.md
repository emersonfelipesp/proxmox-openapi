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
git clone https://github.com/emersonfelipesp/proxmox-openapi.git
cd proxmox-openapi
```

2. **Install in development mode:**

```bash
# Using uv (recommended)
uv pip install -e ".[dev]"

# Or using pip
pip install -e ".[dev]"
```

This installs the package in editable mode with all development dependencies.

3. **Verify installation:**

```bash
# Check that imports work
python -c "from proxmox_openapi import __version__; print(__version__)"

# Run the server
uvicorn proxmox_openapi.main:app --reload
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
# Format code
ruff format .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Type checking
uv run ty check proxmox_openapi tests --output-format concise
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=proxmox_openapi --cov-report=html

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
proxmox-openapi/
├── proxmox_openapi/           # Main package
│   ├── __init__.py           # Package metadata
│   ├── main.py               # Main FastAPI app (with mode switching)
│   ├── mock_main.py          # Mock-only standalone app
│   ├── schema.py             # Schema loading utilities
│   │
│   ├── mock/                 # Mock API implementation
│   │   ├── __init__.py
│   │   ├── app.py           # Mock app builder
│   │   ├── routes.py        # Mock route registration
│   │   ├── state.py         # In-memory state management
│   │   └── loader.py        # Custom mock data loader
│   │
│   ├── proxmox/             # Real Proxmox API implementation
│   │   ├── __init__.py
│   │   ├── config.py        # ProxmoxConfig class
│   │   ├── client.py        # ProxmoxClient (aiohttp)
│   │   └── routes.py        # Real API route registration
│   │
│   ├── routes/              # Management API routes
│   │   ├── __init__.py
│   │   ├── codegen.py       # Code generation endpoints
│   │   └── schema.py        # Schema inspection endpoints
│   │
│   ├── proxmox_codegen/     # OpenAPI generation pipeline
│   │   ├── __init__.py
│   │   ├── crawler.py       # Proxmox API crawler
│   │   ├── pipeline.py      # Generation orchestration
│   │   ├── openapi_builder.py  # OpenAPI schema builder
│   │   └── pydantic_builder.py # Pydantic model generator
│   │
│   └── generated/           # Pre-generated schemas
│       └── proxmox/
│           └── latest/      # Current version (8.1)
│               ├── openapi.json        # 5.2MB OpenAPI schema
│               ├── pydantic_models.py  # Generated models
│               └── raw_capture.json    # Crawler output
│
├── tests/                   # Test suite
│   ├── conftest.py         # Pytest fixtures
│   ├── test_schema.py      # Schema loading tests
│   ├── test_mock_routes.py # Mock CRUD tests
│   ├── test_main_app.py    # Main app tests
│   └── ...
│
├── docs/                    # MkDocs documentation
│   ├── index.md
│   ├── installation.md
│   ├── quickstart.md
│   └── ...
│
├── examples/                # Usage examples
│   ├── mock-data-example.json
│   └── docker-compose.yml
│
├── pyproject.toml          # Project config, dependencies
├── mkdocs.yml             # Documentation config
├── Dockerfile             # Container image
├── README.md              # Main README
└── CLAUDE.md              # AI agent documentation
```

## Key Modules

### `main.py` - Main Application

The central FastAPI app that supports both mock and real modes:

```python
from fastapi import FastAPI
from proxmox_openapi import __version__
from proxmox_openapi.proxmox.config import ProxmoxConfig

config = ProxmoxConfig()
app = FastAPI(title="Proxmox OpenAPI", version=__version__)

if config.mode == "real":
    # Load real Proxmox routes
    from proxmox_openapi.proxmox.routes import register_proxmox_routes
    register_proxmox_routes(app, config)
else:
    # Load mock routes (default)
    from proxmox_openapi.mock.routes import register_generated_proxmox_mock_routes
    register_generated_proxmox_mock_routes(app, "latest")
```

### `mock/routes.py` - Mock Route Builder

Dynamically generates CRUD endpoints from OpenAPI schema:

```python
def register_generated_proxmox_mock_routes(
    app: FastAPI,
    version: str = "latest",
    mock_data_path: str | None = None,
) -> None:
    """Register all mock routes from pre-generated schema."""
    # Load schema
    schema = load_proxmox_schema(version)

    # Create in-memory state
    state = MockState()

    # Load custom data if provided
    if mock_data_path:
        load_custom_mock_data(state, mock_data_path)

    # Generate routes for each endpoint
    for path, methods in schema["paths"].items():
        for method, operation in methods.items():
            create_mock_endpoint(app, state, method, path, operation)
```

### `proxmox/client.py` - Real API Client

aiohttp-based client with authentication and validation:

```python
class ProxmoxClient:
    """Client for real Proxmox VE API."""

    async def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json: dict | None = None,
    ) -> dict:
        """Make authenticated request to Proxmox API."""
        # Build URL
        url = f"{self.config.url}/api2/json{path}"

        # Add auth headers
        headers = await self._get_auth_headers()

        # Make request
        async with self.session.request(
            method, url, headers=headers, params=params, json=json
        ) as response:
            response.raise_for_status()
            return await response.json()
```

### `schema.py` - Schema Utilities

Schema loading and validation:

```python
def load_proxmox_schema(version: str = "latest") -> dict:
    """Load pre-generated Proxmox OpenAPI schema."""
    schema_path = (
        Path(__file__).parent
        / "generated"
        / "proxmox"
        / version
        / "openapi.json"
    )

    with open(schema_path) as f:
        return json.load(f)
```

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
from proxmox_openapi.proxmox_codegen import ProxmoxCodegenPipeline

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
from proxmox_openapi.main import app

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
    from proxmox_openapi.proxmox import ProxmoxClient, ProxmoxConfig

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
pytest --cov=proxmox_openapi --cov-report=html
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

from typing import Any

from fastapi import FastAPI

from proxmox_openapi.schema import load_proxmox_schema


def create_app(version: str = "latest") -> FastAPI:
    """
    Create and configure FastAPI application.

    Args:
        version: Proxmox API version to load.

    Returns:
        Configured FastAPI app instance.
    """
    app = FastAPI(title="Proxmox OpenAPI", version=version)
    schema = load_proxmox_schema(version)
    return app
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

- ✅ All tests pass
- ✅ Code formatted with `ruff format`
- ✅ No linting errors (`ruff check`)
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

1. **Update version** in `proxmox_openapi/__init__.py`
2. **Update CHANGELOG.md** with release notes
3. **Create git tag:**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. **GitHub Actions** automatically publishes to PyPI

## Getting Help

- **Issues:** https://github.com/emersonfelipesp/proxmox-openapi/issues
- **Discussions:** https://github.com/emersonfelipesp/proxmox-openapi/discussions
- **Documentation:** https://emersonfelipesp.github.io/proxmox-openapi/

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/emersonfelipesp/proxmox-openapi/blob/main/LICENSE) file for details.

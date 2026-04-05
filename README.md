# proxmox-openapi

Schema-driven FastAPI package for Proxmox API: OpenAPI generation, mock data, and in-memory CRUD operations.

**📚 [Full Documentation](https://emersonfelipesp.github.io/proxmox-openapi/)**

## Features

- **Dual Mode**: Mock mode (default) for development, Real mode for production Proxmox integration
- **646 Endpoints**: Pre-generated Proxmox VE 8.1 API with full OpenAPI schema
- **Mock Data**: Automatically generate mock data for all endpoints with in-memory CRUD
- **Real API Proxy**: Validated proxy to real Proxmox VE API with request/response validation
- **Code Generation**: Automatically crawl Proxmox API Viewer and convert to OpenAPI schema
- **Multi-version Support**: Select multiple Proxmox versions with `latest` mapped to official Proxmox API viewer
- **Swagger Docs**: FastAPI auto-generates OpenAPI documentation at `/docs`

## Installation

```bash
pip install proxmox-openapi
```

## Quick Start

### Mock Mode (Default)

```bash
# Install
pip install proxmox-openapi

# Start server
uvicorn proxmox_openapi.main:app --reload

# View Swagger docs
# Open http://localhost:8000/docs
```

### SDK Direct Usage (No Server Required)

```python
from proxmox_openapi.sdk import ProxmoxSDK

# Async with mock data
async with ProxmoxSDK.mock() as proxmox:
    nodes = await proxmox.nodes.get()

# Or sync (blocking)
with ProxmoxSDK.sync_mock() as proxmox:
    nodes = proxmox.nodes.get()
```

### CLI TUI

```bash
# Install with CLI extras
pip install proxmox-openapi[cli]

# Production TUI
pbx tui

# Mock TUI
pbx tui mock
```

### Real Mode (Connect to Proxmox)

```bash
# Configure credentials
export PROXMOX_API_MODE=real
export PROXMOX_URL=https://proxmox.example.com:8006
export PROXMOX_API_TOKEN=PVEAPIToken=user@realm!tokenid=uuid

# Start server
uvicorn proxmox_openapi.main:app --reload
```

See the [Quick Start Guide](https://emersonfelipesp.github.io/proxmox-openapi/quickstart/) for more details.

## Documentation

- **[Home](https://emersonfelipesp.github.io/proxmox-openapi/)** - Overview and features
- **[Installation](https://emersonfelipesp.github.io/proxmox-openapi/installation/)** - Installation options (pip, uv, Docker, source)
- **[Quick Start](https://emersonfelipesp.github.io/proxmox-openapi/quickstart/)** - 5-minute getting started guide
- **[SDK Mock Usage](https://emersonfelipesp.github.io/proxmox-openapi/sdk-mock/)** - Using the SDK with mock data (no server required)
- **[Mock API](https://emersonfelipesp.github.io/proxmox-openapi/mock-api/)** - Mock mode guide with custom data
- **[Real API](https://emersonfelipesp.github.io/proxmox-openapi/real-api/)** - Real Proxmox integration guide
- **[API Reference](https://emersonfelipesp.github.io/proxmox-openapi/api-reference/)** - Endpoint documentation
- **[Development](https://emersonfelipesp.github.io/proxmox-openapi/development/)** - Contributing guide
- **[Architecture](https://emersonfelipesp.github.io/proxmox-openapi/architecture/)** - How it works internally
- **[FAQ](https://emersonfelipesp.github.io/proxmox-openapi/faq/)** - Frequently asked questions

## Environment Variables

### Mock Mode
- `PROXMOX_API_MODE` - Set to "mock" (default) or "real"
- `PROXMOX_MOCK_SCHEMA_VERSION` - Version tag to use (default: "latest")
- `PROXMOX_MOCK_DATA_PATH` - Path to custom mock data file (default: "/etc/proxmox-openapi/mock-data.json")

### Real Mode
- `PROXMOX_API_MODE` - Set to "real" to enable Proxmox integration
- `PROXMOX_URL` - Proxmox server URL (e.g., "https://proxmox.example.com:8006")
- `PROXMOX_API_TOKEN` - API token (recommended, format: "PVEAPIToken=user@realm!tokenid=uuid")
- `PROXMOX_USERNAME` - Username (fallback, format: "user@realm")
- `PROXMOX_PASSWORD` - Password (fallback)
- `PROXMOX_API_VERIFY_SSL` - Verify SSL certificates (default: true)

### Server
- `HOST` - Host to bind to (default: "0.0.0.0")
- `PORT` - Port to bind to (default: "8000")

## Development

```bash
# Install dependencies
uv sync --extra test

# Run tests
pytest

# Run linting
ruff check .
ruff format --check .
```

## Docker

```bash
# Build the image
docker build -t proxmox-openapi .

# Run the container
docker run -p 8000:8000 proxmox-openapi
```

## License

MIT

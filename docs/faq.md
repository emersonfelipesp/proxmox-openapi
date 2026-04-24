# FAQ

Frequently Asked Questions about the Proxmox OpenAPI server.

## General Questions

### What is Proxmox OpenAPI?

Proxmox OpenAPI is a FastAPI-based server that provides two modes:

1. **Mock Mode** - In-memory Proxmox VE API simulator with 646 endpoints for development and testing
2. **Real Mode** - Validated proxy to a real Proxmox VE API with full request/response validation

It's designed to help developers build, test, and integrate with Proxmox infrastructure without requiring a live Proxmox cluster for every development task.

### Do I need a Proxmox server to use this?

**No!** The default mock mode works completely standalone with no Proxmox server required. It's perfect for:

- Development and testing
- CI/CD pipelines
- Learning the Proxmox API
- Building integrations before deploying

If you want to connect to a real Proxmox server, switch to real mode by setting `PROXMOX_API_MODE=real`.

### What Proxmox VE version is supported?

The current schema is based on **Proxmox VE 8.1**, but it should work with:

- ✅ **Proxmox VE 8.x** (fully supported)
- ✅ **Proxmox VE 7.x** (mostly compatible)
- ⚠️ **Proxmox VE 6.x** (some endpoints may differ)

You can regenerate schemas for different versions using the code generation pipeline.

### Is this an official Proxmox project?

**No.** This is an independent, community-driven project. It's not affiliated with or endorsed by Proxmox Server Solutions GmbH.

The project uses publicly available Proxmox VE API documentation and generates OpenAPI schemas from live API exploration.

### Can I use this in production?

**Yes**, but with considerations:

- **Mock mode:** Only for development/testing (data is in-memory and not persistent)
- **Real mode:** Yes, but it adds a validation layer between clients and Proxmox. Consider:
  - Additional latency (~20-100ms)
  - Single point of failure (if the proxy goes down)
  - Security: The proxy needs Proxmox credentials

For production, consider whether you need the validation/proxy layer, or if direct Proxmox API access is better for your use case.

## Installation & Setup

### How do I install it?

```bash
# Using pip
pip install proxmox-sdk

# Using uv (recommended)
uv pip install proxmox-sdk

# From source
git clone https://github.com/emersonfelipesp/proxmox-sdk.git
cd proxmox-sdk
uv pip install -e .
```

See the [Installation Guide](installation.md) for more details.

### How do I run the server?

```bash
# Default (mock mode)
uvicorn proxmox_sdk.main:app --reload

# Real mode
export PROXMOX_API_MODE=real
export PROXMOX_API_URL=https://proxmox.example.com:8006
export PROXMOX_API_TOKEN_ID=user@realm!tokenid
export PROXMOX_API_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
uvicorn proxmox_sdk.main:app --reload
```

See the [Quick Start Guide](quickstart.md) for more details.

### What are the system requirements?

- **Python:** 3.11 or later (required)
- **Memory:** ~100MB (mock) or ~80MB (real)
- **Disk:** ~50MB installed
- **OS:** Linux, macOS, Windows (any platform with Python support)

## Mock Mode

### What is mock mode?

Mock mode provides an in-memory simulation of the Proxmox VE API. It:

- Loads 646 pre-generated endpoints from OpenAPI schema
- Provides full CRUD operations (Create, Read, Update, Delete)
- Stores data in memory (resets on restart)
- Requires no Proxmox server

Perfect for development, testing, and CI/CD pipelines.

### Can I customize the mock data?

**Yes!** You can load custom test data from JSON or YAML files:

```bash
export PROXMOX_MOCK_DATA_PATH=/path/to/custom-data.json
uvicorn proxmox_sdk.main:app --reload
```

See the [Mock API Guide](mock-api.md#custom-mock-data) for data format examples.

### Does mock data persist across restarts?

**No.** Mock mode uses in-memory storage, so all data is lost when the server stops.

If you need persistent mock data:
- Use custom mock data files (loaded on startup)
- Consider contributing a database-backed mode (future feature)

### Can I use mock mode in CI/CD?

**Absolutely!** Mock mode is perfect for CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Start Proxmox Mock API
  run: |
    uvicorn proxmox_sdk.main:app &
    sleep 2  # Wait for startup

- name: Run integration tests
  run: pytest tests/integration/
```

No external dependencies, fast startup, predictable behavior.

## Real Mode

### How do I connect to a real Proxmox server?

Set these environment variables:

```bash
export PROXMOX_API_MODE=real
export PROXMOX_API_URL=https://proxmox.example.com:8006
export PROXMOX_API_TOKEN_ID=user@realm!tokenid        # Recommended
export PROXMOX_API_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# OR use username/password
export PROXMOX_API_USERNAME=root@pam
export PROXMOX_API_PASSWORD=your-password
```

Then start the server:

```bash
uvicorn proxmox_sdk.main:app --reload
```

See the [Real API Guide](real-api.md) for full details.

### Should I use API tokens or username/password?

**Use API tokens** (recommended):

- More secure (scoped permissions)
- No password exposure
- Can be revoked individually
- Auditable

Username/password is provided as a fallback for legacy setups.

### How do I disable SSL verification?

```bash
export PROXMOX_API_VERIFY_SSL=false
```

**Warning:** Only use this for development/testing with self-signed certificates. Never disable SSL verification in production.

### What happens if the Proxmox server is down?

The proxy will return a `503 Service Unavailable` error when it cannot reach the Proxmox server.

Your application should handle this gracefully with retry logic or fallback behavior.

### Does real mode cache responses?

**No.** Every request is forwarded to the Proxmox API in real-time. This ensures you always get the latest data but adds latency.

Future versions may add optional caching for read-only operations.

## API Usage

### How do I authenticate with the API?

It depends on the mode:

**Mock Mode (Default):**
- No authentication required by default
- You can add custom auth middleware if needed

**Real Mode:**
- Automatically authenticates with Proxmox using your configured credentials
- Clients just call the proxy endpoints (no need to handle Proxmox auth)

### Where is the API documentation?

Interactive Swagger UI is available at:

```
http://localhost:8000/docs
```

Alternative ReDoc interface:

```
http://localhost:8000/redoc
```

Raw OpenAPI JSON schema:

```
http://localhost:8000/openapi.json
```

### How do I create a VM?

```bash
curl -X POST http://localhost:8000/nodes/pve1/qemu \
  -H "Content-Type: application/json" \
  -d '{
    "vmid": 100,
    "name": "test-vm",
    "memory": 4096,
    "cores": 2,
    "sockets": 1,
    "scsi0": "local-lvm:32",
    "net0": "virtio,bridge=vmbr0"
  }'
```

See the [API Reference](api-reference.md) for all available endpoints.

### What's the difference between this and pynetbox?

**pynetbox** is a Python client for **NetBox** (DCIM/IPAM tool).

**proxmox-sdk** is a FastAPI server for **Proxmox VE** (virtualization platform).

They're completely different projects for different tools. You might use both if you're managing infrastructure with both NetBox and Proxmox.

## Development

### Can I contribute to this project?

**Yes!** Contributions are welcome:

- 🐛 Bug reports and fixes
- ✨ New features
- 📚 Documentation improvements
- 🧪 Test coverage
- 🎨 Code quality improvements

See the [Development Guide](development.md) for contribution guidelines.

### How do I regenerate the OpenAPI schema?

Use the built-in code generation pipeline:

```python
from proxmox_sdk.proxmox_codegen import ProxmoxCodegenPipeline

pipeline = ProxmoxCodegenPipeline(
    proxmox_url="https://proxmox.example.com:8006",
    username="root@pam",
    password="password",
    verify_ssl=False,
)

await pipeline.run_full_pipeline(
    output_dir="./output",
    version_tag="8.1",
)
```

This generates:
- `raw_capture.json` - Crawler output
- `openapi.json` - OpenAPI 3.1 schema
- `pydantic_models.py` - Pydantic models

See the [Development Guide](development.md#code-generation-pipeline) for details.

### How do I run tests?

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=proxmox_sdk --cov-report=html
```

See the [Development Guide](development.md#testing) for more details.

### How do I build the documentation locally?

```bash
# Serve docs with live reload
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

Documentation will be available at `http://127.0.0.1:8000`.

## Troubleshooting

### Server won't start - "Module not found" error

Make sure you've installed the package:

```bash
uv pip install proxmox-sdk

# Or for development
uv pip install -e .
```

### Mock mode: "Schema not found" error

The pre-generated schema should be included in the package. If missing:

```bash
# Reinstall the package
uv pip install --force-reinstall proxmox-sdk
```

### Real mode: "Connection refused" error

Check that:
1. `PROXMOX_API_URL` is correct (including `https://` and port `:8006`)
2. Proxmox server is running and accessible
3. Firewall allows access on port 8006
4. SSL certificate is valid (or set `PROXMOX_API_VERIFY_SSL=false` for testing)

### Real mode: "401 Unauthorized" error

Check your credentials:

```bash
# For API token
echo $PROXMOX_API_TOKEN_ID      # Should be: user@realm!tokenid (e.g., root@pam!mytoken)
echo $PROXMOX_API_TOKEN_SECRET  # Should be: UUID secret

# For username/password
echo $PROXMOX_API_USERNAME  # Should be: user@realm (e.g., root@pam)
echo $PROXMOX_API_PASSWORD
```

Verify credentials work with direct Proxmox API access:

```bash
curl -k https://proxmox.example.com:8006/api2/json/version \
  -H "Authorization: PVEAPIToken=user@realm!tokenid=uuid"
```

### Real mode: "SSL certificate verification failed"

For development/testing with self-signed certificates:

```bash
export PROXMOX_API_VERIFY_SSL=false
```

**Never disable SSL verification in production.** Instead, add the Proxmox CA certificate to your system trust store.

### Slow startup time

Normal startup times:
- Mock mode: ~1 second (loads 5.2MB schema)
- Real mode: ~500ms (minimal initialization)

If startup is significantly slower:
1. Check disk I/O performance
2. Ensure you're not in debug mode with hot-reload (use `--reload` only for development)
3. Verify Python version (3.11+ recommended for best performance)

### High memory usage

Expected memory usage:
- Mock mode: ~100MB (schema + in-memory state)
- Real mode: ~80MB (schema + aiohttp session)

If memory usage is significantly higher:
1. Check for memory leaks in custom code
2. Monitor the size of mock state (large CRUD operations)
3. Consider restarting periodically in development

### Endpoints return different data than real Proxmox

**Mock mode:** Returns simulated data, not real Proxmox data. Use custom mock data to match your test scenarios.

**Real mode:** Should match Proxmox exactly. If not, check:
1. Proxmox version compatibility
2. Schema version matches your Proxmox installation
3. Report as a bug if validation is incorrect

## Performance

### How many requests can it handle?

**Mock mode:** 10,000+ requests/second (limited by FastAPI/uvicorn)

**Real mode:** Limited by your Proxmox server capacity. The proxy adds ~20-100ms overhead for validation.

For high-traffic production use, consider:
- Running multiple instances behind a load balancer
- Using a production ASGI server (gunicorn with uvicorn workers)
- Direct Proxmox API access (bypassing the proxy)

### Can I scale horizontally?

**Yes!** The server is stateless (in real mode) or uses in-memory state (mock mode).

For real mode:
- Run multiple instances behind a load balancer
- Each instance independently proxies to Proxmox

For mock mode:
- Each instance has its own in-memory state
- Not suitable for shared mock environments (use a database-backed mode instead)

## License & Support

### What license is this project under?

**MIT License** - Free to use, modify, and distribute, including commercial use.

See the [LICENSE](https://github.com/emersonfelipesp/proxmox-sdk/blob/main/LICENSE) file for full details.

### Where can I get help?

- **Documentation:** https://emersonfelipesp.github.io/proxmox-sdk/
- **Issues:** https://github.com/emersonfelipesp/proxmox-sdk/issues
- **Discussions:** https://github.com/emersonfelipesp/proxmox-sdk/discussions

### Can I hire you for custom development?

This is an open-source project maintained by community contributors. For custom development or consulting:

- Post in GitHub Discussions
- Create a detailed issue describing your needs
- Consider sponsoring the project if you find it valuable

---

**Still have questions?** Open a [GitHub Discussion](https://github.com/emersonfelipesp/proxmox-sdk/discussions) or [Issue](https://github.com/emersonfelipesp/proxmox-sdk/issues).

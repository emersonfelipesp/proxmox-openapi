# AGENTS.md - proxmox-sdk Agent Index

## Quick Start

| What you need | Go here |
|---|---|
| Project architecture and package structure | [CLAUDE.md](CLAUDE.md) |
| Developer setup and usage | [README.md](README.md) |
| API and SDK documentation | [docs/](docs/) |
| Security controls and hardening details | [docs/security.md](docs/security.md) |
| Performance characteristics and optimisations | [docs/performance.md](docs/performance.md) |

## Working Rules

1. Read [CLAUDE.md](CLAUDE.md) before making changes.
2. Keep changes focused and scoped to the requested task.
3. Run required checks before submitting changes.
4. Before every commit and every push, run `uv run pre-commit run --all-files` and fix all failures.

## Required Pre-Commit Workflow

Use this workflow in the repository root:

```bash
uv sync
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
uv run pre-commit run --all-files
```

Do not commit or push when pre-commit hooks are failing.

## Release Process

To ship a new version to PyPI and Docker Hub:

1. Bump `version` in `pyproject.toml` (PEP 440, e.g. `0.0.2.post4`).
2. Run pre-commit and tests: `uv run pre-commit run --all-files && uv run pytest`
3. Commit: `git commit -m "chore: bump version to <new-version>" pyproject.toml`
4. Push: `git push origin main`
5. Tag: `git tag v<new-version> && git push origin v<new-version>`
6. Release (triggers full publish pipeline):
   ```bash
   gh release create v<new-version> --title "v<new-version>" --notes "..."
   ```
7. Update dependents — bump `proxmox-sdk==<new-version>` in `proxbox-api/pyproject.toml` and any other consumers, commit, and push.

The GitHub release triggers `publish-testpypi.yml` which validates, publishes to PyPI, and pushes all three Docker image variants (`raw`, `nginx`, `granian`) with both `<version>` and `latest` tags.

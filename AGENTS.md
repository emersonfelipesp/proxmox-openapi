# AGENTS.md - proxmox-openapi Agent Index

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

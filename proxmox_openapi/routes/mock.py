"""Routes for mock API endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from proxmox_openapi import __version__

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Return the mock API root payload."""
    return {
        "message": "Proxmox OpenAPI Mock Server",
        "version": __version__,
        "docs": "/mock/docs",
    }


@router.get("/health")
async def health() -> dict[str, str]:
    """Return the mock API health status."""
    return {"status": "ready"}


@router.get("/version")
async def version() -> dict[str, str]:
    """Return the package version for the mock API."""
    return {"version": __version__}


__all__ = ["router"]

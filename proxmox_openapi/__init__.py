"""Proxmox OpenAPI - Schema-driven FastAPI package for Proxmox API."""

__version__ = "0.0.1"

from proxmox_openapi.main import app
from proxmox_openapi.mock_main import app as mock_app
from proxmox_openapi.mock_main import run

__all__ = ["app", "mock_app", "run", "__version__"]

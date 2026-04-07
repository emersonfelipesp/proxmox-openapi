"""Proxmox OpenAPI — schema-driven FastAPI package and standalone Python SDK."""

__version__ = "0.0.2"

# FastAPI app exports (unchanged)
from proxmox_openapi.main import app
from proxmox_openapi.mock_main import app as mock_app
from proxmox_openapi.mock_main import run

# SDK exports
from proxmox_openapi.sdk.api import ProxmoxSDK
from proxmox_openapi.sdk.exceptions import (
    AuthenticationError,
    BackendNotAvailableError,
    ProxmoxSDKError,
    ResourceException,
)
from proxmox_openapi.sdk.sync import SyncProxmoxSDK
from proxmox_openapi.sdk.tools.files import Files
from proxmox_openapi.sdk.tools.tasks import Tasks

__all__ = [
    # FastAPI
    "app",
    "mock_app",
    "run",
    # SDK
    "ProxmoxSDK",
    "SyncProxmoxSDK",
    "ResourceException",
    "AuthenticationError",
    "BackendNotAvailableError",
    "ProxmoxSDKError",
    "Tasks",
    "Files",
    "__version__",
]

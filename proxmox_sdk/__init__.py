"""Proxmox OpenAPI — schema-driven FastAPI package and standalone Python SDK."""

__version__ = "0.0.3.post1"

# Lazy imports: avoid constructing FastAPI apps or loading heavy SDK modules
# at package import time.  Attributes are resolved on first access only.

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
    "ProxmoxTimeoutError",
    "ProxmoxConnectionError",
    "Tasks",
    "Files",
    "__version__",
]

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    # (module_path, attribute_name)
    "app": ("proxmox_sdk.main", "app"),
    "mock_app": ("proxmox_sdk.mock_main", "app"),
    "run": ("proxmox_sdk.mock_main", "run"),
    "ProxmoxSDK": ("proxmox_sdk.sdk.api", "ProxmoxSDK"),
    "SyncProxmoxSDK": ("proxmox_sdk.sdk.sync", "SyncProxmoxSDK"),
    "ResourceException": ("proxmox_sdk.sdk.exceptions", "ResourceException"),
    "AuthenticationError": ("proxmox_sdk.sdk.exceptions", "AuthenticationError"),
    "BackendNotAvailableError": ("proxmox_sdk.sdk.exceptions", "BackendNotAvailableError"),
    "ProxmoxSDKError": ("proxmox_sdk.sdk.exceptions", "ProxmoxSDKError"),
    "ProxmoxTimeoutError": ("proxmox_sdk.sdk.exceptions", "ProxmoxTimeoutError"),
    "ProxmoxConnectionError": ("proxmox_sdk.sdk.exceptions", "ProxmoxConnectionError"),
    "Tasks": ("proxmox_sdk.sdk.tools.tasks", "Tasks"),
    "Files": ("proxmox_sdk.sdk.tools.files", "Files"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_path, attr = _LAZY_IMPORTS[name]
        import importlib

        mod = importlib.import_module(module_path)
        value = getattr(mod, attr)
        # Cache on the module so __getattr__ is not called again for this name.
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

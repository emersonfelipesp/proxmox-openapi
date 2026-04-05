"""Standalone FastAPI app for the schema-driven Proxmox mock API."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI

from proxmox_openapi import __version__
from proxmox_openapi.mock.loader import load_mock_data
from proxmox_openapi.schema import DEFAULT_PROXMOX_OPENAPI_TAG, load_proxmox_generated_openapi


def create_mock_app() -> FastAPI:
    """Build the standalone Proxmox mock API app."""

    version_tag = os.environ.get("PROXMOX_MOCK_SCHEMA_VERSION", DEFAULT_PROXMOX_OPENAPI_TAG)
    openapi_doc = load_proxmox_generated_openapi(version_tag=version_tag)

    app = FastAPI(
        title="Proxmox Mock API",
        description="Schema-driven in-memory FastAPI mock for the generated Proxmox API.",
        version=__version__,
    )

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "message": "Schema-driven Proxmox mock API",
            "schema_version": version_tag,
            "package_version": __version__,
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ready"}

    @app.get("/version")
    async def version() -> dict[str, str]:
        return {"version": __version__}

    custom_mock_data = load_mock_data()
    if custom_mock_data:
        if openapi_doc:
            from proxmox_openapi.mock.routes import register_generated_proxmox_mock_routes

            register_generated_proxmox_mock_routes(
                app,
                version_tag=version_tag,
                openapi_document=openapi_doc,
                custom_mock_data=custom_mock_data,
            )
            return app

        _register_static_mock_routes(app, custom_mock_data)
        return app

    if openapi_doc:
        from proxmox_openapi.mock.routes import register_generated_proxmox_mock_routes

        register_generated_proxmox_mock_routes(
            app, version_tag=version_tag, openapi_document=openapi_doc
        )
        return app

    @app.get("/api2/json")
    async def no_schema() -> dict[str, str]:
        return {
            "error": "No schema loaded",
            "message": f"Run /codegen/generate to generate version '{version_tag}' or use the full API server.",
        }

    return app


def _register_static_mock_routes(app: FastAPI, mock_data: dict[str, Any]) -> None:
    """Register static mock routes from custom mock data."""

    @app.get("/api2/json/{path:path}")
    async def static_mock_get(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

    @app.post("/api2/json/{path:path}")
    async def static_mock_post(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

    @app.put("/api2/json/{path:path}")
    async def static_mock_put(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

    @app.patch("/api2/json/{path:path}")
    async def static_mock_patch(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

    @app.delete("/api2/json/{path:path}")
    async def static_mock_delete(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

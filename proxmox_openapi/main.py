"""Proxmox OpenAPI main module - Full API with Swagger docs."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, Request
from fastapi import __version__ as fastapi_version

from proxmox_openapi import __version__
from proxmox_openapi.proxmox.config import ProxmoxConfig
from proxmox_openapi.routes.codegen import router as codegen_router
from proxmox_openapi.routes.mock import router as mock_router
from proxmox_openapi.routes.versions import router as versions_router
from proxmox_openapi.schema import DEFAULT_PROXMOX_OPENAPI_TAG, load_proxmox_generated_openapi


def create_app() -> FastAPI:
    """Build the Proxmox OpenAPI FastAPI application.

    Modes:
        - mock (default): In-memory CRUD with generated mock endpoints
        - real: Proxy to real Proxmox API with request/response validation

    Environment Variables:
        PROXMOX_API_MODE: "mock" or "real" (default: "mock")
        PROXMOX_MOCK_SCHEMA_VERSION: Schema version tag for mock mode (default: "latest")

    For real mode, also required:
        PROXMOX_API_URL: Proxmox server URL (e.g., "https://pve.example.com:8006")
        PROXMOX_API_TOKEN_ID + PROXMOX_API_TOKEN_SECRET: API token auth
        OR PROXMOX_API_USERNAME + PROXMOX_API_PASSWORD: Password auth
        PROXMOX_API_VERIFY_SSL: Verify SSL (default: "true")
    """
    # Load configuration from environment
    config = ProxmoxConfig.from_env()
    api_mode = config.api_mode

    app = FastAPI(
        title="Proxmox OpenAPI",
        description=(
            f"Schema-driven FastAPI package for Proxmox API (mode: {api_mode}). "
            "Supports OpenAPI generation, mock data, in-memory CRUD, and real Proxmox connections."
        ),
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    import logging

    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from slowapi import _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    from slowapi.middleware import SlowAPIMiddleware
    from starlette.exceptions import HTTPException as StarletteHTTPException

    from proxmox_openapi.rate_limit import limiter

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    logger = logging.getLogger("proxmox_openapi")

    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        if isinstance(exc, StarletteHTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
                headers=exc.headers,
            )
        logger.exception("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."},
        )

    cors_origins = os.environ.get("CORS_ORIGINS", "")
    allowed_origins = [origin.strip() for origin in cors_origins.split(",")] if cors_origins else []

    if allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )

    # Track loaded Proxmox endpoints
    proxmox_route_info: dict[str, Any] = {"mode": api_mode}

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "message": "Proxmox OpenAPI",
            "version": __version__,
            "docs": "/docs",
            "mode": api_mode,
            "proxmox_endpoints": proxmox_route_info.get("route_count", 0),
        }

    @app.get("/health", include_in_schema=False)
    async def health(request: Request) -> dict[str, str]:
        # Require internal IP or authorization
        client_host = request.client.host if request.client else None
        if client_host not in ("127.0.0.1", "::1", "localhost", "testclient"):
            from fastapi import HTTPException, status

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return {"status": "ready"}

    @app.get("/version")
    async def version() -> dict[str, str]:
        return {
            "version": __version__,
            "fastapi": fastapi_version,
        }

    @app.get("/mode")
    async def mode() -> dict[str, Any]:
        result: dict[str, Any] = {
            "mode": api_mode,
            "schema_version": proxmox_route_info.get("schema_version", "unknown"),
            "proxmox_endpoints": proxmox_route_info.get("route_count", 0),
            "proxmox_paths": proxmox_route_info.get("path_count", 0),
            "proxmox_methods": proxmox_route_info.get("method_count", 0),
        }
        if api_mode == "real":
            result["auth_method"] = (
                "token" if config.token_id else "password" if config.username else "none"
            )
            result["ssl_verify"] = config.verify_ssl
        return result

    app.include_router(codegen_router, prefix="/codegen", tags=["codegen"])
    app.include_router(mock_router, prefix="/mock", tags=["mock"])
    app.include_router(versions_router, prefix="/versions", tags=["versions"])

    # Load Proxmox endpoints based on mode
    version_tag = os.environ.get("PROXMOX_MOCK_SCHEMA_VERSION", DEFAULT_PROXMOX_OPENAPI_TAG)
    openapi_doc = load_proxmox_generated_openapi(version_tag=version_tag)

    if openapi_doc:
        if config.is_mock_mode():
            # Mock mode: In-memory CRUD operations
            from proxmox_openapi.mock.routes import register_generated_proxmox_mock_routes

            proxmox_route_info.update(
                register_generated_proxmox_mock_routes(
                    app,
                    version_tag=version_tag,
                    openapi_document=openapi_doc,
                )
            )
        elif config.is_real_mode():
            # Real mode: Proxy to actual Proxmox API with validation
            try:
                config.validate_for_real_mode()
                from proxmox_openapi.proxmox.routes import register_generated_proxmox_real_routes

                proxmox_route_info.update(
                    register_generated_proxmox_real_routes(
                        app,
                        version_tag=version_tag,
                        openapi_document=openapi_doc,
                        proxmox_config=config,
                    )
                )
            except ValueError as config_error:
                # Configuration validation failed - add warning endpoint
                error_message = str(config_error)

                @app.get("/api2/json")
                async def config_error_endpoint() -> dict[str, str]:
                    return {
                        "error": "Invalid configuration for real API mode",
                        "detail": error_message,
                    }

    return app


app = create_app()

__all__ = ["app", "create_app"]

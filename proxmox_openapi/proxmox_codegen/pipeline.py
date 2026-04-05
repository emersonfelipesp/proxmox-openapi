"""End-to-end Proxmox API Viewer -> OpenAPI -> Pydantic generation pipeline."""

from __future__ import annotations

import asyncio
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from proxmox_openapi.proxmox_codegen.apidoc_parser import (
    PROXMOX_API_VIEWER_URL,
    fetch_apidoc_js,
    flatten_api_schema,
    parse_api_schema,
)
from proxmox_openapi.proxmox_codegen.crawler import crawl_proxmox_api_viewer_async
from proxmox_openapi.proxmox_codegen.models import GenerationBundle
from proxmox_openapi.proxmox_codegen.normalize import normalize_captured_endpoints
from proxmox_openapi.proxmox_codegen.openapi_generator import generate_openapi_schema
from proxmox_openapi.proxmox_codegen.pydantic_generator import (
    generate_pydantic_models_from_openapi,
)
from proxmox_openapi.proxmox_codegen.utils import dump_json, ensure_parent, utc_now_iso

LATEST_VERSION_TAG = "latest"

_playwright_available: bool | None = None


def _check_playwright_available() -> bool:
    """Check if playwright is available for import."""
    global _playwright_available
    if _playwright_available is None:
        try:
            import playwright  # noqa: F401

            _playwright_available = True
        except ImportError:
            _playwright_available = False
    return _playwright_available


def _normalized_viewer_url(url: str) -> str:
    """Normalize a Proxmox viewer URL for comparisons."""
    parsed = urlparse(url.strip())
    path = parsed.path or "/"
    if path.endswith("index.html"):
        path = path[: -len("index.html")]
    path = path.rstrip("/")
    if not path:
        path = "/"
    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            "",
            "",
            "",
        )
    )


def _viewer_apidoc_js_url(source_url: str) -> str:
    """Build the apidoc.js URL for a viewer source URL."""
    normalized = _normalized_viewer_url(source_url)
    parsed = urlparse(normalized)
    apidoc_path = f"{parsed.path.rstrip('/')}/apidoc.js"
    return urlunparse((parsed.scheme, parsed.netloc, apidoc_path, "", "", ""))


def _validate_source_for_version_tag(source_url: str, version_tag: str) -> None:
    """Reject non-official viewer URLs when using the reserved latest tag."""
    if version_tag != LATEST_VERSION_TAG:
        return
    if _normalized_viewer_url(source_url) != _normalized_viewer_url(PROXMOX_API_VIEWER_URL):
        raise ValueError("Version tag 'latest' is reserved for official Proxmox API viewer URL.")


def _merge_capture(
    viewer_capture: dict[str, object],
    apidoc_flattened: dict[str, dict[str, object]],
) -> dict[str, object]:
    """Merge viewer-captured methods with apidoc fallback when any method is missing."""

    merged = {}
    viewer_endpoints = viewer_capture.get("endpoints", {}) or {}

    for path in sorted(set(viewer_endpoints) | set(apidoc_flattened)):
        viewer_endpoint = viewer_endpoints.get(path, {})
        fallback = apidoc_flattened.get(path, {})
        methods = dict(viewer_endpoint.get("methods", {}) or {})
        fallback_info = fallback.get("info", {}) if isinstance(fallback, dict) else {}

        for method in ("GET", "POST", "PUT", "DELETE"):
            if method in methods:
                continue
            method_data = fallback_info.get(method)
            if method_data:
                methods[method] = {
                    "method": method,
                    "path": path,
                    "method_name": method_data.get("name"),
                    "description": method_data.get("description"),
                    "viewer_description": None,
                    "viewer_usage": None,
                    "parameters": method_data.get("parameters"),
                    "returns": method_data.get("returns"),
                    "permissions": method_data.get("permissions"),
                    "allowtoken": method_data.get("allowtoken"),
                    "protected": method_data.get("protected"),
                    "unstable": method_data.get("unstable"),
                    "raw_sections": [],
                    "source": "apidoc-fallback",
                }

        merged[path] = {
            "path": path,
            "text": viewer_endpoint.get("text") or fallback.get("text"),
            "depth": viewer_endpoint.get("depth"),
            "methods": methods,
        }

    return merged


def _capture_completeness(
    merged_capture: dict[str, object],
    viewer_capture: dict[str, object],
    apidoc_flat: dict[str, object],
) -> dict[str, object]:
    """Build capture completeness stats for diagnostics and validation."""

    merged_paths = set(merged_capture.keys())
    viewer_paths = set((viewer_capture.get("endpoints") or {}).keys())
    apidoc_paths = set(apidoc_flat.keys())

    missing_from_viewer = sorted(merged_paths - viewer_paths)
    missing_from_apidoc = sorted(merged_paths - apidoc_paths)

    fallback_methods = 0
    for endpoint in merged_capture.values():
        for method_data in (endpoint.get("methods") or {}).values():
            if method_data.get("source") == "apidoc-fallback":
                fallback_methods += 1

    return {
        "merged_endpoint_count": len(merged_paths),
        "viewer_endpoint_count": len(viewer_paths),
        "apidoc_endpoint_count": len(apidoc_paths),
        "missing_from_viewer": missing_from_viewer,
        "missing_from_apidoc": missing_from_apidoc,
        "fallback_method_count": fallback_methods,
    }


def _run_async_from_sync(coro: object) -> object:
    """Run a coroutine from sync code, even when already inside an event loop."""

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    result: dict[str, object] = {"value": None, "error": None}

    def _runner() -> None:
        try:
            result["value"] = asyncio.run(coro)
        except Exception as error:  # pragma: no cover - surfaced to caller
            result["error"] = error

    import threading

    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()
    thread.join()
    if result["error"] is not None:
        raise result["error"]
    return result["value"]


def generate_proxmox_codegen_bundle(
    output_dir: str | Path | None = None,
    *,
    source_url: str = PROXMOX_API_VIEWER_URL,
    version_tag: str = LATEST_VERSION_TAG,
    worker_count: int = 10,
    retry_count: int = 2,
    retry_backoff_seconds: float = 0.35,
    checkpoint_every: int = 50,
    allow_insecure_ssl: bool = False,
) -> GenerationBundle:
    """Sync wrapper for async generation pipeline."""

    return _run_async_from_sync(
        generate_proxmox_codegen_bundle_async(
            output_dir=output_dir,
            source_url=source_url,
            version_tag=version_tag,
            worker_count=worker_count,
            retry_count=retry_count,
            retry_backoff_seconds=retry_backoff_seconds,
            checkpoint_every=checkpoint_every,
            allow_insecure_ssl=allow_insecure_ssl,
        )
    )


async def generate_proxmox_codegen_bundle_async(
    output_dir: str | Path | None = None,
    *,
    source_url: str = PROXMOX_API_VIEWER_URL,
    version_tag: str = LATEST_VERSION_TAG,
    worker_count: int = 10,
    retry_count: int = 2,
    retry_backoff_seconds: float = 0.35,
    checkpoint_every: int = 50,
    allow_insecure_ssl: bool = False,
) -> GenerationBundle:
    """Run full generation pipeline and optionally persist artifacts."""

    cleaned_version_tag = version_tag.strip()
    if not cleaned_version_tag:
        raise ValueError("version_tag cannot be empty.")
    _validate_source_for_version_tag(source_url=source_url, version_tag=cleaned_version_tag)

    if _check_playwright_available():
        viewer_capture = await crawl_proxmox_api_viewer_async(
            url=source_url,
            worker_count=worker_count,
            retry_count=retry_count,
            retry_backoff_seconds=retry_backoff_seconds,
            checkpoint_path=(
                str(Path(output_dir) / cleaned_version_tag / "crawl_checkpoint.json")
                if output_dir is not None
                else None
            ),
            checkpoint_every=checkpoint_every,
        )
    else:
        viewer_capture = {
            "endpoints": {},
            "discovered_navigation_items": 0,
            "method_count": 0,
            "failed_endpoint_count": 0,
            "duration_seconds": 0.0,
        }

    apidoc_source = fetch_apidoc_js(
        url=_viewer_apidoc_js_url(source_url),
        allow_insecure=allow_insecure_ssl,
    )
    apidoc_tree = parse_api_schema(apidoc_source)
    apidoc_flat = flatten_api_schema(apidoc_tree)

    merged_capture = _merge_capture(viewer_capture=viewer_capture, apidoc_flattened=apidoc_flat)
    completeness = _capture_completeness(
        merged_capture=merged_capture,
        viewer_capture=viewer_capture,
        apidoc_flat=apidoc_flat,
    )
    operations = normalize_captured_endpoints(merged_capture)

    openapi = generate_openapi_schema(
        operations,
        version=cleaned_version_tag,
        server_url="/api2/json",
    )

    models_code = generate_pydantic_models_from_openapi(openapi)

    bundle = GenerationBundle(
        source_url=source_url,
        version_tag=cleaned_version_tag,
        generated_at=utc_now_iso(),
        endpoint_count=len(merged_capture),
        operation_count=len(operations),
        capture={
            "viewer": viewer_capture,
            "apidoc_endpoint_count": len(apidoc_flat),
            "merged_endpoints": merged_capture,
            "completeness": completeness,
        },
        openapi=openapi,
        pydantic_models_code=models_code,
    )

    if output_dir is not None:
        base = Path(output_dir) / cleaned_version_tag
        raw_path = base / "raw_capture.json"
        openapi_path = base / "openapi.json"
        models_path = base / "pydantic_models.py"

        dump_json(raw_path, bundle.capture)
        dump_json(openapi_path, bundle.openapi)
        ensure_parent(models_path)
        models_path.write_text(bundle.pydantic_models_code, encoding="utf-8")

    return bundle


__all__ = [
    "LATEST_VERSION_TAG",
    "generate_proxmox_codegen_bundle",
    "generate_proxmox_codegen_bundle_async",
]

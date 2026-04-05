"""CLI entrypoint for Proxmox API Viewer code generation artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

from proxmox_openapi.proxmox_codegen.apidoc_parser import PROXMOX_API_VIEWER_URL
from proxmox_openapi.proxmox_codegen.pipeline import generate_proxmox_codegen_bundle


def build_parser() -> argparse.ArgumentParser:
    """Build command-line parser for Proxmox code generation command."""

    parser = argparse.ArgumentParser(
        description="Generate OpenAPI and Pydantic v2 schemas from Proxmox API Viewer.",
    )
    parser.add_argument(
        "--output-dir",
        default="proxmox_openapi/generated/proxmox",
        help="Base output directory; artifacts are written under <output-dir>/<version-tag>/.",
    )
    parser.add_argument(
        "--source-url",
        default=PROXMOX_API_VIEWER_URL,
        help="Proxmox API viewer URL to crawl.",
    )
    parser.add_argument(
        "--version-tag",
        default="latest",
        help="Version tag used for output subdirectory and OpenAPI info.version.",
    )
    parser.add_argument(
        "--workers",
        default=10,
        type=int,
        help="Number of async Playwright workers used for endpoint capture.",
    )
    parser.add_argument(
        "--retry-count",
        default=2,
        type=int,
        help="Retry attempts per endpoint capture when transient failures occur.",
    )
    parser.add_argument(
        "--retry-backoff",
        default=0.35,
        type=float,
        help="Base exponential backoff in seconds between endpoint retries.",
    )
    parser.add_argument(
        "--checkpoint-every",
        default=50,
        type=int,
        help="Write crawl checkpoint after this many processed endpoints.",
    )
    parser.add_argument(
        "--allow-insecure-ssl",
        action="store_true",
        default=False,
        help=(
            "Disable SSL certificate verification when fetching apidoc.js. "
            "Only use this in controlled/offline environments with a self-signed cert. "
            "NOT recommended for production use."
        ),
    )
    return parser


def main() -> int:
    """Run Proxmox API Viewer code generation and write artifacts to disk."""

    parser = build_parser()
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    bundle = generate_proxmox_codegen_bundle(
        output_dir=output_dir,
        source_url=args.source_url,
        version_tag=args.version_tag,
        worker_count=max(1, args.workers),
        retry_count=max(0, args.retry_count),
        retry_backoff_seconds=max(0.0, args.retry_backoff),
        checkpoint_every=max(1, args.checkpoint_every),
        allow_insecure_ssl=args.allow_insecure_ssl,
    )
    viewer_capture = bundle.capture.get("viewer", {})
    completeness = bundle.capture.get("completeness", {})
    print(
        "Generated artifacts:",
        {
            "output_dir": str(output_dir),
            "source_url": bundle.source_url,
            "version_tag": bundle.version_tag,
            "generated_at": bundle.generated_at,
            "endpoint_count": bundle.endpoint_count,
            "operation_count": bundle.operation_count,
            "viewer_capture": {
                "endpoint_count": viewer_capture.get("endpoint_count"),
                "navigation_items": viewer_capture.get("discovered_navigation_items"),
                "method_count": viewer_capture.get("method_count"),
                "duration_seconds": viewer_capture.get("duration_seconds"),
                "worker_count": viewer_capture.get("worker_count"),
            },
            "completeness": {
                "fallback_method_count": completeness.get("fallback_method_count"),
                "missing_from_viewer": len(completeness.get("missing_from_viewer", [])),
            },
            "requested_workers": max(1, args.workers),
            "retry_count": max(0, args.retry_count),
            "retry_backoff_seconds": max(0.0, args.retry_backoff),
            "checkpoint_every": max(1, args.checkpoint_every),
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

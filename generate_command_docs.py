#!/usr/bin/env python3
"""Shim for `proxmox docs generate-capture`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate proxmox CLI capture documentation.",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--raw-dir", type=Path, default=None)
    parser.add_argument("--max-lines", type=int, default=200)
    parser.add_argument("--max-chars", type=int, default=120_000)
    args = parser.parse_args()

    from proxmox_openapi.proxmox_cli.docgen_capture import (
        generate_command_capture_docs,
        resolve_capture_paths,
    )

    try:
        out, raw = resolve_capture_paths(args.output, args.raw_dir)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    return generate_command_capture_docs(
        output=out,
        raw_dir=raw,
        max_lines=args.max_lines,
        max_chars=args.max_chars,
    )


if __name__ == "__main__":
    raise SystemExit(main())

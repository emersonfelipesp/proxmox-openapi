"""MkDocs hooks to expand generated CLI capture JSON into linked reference pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_RAW_DIR = _REPO_ROOT / "docs" / "generated" / "raw"
_INDEX_FILE = _RAW_DIR / "index.json"
_CAPTURES_DIR = _REPO_ROOT / "docs" / "reference" / "command-capture"


def _strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[mGKHF]", "", text)


def _slug(section: str) -> str:
    s = section.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "uncategorized"


def _render_section(section: str, runs: list[dict], stdout_map: dict[tuple[str, str], str]) -> str:
    lines: list[str] = [f"# {section}", ""]

    for run in runs:
        title = str(run.get("title", ""))
        argv = run.get("argv", [])
        exit_code = int(run.get("exit_code", 0))
        elapsed = float(run.get("elapsed_seconds", 0.0))
        stdout = stdout_map.get((section, title), "(empty)").rstrip() or "(empty)"

        cmd = "proxmox " + " ".join(argv)

        lines.append(f"### `{title}`")
        lines.append("")
        lines.append("**Input:**")
        lines.append("")
        lines.append("```bash")
        lines.append(cmd)
        lines.append("```")
        lines.append("")
        lines.append("**Output:**")
        lines.append("")
        lines.append("```text")
        lines.extend(_strip_ansi(stdout).splitlines() or ["(empty)"])
        lines.append("```")
        lines.append("")
        lines.append(f"**Exit code:** `{exit_code}`  ·  **Wall time (s):** `{elapsed:.3f}`")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _not_generated() -> str:
    return (
        "# CLI command captures\n\n"
        "!!! warning \"Not yet generated\"\n"
        "    Run `uv run proxmox docs generate-capture` from repo root, then rebuild docs.\n"
    )


def _build_command_capture_pages() -> None:
    _CAPTURES_DIR.mkdir(parents=True, exist_ok=True)

    if not _INDEX_FILE.exists():
        (_CAPTURES_DIR / "index.md").write_text(_not_generated(), encoding="utf-8")
        return

    payload = json.loads(_INDEX_FILE.read_text(encoding="utf-8"))
    meta = payload.get("meta", {})
    runs = payload.get("runs", [])

    stdout_map: dict[tuple[str, str], str] = {}
    for raw_file in sorted(_RAW_DIR.glob("*.json")):
        if raw_file.name == "index.json":
            continue
        try:
            row = json.loads(raw_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        key = (str(row.get("section", "")), str(row.get("title", "")))
        stdout_map[key] = str(row.get("stdout_full", ""))

    sections: dict[str, list[dict]] = {}
    for run in runs:
        section = str(run.get("section", "Uncategorized"))
        sections.setdefault(section, []).append(run)

    section_rows: list[tuple[str, str]] = []
    for section in sorted(sections.keys()):
        slug = _slug(section)
        content = _render_section(section, sections[section], stdout_map)
        (_CAPTURES_DIR / f"{slug}.md").write_text(content, encoding="utf-8")
        section_rows.append((section, slug))

    generated_at = str(meta.get("generated_at", "unknown"))
    total = len(runs)

    index_lines: list[str] = [
        "# CLI command captures",
        "",
        "!!! info \"Machine-generated\"",
        "    Built from `docs/generated/raw/index.json` during MkDocs build.",
        f"    Last updated: `{generated_at}`",
        "",
        "## Sections",
        "",
    ]
    for section, slug in section_rows:
        count = len(sections[section])
        suffix = "s" if count != 1 else ""
        index_lines.append(f"- [{section}](./{slug}.md) - {count} command{suffix}")
    index_lines.extend(["", f"Total captures: `{total}`", ""])

    (_CAPTURES_DIR / "index.md").write_text("\n".join(index_lines), encoding="utf-8")


def on_pre_build(config, **kwargs) -> None:
    _build_command_capture_pages()

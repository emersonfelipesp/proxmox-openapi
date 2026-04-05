from __future__ import annotations

from pathlib import Path

from proxmox_openapi import schema as schema_module
from proxmox_openapi.mock.loader import load_mock_data
from proxmox_openapi.schema import load_proxmox_generated_openapi


def test_load_mock_data_rejects_json_array(tmp_path: Path) -> None:
    mock_file = tmp_path / "mock-data.json"
    mock_file.write_text("[]", encoding="utf-8")

    assert load_mock_data(mock_file) is None


def test_load_mock_data_rejects_yaml_scalar(tmp_path: Path) -> None:
    mock_file = tmp_path / "mock-data.yaml"
    mock_file.write_text("- item\n- item2\n", encoding="utf-8")

    assert load_mock_data(mock_file) is None


def test_load_generated_openapi_rejects_non_object(tmp_path: Path, monkeypatch) -> None:
    version_dir = tmp_path / "latest"
    version_dir.mkdir(parents=True)
    (version_dir / "openapi.json").write_text("[]", encoding="utf-8")

    monkeypatch.setattr(schema_module, "_generated_dir", lambda: tmp_path)

    assert load_proxmox_generated_openapi("latest") is None


def test_load_generated_openapi_rejects_malformed_json(tmp_path: Path, monkeypatch) -> None:
    version_dir = tmp_path / "latest"
    version_dir.mkdir(parents=True)
    (version_dir / "openapi.json").write_text("{", encoding="utf-8")

    monkeypatch.setattr(schema_module, "_generated_dir", lambda: tmp_path)

    assert load_proxmox_generated_openapi("latest") is None

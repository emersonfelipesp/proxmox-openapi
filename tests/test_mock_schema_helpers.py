from proxmox_openapi.mock.schema_helpers import sample_value_for_schema


def test_semantic_node_string_value() -> None:
    value = sample_value_for_schema({"type": "string"}, seed="s1", field_name="node")
    assert isinstance(value, str)
    assert value.startswith("pve-node-")


def test_semantic_vmid_integer_value() -> None:
    value = sample_value_for_schema({"type": "integer"}, seed="s2", field_name="vmid")
    assert isinstance(value, int)
    assert 100 <= value <= 899


def test_semantic_status_prefers_running_enum() -> None:
    value = sample_value_for_schema(
        {"type": "string", "enum": ["stopped", "running", "paused"]},
        seed="s3",
        field_name="status",
    )
    assert value == "running"


def test_semantic_nested_object_fields() -> None:
    schema = {
        "type": "object",
        "properties": {
            "node": {"type": "string"},
            "vmid": {"type": "integer"},
            "status": {"type": "string", "enum": ["stopped", "running"]},
            "template": {"type": "boolean"},
            "maxmem": {"type": "integer"},
        },
    }
    value = sample_value_for_schema(schema, seed="obj_seed")
    assert isinstance(value, dict)
    assert value["status"] == "running"
    assert value["template"] is False
    assert value["maxmem"] == 16 * 1024**3
    assert isinstance(value["vmid"], int)
    assert value["node"].startswith("pve-node-")

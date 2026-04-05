# Benchmark

### `proxmox benchmark --help`

**Input:**

```bash
proxmox benchmark --help
```

**Output:**

```text

 Usage: proxmox benchmark [OPTIONS]

 Benchmark API performance.

 Example:
 proxmox benchmark --path /nodes
 proxmox benchmark --path /nodes --iterations 10
 proxmox benchmark --backend https --path /nodes/pve1/qemu

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --iterations          INTEGER  Number of iterations to run [default: 5]      │
│ --path                TEXT     API path to benchmark [default: /nodes]       │
│ --backend             TEXT     Backend to use                                │
│ --output      -o      TEXT     Output format (human, json, yaml, markdown,   │
│                                table, text, raw)                             │
│ --json                         Shortcut for --output json                    │
│ --yaml                         Shortcut for --output yaml                    │
│ --markdown                     Shortcut for --output markdown                │
│ --help                         Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `8.261`

---

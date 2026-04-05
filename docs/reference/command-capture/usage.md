# Usage

### `proxmox usage --help`

**Input:**

```bash
proxmox usage --help
```

**Output:**

```text

 Usage: proxmox usage [OPTIONS] PATH

 Show API schema and usage information for an endpoint.

 Examples:
 proxmox usage /nodes/pve1/qemu/100
 proxmox usage /nodes/pve1/qemu/100 --command GET
 proxmox usage /nodes/pve1/qemu/100 --command POST --returns

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to get usage for [required]                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --command           TEXT  HTTP method to inspect (GET, POST, PUT, DELETE)    │
│ --returns                 Include return schema                              │
│ --verbose   -v            Verbose output                                     │
│ --output    -o      TEXT  Output format (human, json, yaml, markdown, table, │
│                           text, raw)                                         │
│ --json                    Shortcut for --output json                         │
│ --yaml                    Shortcut for --output yaml                         │
│ --markdown                Shortcut for --output markdown                     │
│ --help                    Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `8.806`

---

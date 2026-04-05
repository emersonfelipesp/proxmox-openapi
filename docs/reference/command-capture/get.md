# Get

### `proxmox get --help`

**Input:**

```bash
proxmox get --help
```

**Output:**

```text

 Usage: proxmox get [OPTIONS] PATH

 Retrieve resources from the Proxmox API.

 Examples:
 proxmox get /nodes
 proxmox get /nodes/pve1/status
 proxmox get /nodes/pve1/qemu --output json

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to retrieve [required]                         │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --columns   -c      TEXT  Comma-separated columns to display                 │
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

**Exit code:** `0`  ·  **Wall time (s):** `8.960`

---

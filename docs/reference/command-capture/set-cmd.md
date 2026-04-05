# Set Cmd

### `proxmox set-cmd --help`

**Input:**

```bash
proxmox set-cmd --help
```

**Output:**

```text

 Usage: proxmox set-cmd [OPTIONS] PATH

 Update resources in the Proxmox API.

 Examples:
 proxmox set /nodes/pve1 -d description=Node1
 proxmox set /nodes/pve1 -d description=Node1 -d features=snapshot,nesting
 proxmox set /nodes/pve1 -f updates.json

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to update [required]                           │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --data       -d      TEXT  Data parameter (key=value, can be repeated)       │
│ --json-file  -f      TEXT  JSON file with parameters                         │
│ --output     -o      TEXT  Output format (human, json, yaml, markdown,       │
│                            table, text, raw)                                 │
│ --json                     Shortcut for --output json                        │
│ --yaml                     Shortcut for --output yaml                        │
│ --markdown                 Shortcut for --output markdown                    │
│ --help                     Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `9.247`

---

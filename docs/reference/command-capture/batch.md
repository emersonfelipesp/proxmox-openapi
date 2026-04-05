# Batch

### `proxmox batch --help`

**Input:**

```bash
proxmox batch --help
```

**Output:**

```text

 Usage: proxmox batch [OPTIONS] FILE

 Execute batch operations from a JSON file.

 Batch file format:
 ```json
 {
   "operations": [
     {"action": "get", "path": "/nodes"},
     {"action": "create", "path": "/nodes/pve1/qemu/100", "params": {"vmid":
 100}},
     {"action": "set", "path": "/nodes/pve1/qemu/100", "params": {"cores": 4}}
   ]
 }
 ```

 Example:
     proxmox batch operations.json
     proxmox batch operations.json --dry-run
     proxmox batch operations.json --continue-on-error

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    file      TEXT  JSON file with batch operations [required]              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --dry-run                --no-dry-run                  Show what would be    │
│                                                        executed              │
│                                                        [default: no-dry-run] │
│ --continue-on-error      --no-continue-on-er…          Continue if operation │
│                                                        fails                 │
│                                                        [default:             │
│                                                        no-continue-on-error] │
│ --backend                                        TEXT  Backend to use        │
│ --output             -o                          TEXT  Output format (human, │
│                                                        json, yaml, markdown, │
│                                                        table, text, raw)     │
│ --json                                                 Shortcut for --output │
│                                                        json                  │
│ --yaml                                                 Shortcut for --output │
│                                                        yaml                  │
│ --markdown                                             Shortcut for --output │
│                                                        markdown              │
│ --help                                                 Show this message and │
│                                                        exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `8.079`

---

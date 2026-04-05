# Config Remove

### `proxmox config-remove --help`

**Input:**

```bash
proxmox config-remove --help
```

**Output:**

```text

 Usage: proxmox config-remove [OPTIONS] NAME

 Remove a configuration profile.

 Example:
 proxmox config-remove staging
 proxmox config-remove staging --force

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    name      TEXT  Profile name [required]                                 │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --force     -f            Skip confirmation                                  │
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

**Exit code:** `0`  ·  **Wall time (s):** `8.481`

---

# Config Add

### `proxmox config-add --help`

**Input:**

```bash
proxmox config-add --help
```

**Output:**

```text

 Usage: proxmox config-add [OPTIONS] NAME

 Add a new configuration profile.

 Example:
 proxmox config-add staging --host proxmox-staging.example.com --user admin@pam
 proxmox config-add prod --backend https --host proxmox.example.com
 --token-name api-token

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    name      TEXT  Profile name [required]                                 │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --backend              TEXT     Backend type [default: https]             │
│ *  --host                 TEXT     Host address [required]                   │
│    --port                 INTEGER  Port number [default: 8006]               │
│    --user                 TEXT     Username                                  │
│    --token-name           TEXT     Token name                                │
│    --token-value          TEXT     Token value                               │
│    --service              TEXT     Service type (PVE/PMG/PBS) [default: PVE] │
│    --output       -o      TEXT     Output format (human, json, yaml,         │
│                                    markdown, table, text, raw)               │
│    --json                          Shortcut for --output json                │
│    --yaml                          Shortcut for --output yaml                │
│    --markdown                      Shortcut for --output markdown            │
│    --help                          Show this message and exit.               │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `8.182`

---

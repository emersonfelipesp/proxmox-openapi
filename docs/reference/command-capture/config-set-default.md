# Config Set Default

### `proxmox config-set-default --help`

**Input:**

```bash
proxmox config-set-default --help
```

**Output:**

```text
                                                                                
 Usage: proxmox config-set-default [OPTIONS] NAME                               
                                                                                
 Set the default profile.                                                       
                                                                                
 Example:                                                                       
 proxmox config-set-default staging                                             
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    name      TEXT  Profile name to set as default [required]               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
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

**Exit code:** `0`  ·  **Wall time (s):** `8.187`

---

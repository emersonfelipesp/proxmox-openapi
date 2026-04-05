# Config List

### `proxmox config-list --help`

**Input:**

```bash
proxmox config-list --help
```

**Output:**

```text
                                                                                
 Usage: proxmox config-list [OPTIONS]                                           
                                                                                
 List all available configuration profiles.                                     
                                                                                
 Example:                                                                       
 proxmox config-list                                                            
                                                                                
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

**Exit code:** `0`  ·  **Wall time (s):** `8.280`

---

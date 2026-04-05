# Config Show

### `proxmox config-show --help`

**Input:**

```bash
proxmox config-show --help
```

**Output:**

```text
                                                                                
 Usage: proxmox config-show [OPTIONS] [PROFILE]                                 
                                                                                
 Show configuration for a specific profile.                                     
                                                                                
 Example:                                                                       
 proxmox config-show default                                                    
 proxmox config-show staging                                                    
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   profile      [PROFILE]  Profile name [default: default]                    │
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

**Exit code:** `0`  ·  **Wall time (s):** `8.258`

---

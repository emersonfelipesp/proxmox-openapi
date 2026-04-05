# Help Cmd

### `proxmox help-cmd --help`

**Input:**

```bash
proxmox help-cmd --help
```

**Output:**

```text
                                                                                
 Usage: proxmox help-cmd [OPTIONS] [PATH]                                       
                                                                                
 Show help for API endpoints.                                                   
                                                                                
 Examples:                                                                      
 proxmox help                                                                   
 proxmox help /nodes                                                            
 proxmox help /nodes/pve1/qemu                                                  
 proxmox help --search qemu                                                     
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   path      [PATH]  API path to get help for                                 │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --search    -s      TEXT  Search for endpoints matching pattern              │
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

**Exit code:** `0`  ·  **Wall time (s):** `9.397`

---

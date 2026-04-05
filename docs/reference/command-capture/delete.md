# Delete

### `proxmox delete --help`

**Input:**

```bash
proxmox delete --help
```

**Output:**

```text
                                                                                
 Usage: proxmox delete [OPTIONS] PATH                                           
                                                                                
 Delete resources from the Proxmox API.                                         
                                                                                
 Examples:                                                                      
 proxmox delete /nodes/pve1/qemu/100                                            
 proxmox delete /nodes/pve1/qemu/100 --force                                    
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to delete [required]                           │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --force     -f            Force deletion without confirmation                │
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

**Exit code:** `0`  ·  **Wall time (s):** `9.588`

---

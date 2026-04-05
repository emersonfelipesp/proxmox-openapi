# Create

### `proxmox create --help`

**Input:**

```bash
proxmox create --help
```

**Output:**

```text
                                                                                
 Usage: proxmox create [OPTIONS] PATH                                           
                                                                                
 Create resources in the Proxmox API.                                           
                                                                                
 Examples:                                                                      
 proxmox create /nodes/pve1/qemu/100 --vmid 100 --name test-vm                  
 proxmox create /nodes/pve1/qemu/100 -d vmid=100 -d name=test-vm                
 proxmox create /nodes/pve1/qemu/100 -f params.json                             
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path where to create [required]                     │
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

**Exit code:** `0`  ·  **Wall time (s):** `8.436`

---

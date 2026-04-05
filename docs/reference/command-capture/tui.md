# Tui

### `proxmox tui --help`

**Input:**

```bash
proxmox tui --help
```

**Output:**

```text
                                                                                
 Usage: proxmox tui [OPTIONS] [MODE]:[mock]                                     
                                                                                
 Launch interactive Proxmox TUI.                                                
                                                                                
 Examples:                                                                      
 proxmox tui                                                                    
 proxmox tui mock                                                               
 pbx tui                                                                        
 pbx tui mock                                                                   
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   mode      [MODE]:[mock]  Optional mode. Use 'mock' to run TUI against      │
│                            in-memory mock backend.                           │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --path  -p      TEXT  Initial API path to load in the TUI. [default: /nodes] │
│ --help                Show this message and exit.                            │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `8.667`

---

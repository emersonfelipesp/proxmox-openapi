# Perf Test

### `proxmox perf-test --help`

**Input:**

```bash
proxmox perf-test --help
```

**Output:**

```text
                                                                                
 Usage: proxmox perf-test [OPTIONS] [OPERATION]                                 
                                                                                
 Run performance tests.                                                         
                                                                                
 Example:                                                                       
 proxmox perf-test get --iterations 20                                          
 proxmox perf-test list                                                         
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   operation      [OPERATION]  Operation type (get/create/list)               │
│                               [default: get]                                 │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --iterations          INTEGER  Number of iterations [default: 10]            │
│ --output      -o      TEXT     Output format (human, json, yaml, markdown,   │
│                                table, text, raw)                             │
│ --json                         Shortcut for --output json                    │
│ --yaml                         Shortcut for --output yaml                    │
│ --markdown                     Shortcut for --output markdown                │
│ --help                         Show this message and exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `8.146`

---

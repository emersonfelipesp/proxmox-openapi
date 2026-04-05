# Top-level

### `proxmox --help`

**Input:**

```bash
proxmox --help
```

**Output:**

```text
                                                                                
 Usage: proxmox [OPTIONS] COMMAND [ARGS]...                                     
                                                                                
 Proxmox VE, PMG, and PBS CLI - A pvesh-like interface for Proxmox API          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version                                    Show version and exit           │
│ --verbose             -v                     Enable verbose logging          │
│ --quiet               -q                     Suppress non-essential output   │
│ --config              -c      TEXT           Path to configuration file      │
│ --backend             -b      TEXT           Backend to use (https,          │
│                                              ssh_paramiko, openssh, local,   │
│                                              mock)                           │
│ --host                -H      TEXT           Proxmox host address            │
│ --user                -U      TEXT           Username or token name          │
│ --password            -P      TEXT           Password (insecure, prefer      │
│                                              token)                          │
│ --token-value                 TEXT           API token value                 │
│ --port                        INTEGER        API port (default: 8006)        │
│ --service             -S      [PVE|PMG|PBS]  Proxmox service type            │
│                                              [default: PVE]                  │
│ --output              -o      TEXT           Output format (human, json,     │
│                                              yaml, markdown, table, text,    │
│                                              raw)                            │
│ --json                                       Shortcut for --output json      │
│ --yaml                                       Shortcut for --output yaml      │
│ --markdown                                   Shortcut for --output markdown  │
│ --install-completion                         Install completion for the      │
│                                              current shell.                  │
│ --show-completion                            Show completion for the current │
│                                              shell, to copy it or customize  │
│                                              the installation.               │
│ --help                                       Show this message and exit.     │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ batch               Execute batch operations from a JSON file.               │
│ create              Create resources in the Proxmox API.                     │
│ delete              Delete resources from the Proxmox API.                   │
│ get                 Retrieve resources from the Proxmox API.                 │
│ help-cmd            Show help for API endpoints.                             │
│ ls                  List child resources at a given path.                    │
│ set-cmd             Update resources in the Proxmox API.                     │
│ tui                 Launch interactive Proxmox TUI.                          │
│ usage               Show API schema and usage information for an endpoint.   │
│ completion-install  Install shell completion for proxmox CLI.                │
│ config-list         List all available configuration profiles.               │
│ config-show         Show configuration for a specific profile.               │
│ config-add          Add a new configuration profile.                         │
│ config-remove       Remove a configuration profile.                          │
│ config-set-default  Set the default profile.                                 │
│ benchmark           Benchmark API performance.                               │
│ perf-test           Run performance tests.                                   │
│ docs                Generate CLI documentation artifacts for MkDocs.         │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `8.293`

---

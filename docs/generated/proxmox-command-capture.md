# Proxmox CLI - captured command input and output

This file is machine-generated. Regenerate with:

```bash
cd /path/to/proxmox-openapi
uv sync --group dev --group docs --extra cli
uv run proxmox docs generate-capture
# or: uv run python docs/generate_command_docs.py
```

## Generation metadata

- **UTC time:** `2026-04-05T01:14:34.729455+00:00`
- **Subprocess command:** `/root/nms/proxmox-openapi/.venv/bin/proxmox`

---

## Top-level

### proxmox --help

**Input:**

```bash
proxmox --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.293`

*Output truncated for this doc (max 40 lines / 20000 chars).*

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

... (19 more lines truncated)
```

---

## Batch

### proxmox batch --help

**Input:**

```bash
proxmox batch --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.079`

*Output truncated for this doc (max 40 lines / 20000 chars).*

**Output:**

```text
                                                                                
 Usage: proxmox batch [OPTIONS] FILE                                            
                                                                                
 Execute batch operations from a JSON file.                                     
                                                                                
 Batch file format:                                                             
 ```json                                                                        
 {                                                                              
   "operations": [                                                              
     {"action": "get", "path": "/nodes"},                                       
     {"action": "create", "path": "/nodes/pve1/qemu/100", "params": {"vmid":    
 100}},                                                                         
     {"action": "set", "path": "/nodes/pve1/qemu/100", "params": {"cores": 4}}  
   ]                                                                            
 }                                                                              
 ```                                                                            
                                                                                
 Example:                                                                       
     proxmox batch operations.json                                              
     proxmox batch operations.json --dry-run                                    
     proxmox batch operations.json --continue-on-error                          
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    file      TEXT  JSON file with batch operations [required]              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --dry-run                --no-dry-run                  Show what would be    │
│                                                        executed              │
│                                                        [default: no-dry-run] │
│ --continue-on-error      --no-continue-on-er…          Continue if operation │
│                                                        fails                 │
│                                                        [default:             │
│                                                        no-continue-on-error] │
│ --backend                                        TEXT  Backend to use        │
│ --output             -o                          TEXT  Output format (human, │
│                                                        json, yaml, markdown, │
│                                                        table, text, raw)     │
│ --json                                                 Shortcut for --output │
│                                                        json                  │
│ --yaml                                                 Shortcut for --output │

... (11 more lines truncated)
```

---

## Benchmark

### proxmox benchmark --help

**Input:**

```bash
proxmox benchmark --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.261`

**Output:**

```text
                                                                                
 Usage: proxmox benchmark [OPTIONS]                                             
                                                                                
 Benchmark API performance.                                                     
                                                                                
 Example:                                                                       
 proxmox benchmark --path /nodes                                                
 proxmox benchmark --path /nodes --iterations 10                                
 proxmox benchmark --backend https --path /nodes/pve1/qemu                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --iterations          INTEGER  Number of iterations to run [default: 5]      │
│ --path                TEXT     API path to benchmark [default: /nodes]       │
│ --backend             TEXT     Backend to use                                │
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

---

## Completion Install

### proxmox completion-install --help

**Input:**

```bash
proxmox completion-install --help
```

**Exit code:** `0`  ·  **Wall time (s):** `9.143`

**Output:**

```text
                                                                                
 Usage: proxmox completion-install [OPTIONS]                                    
                                                                                
 Install shell completion for proxmox CLI.                                      
                                                                                
 Examples:                                                                      
 # Bash                                                                         
 proxmox completion-install --shell bash >> ~/.bashrc                           
                                                                                
 # Zsh                                                                          
 proxmox completion-install --shell zsh >> ~/.zshrc                             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --shell        TEXT  Shell type (bash or zsh) [default: bash]                │
│ --help               Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

---

## Config Add

### proxmox config-add --help

**Input:**

```bash
proxmox config-add --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.182`

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

---

## Config List

### proxmox config-list --help

**Input:**

```bash
proxmox config-list --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.280`

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

---

## Config Remove

### proxmox config-remove --help

**Input:**

```bash
proxmox config-remove --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.481`

**Output:**

```text
                                                                                
 Usage: proxmox config-remove [OPTIONS] NAME                                    
                                                                                
 Remove a configuration profile.                                                
                                                                                
 Example:                                                                       
 proxmox config-remove staging                                                  
 proxmox config-remove staging --force                                          
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    name      TEXT  Profile name [required]                                 │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --force     -f            Skip confirmation                                  │
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

---

## Config Set Default

### proxmox config-set-default --help

**Input:**

```bash
proxmox config-set-default --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.187`

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

---

## Config Show

### proxmox config-show --help

**Input:**

```bash
proxmox config-show --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.258`

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

---

## Create

### proxmox create --help

**Input:**

```bash
proxmox create --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.436`

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

---

## Delete

### proxmox delete --help

**Input:**

```bash
proxmox delete --help
```

**Exit code:** `0`  ·  **Wall time (s):** `9.588`

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

---

## Docs

### proxmox docs --help

**Input:**

```bash
proxmox docs --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.740`

**Output:**

```text
                                                                                
 Usage: proxmox docs [OPTIONS] COMMAND [ARGS]...                                
                                                                                
 Generate CLI documentation artifacts for MkDocs.                               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ generate-capture  Capture proxmox CLI command input/output recursively from  │
│                   the command tree.                                          │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

---

### proxmox docs generate-capture --help

**Input:**

```bash
proxmox docs generate-capture --help
```

**Exit code:** `0`  ·  **Wall time (s):** `7.891`

**Output:**

```text
                                                                                
 Usage: proxmox docs generate-capture [OPTIONS]                                 
                                                                                
 Capture proxmox CLI command input/output recursively from the command tree.    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --output     -o      PATH     Markdown output path (default:                 │
│                               <repo>/docs/generated/proxmox-command-capture… │
│ --raw-dir            PATH     JSON artifact directory (default:              │
│                               <repo>/docs/generated/raw).                    │
│ --max-lines          INTEGER  Max lines per output block in the generated    │
│                               Markdown.                                      │
│                               [default: 200]                                 │
│ --max-chars          INTEGER  Max characters per output block in the         │
│                               generated Markdown.                            │
│                               [default: 120000]                              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

---

## Get

### proxmox get --help

**Input:**

```bash
proxmox get --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.960`

**Output:**

```text
                                                                                
 Usage: proxmox get [OPTIONS] PATH                                              
                                                                                
 Retrieve resources from the Proxmox API.                                       
                                                                                
 Examples:                                                                      
 proxmox get /nodes                                                             
 proxmox get /nodes/pve1/status                                                 
 proxmox get /nodes/pve1/qemu --output json                                     
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to retrieve [required]                         │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --columns   -c      TEXT  Comma-separated columns to display                 │
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

---

## Help Cmd

### proxmox help-cmd --help

**Input:**

```bash
proxmox help-cmd --help
```

**Exit code:** `0`  ·  **Wall time (s):** `9.397`

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

---

## Ls

### proxmox ls --help

**Input:**

```bash
proxmox ls --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.796`

**Output:**

```text
                                                                                
 Usage: proxmox ls [OPTIONS] PATH                                               
                                                                                
 List child resources at a given path.                                          
                                                                                
 Examples:                                                                      
 proxmox ls /nodes                                                              
 proxmox ls /nodes/pve1/qemu                                                    
 proxmox ls /nodes/pve1/qemu --columns vmid,name,status                         
 proxmox ls /nodes/pve1/qemu --sort name                                        
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to list [required]                             │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --columns   -c      TEXT  Comma-separated columns to display                 │
│ --sort              TEXT  Field to sort by                                   │
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

---

## Perf Test

### proxmox perf-test --help

**Input:**

```bash
proxmox perf-test --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.146`

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

---

## Set Cmd

### proxmox set-cmd --help

**Input:**

```bash
proxmox set-cmd --help
```

**Exit code:** `0`  ·  **Wall time (s):** `9.247`

**Output:**

```text
                                                                                
 Usage: proxmox set-cmd [OPTIONS] PATH                                          
                                                                                
 Update resources in the Proxmox API.                                           
                                                                                
 Examples:                                                                      
 proxmox set /nodes/pve1 -d description=Node1                                   
 proxmox set /nodes/pve1 -d description=Node1 -d features=snapshot,nesting      
 proxmox set /nodes/pve1 -f updates.json                                        
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to update [required]                           │
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

---

## Tui

### proxmox tui --help

**Input:**

```bash
proxmox tui --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.667`

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

---

## Usage

### proxmox usage --help

**Input:**

```bash
proxmox usage --help
```

**Exit code:** `0`  ·  **Wall time (s):** `8.806`

**Output:**

```text
                                                                                
 Usage: proxmox usage [OPTIONS] PATH                                            
                                                                                
 Show API schema and usage information for an endpoint.                         
                                                                                
 Examples:                                                                      
 proxmox usage /nodes/pve1/qemu/100                                             
 proxmox usage /nodes/pve1/qemu/100 --command GET                               
 proxmox usage /nodes/pve1/qemu/100 --command POST --returns                    
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to get usage for [required]                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --command           TEXT  HTTP method to inspect (GET, POST, PUT, DELETE)    │
│ --returns                 Include return schema                              │
│ --verbose   -v            Verbose output                                     │
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

---

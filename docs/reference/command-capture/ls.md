# Ls

### `proxmox ls --help`

**Input:**

```bash
proxmox ls --help
```

**Output:**

```text

 Usage: proxmox ls [OPTIONS] PATH

 List child resources at a given path.

 Examples:
 proxmox ls /nodes
 proxmox ls /nodes/pve1/qemu
 proxmox ls /nodes/pve1/qemu --columns vmid,name,status
 proxmox ls /nodes/pve1/qemu --sort name --reverse
 proxmox ls /nodes/pve1/qemu --filter status=running
 proxmox ls /nodes/pve1/qemu --limit 10 --offset 20
 proxmox ls /nodes --watch 5

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    path      TEXT  API path to list [required]                             │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --columns   -c      TEXT     Comma-separated columns to display              │
│ --sort              TEXT     Field to sort by                                │
│ --reverse   -r               Sort in reverse order                           │
│ --limit     -l      INTEGER  Maximum number of results to return             │
│ --offset            INTEGER  Number of results to skip (for pagination)      │
│ --filter    -f      TEXT     Filter results (field=value or field~substring) │
│ --watch     -w      INTEGER  Refresh every N seconds (Ctrl+C to stop)        │
│ --output    -o      TEXT     Output format (human, json, yaml, markdown,     │
│                              table, text, raw)                               │
│ --json                       Shortcut for --output json                       │
│ --yaml                       Shortcut for --output yaml                       │
│ --markdown                   Shortcut for --output markdown                   │
│ --help                       Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯


--- stderr ---
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
<string>:540: UserWarning: Field name "schema" in "GetClusterAcmeChallengeSchemaResponseItem" shadows an attribute in parent "ProxmoxBaseModel"
```

**Exit code:** `0`  ·  **Wall time (s):** `8.796`

---

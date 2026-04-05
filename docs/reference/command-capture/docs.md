# Docs

### `proxmox docs --help`

**Input:**

```bash
proxmox docs --help
```

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

**Exit code:** `0`  ·  **Wall time (s):** `8.740`

---

### `proxmox docs generate-capture --help`

**Input:**

```bash
proxmox docs generate-capture --help
```

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

**Exit code:** `0`  ·  **Wall time (s):** `7.891`

---

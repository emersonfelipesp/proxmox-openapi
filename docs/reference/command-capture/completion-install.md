# Completion Install

### `proxmox completion-install --help`

**Input:**

```bash
proxmox completion-install --help
```

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

**Exit code:** `0`  ·  **Wall time (s):** `9.143`

---

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

## TUI Enhanced Features (v0.0.2)

The TUI now includes enhanced navigation and viewing capabilities:

### Keyboard Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| `q` | Quit | Exit the TUI |
| `r` | Refresh | Reload current view |
| `i` | Focus input | Focus command input |
| `f` | Filter | Toggle filter bar |
| `t` | Tree | Toggle navigation tree |
| `/` | Search | Focus filter bar |
| `Esc` | Close filter | Close filter bar |
| `j` | Down | Navigate down |
| `k` | Up | Navigate up |
| `l` | Right/Expand | Expand tree node or select |
| `h` | Left/Collapse | Collapse tree node |
| `Ctrl+L` | Clear | Clear output |

### Features

1. **Tree Navigation Panel** - Browse hierarchical paths (Nodes → pve1 → qemu)
2. **JSON Viewer** - View API responses in formatted JSON with TextArea
3. **Filter Bar** - Real-time filtering of results (press `/` to focus)
4. **Split View** - Tree on left, details on right (toggle with `t`)

---

# PVESH: Structured Review

## Scope and Source

This document is a structured review of the Proxmox VE `pvesh` command-line package, based on the official manual page:

- Source: https://pve.proxmox.com/pve-docs/pvesh.1.html
- Reviewed manual version: 9.1.2 (last updated Fri Dec 12 13:18:26 UTC 2025)

## Executive Summary

`pvesh` is a local shell interface to the Proxmox VE API. It allows direct invocation of API methods from the Proxmox host without going through the REST/HTTPS endpoint as an external client. Conceptually, it maps CRUD-like CLI verbs to API operations:

- `get` -> HTTP GET
- `create` -> HTTP POST
- `set` -> HTTP PUT
- `delete` -> HTTP DELETE

The tool is intentionally low-level and API-centric. It is best suited for administration workflows, troubleshooting, introspection, and scripting on Proxmox hosts.

A critical operational constraint is explicitly documented: only `root` is allowed to use it.

## What pvesh Is (and Is Not)

### What it is

- A direct API shell for Proxmox VE.
- A discovery tool (`ls`, `usage`, `help`) for endpoint exploration.
- A data retrieval and mutation interface with selectable output formats.

### What it is not

- Not a remote client SDK by itself.
- Not intended as a replacement for role-scoped remote API consumers.
- Not an abstraction layer that hides API paths and schemas.

## Command Surface

## Global Form

```bash
pvesh <COMMAND> [ARGS] [OPTIONS]
```

## Core Subcommands and API Mapping

### `pvesh get <api_path> [OPTIONS] [FORMAT_OPTIONS]`

- Purpose: call API GET on `<api_path>`.
- Typical usage: reads/listing/detail retrieval.

### `pvesh create <api_path> [OPTIONS] [FORMAT_OPTIONS]`

- Purpose: call API POST on `<api_path>`.
- Typical usage: create/start/action-style API calls.

### `pvesh set <api_path> [OPTIONS] [FORMAT_OPTIONS]`

- Purpose: call API PUT on `<api_path>`.
- Typical usage: updates/overwrites configuration.

### `pvesh delete <api_path> [OPTIONS] [FORMAT_OPTIONS]`

- Purpose: call API DELETE on `<api_path>`.
- Typical usage: remove objects or clear configuration.

### `pvesh ls <api_path> [OPTIONS] [FORMAT_OPTIONS]`

- Purpose: list child objects under `<api_path>`.
- Typical usage: navigate API hierarchy.

### `pvesh usage <api_path> [OPTIONS]`

- Purpose: print API usage/schema information for an endpoint.
- Notable options:
  - `--command <create | delete | get | set>` to inspect method-specific schema.
  - `--returns <boolean>` to include return schema.
  - `--verbose <boolean>` for expanded output.

### `pvesh help [OPTIONS]`

- Purpose: command help.
- Notable options:
  - `--extra-args <array>` for command-specific help path.
  - `--verbose <boolean>` for richer help output.

## Shared Options by API-Calling Verbs

For `get/create/set/delete/ls`, the man page documents:

- `<api_path>: <string>` API path.
- `--noproxy <boolean>` disable automatic proxying.

## Output and Rendering Model (FORMAT_OPTIONS)

`pvesh` supports explicit output controls, which are central for automation quality.

### Output format

- `--output-format <json | json-pretty | text | yaml>` (default: `text`)

### Text rendering controls

- `--human-readable <boolean>` (default: `1`)
- `--noborder <boolean>` (default: `0`)
- `--noheader <boolean>` (default: `0`)

### Silent mode

- `--quiet <boolean>` suppress result printing.

### Human-readable transformations in text mode

The default text mode applies presentation transforms, including:

- Unix epoch -> ISO 8601 date string
- Duration values -> compact duration form (for example `1d 5h`)
- Byte values -> unitized values (`B`, `KiB`, `MiB`, `GiB`, `TiB`, `PiB`)
- Fractions -> percentage rendering (`1.0` shown as `100%`)

## Official Examples (from man page)

```bash
# List nodes in the cluster
pvesh get /nodes

# Inspect available options for datacenter cluster options
pvesh usage cluster/options -v

# Set HTML5 NoVNC as default datacenter console
pvesh set cluster/options -console html5
```

## Behavioral Review

## Strengths

### 1) Directness and fidelity to API semantics

The command verbs and API paths preserve API intent clearly. Operators can move between API docs and CLI with minimal translation overhead.

### 2) Discoverability from the host

`ls` and `usage` make endpoint discovery and schema inspection fast during incident response or live administration.

### 3) Automation-friendly output controls

JSON/YAML support and suppressible text formatting allow integration into shell pipelines and tooling.

### 4) Low additional dependency surface

As part of the Proxmox toolchain, `pvesh` is available where Proxmox administration is already performed.

## Limitations and Risk Areas

### 1) Privilege model is strict

`root`-only access is secure by default but limits delegated operations and requires careful operational governance.

### 2) Path-first UX has a learning curve

Users must know API path structure (`/nodes/...`) and endpoint semantics; this can be error-prone without discovery discipline.

### 3) Text output defaults can surprise scripts

The `text` default and human-readable transforms are ideal for humans but may introduce parsing ambiguity in scripts if not switched to JSON/YAML.

### 4) API-first behavior means low guardrails

The tool exposes backend operations closely; incorrect path or parameters can lead to immediate configuration impact.

## Security and Operations Notes

- Access control: only root can execute `pvesh` per official docs.
- Recommended for scripts: use `--output-format json` for deterministic parsing.
- For high-safety workflows: prefer read-first then mutate pattern.
  - Example flow: `usage` -> `get` -> `set/create/delete`.
- For change validation: pair write operations with immediate read-back using `get`.

## Practical Usage Patterns

### Endpoint exploration

```bash
pvesh ls /
pvesh ls /nodes
pvesh usage /nodes --command get --returns 1 --verbose 1
```

### Deterministic automation output

```bash
pvesh get /nodes --output-format json
pvesh get /cluster/resources --output-format json-pretty
```

### Quiet write operations in scripts

```bash
pvesh set cluster/options -console html5 --quiet 1
```

### Human-facing CLI output cleanup

```bash
pvesh get /nodes --output-format text --noborder 1 --noheader 1
```

## Relevance to proxmox-openapi

For this project, `pvesh` is useful as a practical validation and cross-check interface when comparing generated OpenAPI artifacts against live Proxmox behavior on a host.

Recommended integration mindset:

- Use `pvesh usage` output to verify expected method/path/parameter surfaces.
- Use `pvesh get` snapshots as reference points for response shape sanity checks.
- Keep comparisons version-aware, since Proxmox endpoint behavior evolves across releases.

## Suggested Validation Checklist

When evaluating endpoint coverage or generated schema quality:

1. Confirm endpoint exists with `pvesh ls` and `pvesh usage`.
2. Confirm command method compatibility (`get/create/set/delete`).
3. Capture response in JSON (`--output-format json`) for stable comparison.
4. Validate documented return schema hints (`--returns 1`) against observed fields.
5. Repeat on targeted Proxmox versions to identify drift.

## Conclusion

`pvesh` is a powerful, direct administrative interface for Proxmox VE API access on the host. Its strengths are transparency, introspection, and operational speed. Its main constraints are privilege requirements and the need for API-path literacy.

For automation and tooling ecosystems such as proxmox-openapi, `pvesh` is best treated as a high-fidelity local probe for endpoint discovery and behavior verification.

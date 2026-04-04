# Proxmoxer: Python Wrapper for Proxmox REST API

## Overview

**Proxmoxer** is a comprehensive Python wrapper around the Proxmox REST API v2 that provides a dynamic, Pythonic interface for interacting with Proxmox services.

### Key Information

- **Current Version**: 2.3.0 (released March 4, 2026)
- **Author**: Oleg Butovich
- **License**: MIT
- **Repository**: https://github.com/proxmoxer/proxmoxer
- **Documentation**: https://proxmoxer.github.io/docs/
- **PyPI**: https://pypi.python.org/pypi/proxmoxer

### Supported Proxmox Services

Proxmoxer supports multiple Proxmox products:

1. **PVE** (Proxmox Virtual Environment) - Full support
2. **PMG** (Proxmox Mail Gateway) - Full support  
3. **PBS** (Proxmox Backup Server) - HTTPS backend only

### Design Philosophy

Proxmoxer was inspired by [slumber](https://github.com/samgiles/slumber) but is dedicated exclusively to Proxmox. Like [Proxmoxia](https://github.com/baseblack/Proxmoxia), it dynamically creates attributes based on API paths, allowing natural Python navigation of the Proxmox API hierarchy.

**Key Design Principles:**

- **Dynamic attribute creation** - API paths become Python attributes
- **Multiple backends** - Same API over HTTPS, SSH, or local pvesh
- **Minimal dependencies** - Core library is lightweight
- **RESTful operations** - Clean mapping to HTTP verbs
- **Service-agnostic** - Single codebase supports PVE, PMG, and PBS

---

## Architecture

### Core Components

Proxmoxer's architecture consists of four main layers:

```
┌─────────────────────────────────────────┐
│         ProxmoxAPI (Entry Point)        │
│  - Service validation                   │
│  - Backend selection & initialization   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      ProxmoxResource (Navigation)       │
│  - Dynamic attribute generation         │
│  - URL building (posixpath)             │
│  - HTTP method mapping                  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Backend Layer (Abstraction)      │
│  ┌─────────┬──────────┬──────────────┐  │
│  │ HTTPS   │ SSH      │ Local        │  │
│  │ Backend │ Backends │ Backend      │  │
│  └─────────┴──────────┴──────────────┘  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Session & Serialization Layer      │
│  - Request/response handling            │
│  - JSON serialization                   │
│  - Error handling                       │
└─────────────────────────────────────────┘
```

#### 1. ProxmoxAPI (core.py)

**Purpose**: Main entry point and backend orchestration

**Responsibilities:**
- Validate service type (PVE/PMG/PBS)
- Verify backend compatibility with service
- Dynamically import and initialize backend
- Inherit from `ProxmoxResource` to provide API navigation

**Key Methods:**
```python
def __init__(self, host=None, backend="https", service="PVE", **kwargs)
def get_tokens(self)  # Returns auth/csrf tokens for https backend
```

**Example:**
```python
from proxmoxer import ProxmoxAPI

# HTTPS backend (default)
proxmox = ProxmoxAPI('proxmox.example.com', 
                     user='admin@pam', 
                     password='secret',
                     verify_ssl=False)

# SSH backend
proxmox = ProxmoxAPI('proxmox.example.com',
                     user='root',
                     backend='ssh_paramiko',
                     service='PVE')

# Local backend (on Proxmox host itself)
proxmox = ProxmoxAPI(backend='local', service='PVE')
```

#### 2. ProxmoxResource (core.py)

**Purpose**: Dynamic resource navigation and HTTP operations

**Responsibilities:**
- Build API URLs using attribute access
- Handle resource IDs (strings, lists, tuples)
- Execute HTTP methods (GET, POST, PUT, DELETE)
- Filter None values from params/data
- Delegate requests to backend session

**Key Methods:**
```python
def __getattr__(self, item)           # Create sub-resources
def __call__(self, resource_id=None)  # Add resource IDs to path
def url_join(self, base, *args)       # Build URLs with posixpath
def _request(self, method, data=None, params=None)  # Execute requests
def get/post/put/delete(*args, **params)  # HTTP verbs
def create/set(*args, **data)         # Aliases for post/put
```

**Dynamic Navigation Example:**
```python
# API path: /api2/json/nodes/pve1/qemu/100/status/current
# Proxmoxer equivalent:
status = proxmox.nodes('pve1').qemu('100').status.current.get()

# Or with parameters:
status = proxmox.nodes.pve1.qemu(100).status.current.get()
```

**URL Building Logic:**
- Uses `urllib.parse.urlsplit` and `posixpath.join`
- Preserves scheme, netloc, query, and fragment
- Handles nested paths cleanly
- Converts all arguments to strings

#### 3. Backend Abstraction Layer

Each backend implements three required methods:

```python
def get_base_url(self)    # Returns API base URL
def get_session(self)     # Returns session/client object
def get_serializer(self)  # Returns JSON serializer
```

**Service Configuration (SERVICES dict):**

```python
SERVICES = {
    "PVE": {
        "supported_backends": ["local", "https", "openssh", "ssh_paramiko"],
        "supported_https_auths": ["password", "token"],
        "default_port": 8006,
        "token_separator": "=",
        "cli_additional_options": ["--output-format", "json"],
    },
    "PMG": {
        "supported_backends": ["local", "https", "openssh", "ssh_paramiko"],
        "supported_https_auths": ["password"],
        "default_port": 8006,
    },
    "PBS": {
        "supported_backends": ["https"],
        "supported_https_auths": ["password", "token"],
        "default_port": 8007,
        "token_separator": ":",
    },
}
```

---

## Backend Implementations

### 1. HTTPS Backend (backends/https.py)

**Default backend** - Uses the `requests` library for HTTP/HTTPS communication.

**Dependencies:** `requests` (required)

**Features:**
- User/password authentication with ticket renewal
- API token authentication
- Two-factor authentication (TOTP/OTP)
- Automatic ticket refresh (every 3600 seconds)
- Large file uploads (>10 MiB streaming with `requests_toolbelt`)
- SSL/TLS verification control
- Client certificate support
- HTTP proxy support
- IPv6 support

#### Authentication Methods

##### Password Authentication (ProxmoxHTTPAuth)

**Features:**
- Initial authentication via `/access/ticket`
- Automatic ticket refresh before expiration
- CSRF token management
- Two-factor authentication support

**Flow:**
1. POST to `/access/ticket` with username/password
2. Receive `ticket` and `CSRFPreventionToken`
3. Store ticket in cookie (`PVEAuthCookie`/`PMGAuthCookie`/`PBSAuthCookie`)
4. Add CSRF token to non-GET request headers
5. Auto-refresh ticket after 3600 seconds (1 hour)

**Two-Factor Authentication:**
- Detects `NeedTFA` in initial response
- Sends second request with `tfa-challenge` and OTP code
- Supports `totp` (TOTP) and other OTP types

**Example:**
```python
# Basic authentication
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     verify_ssl=True)

# With OTP/2FA
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     otp='123456',        # OTP code
                     otptype='totp',      # OTP type (default: totp)
                     verify_ssl=True)

# With client certificate
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     cert='/path/to/cert.pem',
                     verify_ssl=True)

# With HTTP proxy
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     proxies={'https': 'http://proxy.example.com:8080'})
```

##### API Token Authentication (ProxmoxHTTPApiTokenAuth)

**Features:**
- No ticket expiration
- No session management needed
- Simpler for automation/scripts

**Token Format:**
- PVE/PMG: `{service}APIToken={user}!{token_name}={token_value}`
- PBS: `PBSAPIToken={user}!{token_name}:{token_value}`

**Example:**
```python
proxmox = ProxmoxAPI('pve.example.com',
                     user='monitoring@pve',
                     token_name='api-token',
                     token_value='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
                     verify_ssl=True)
```

#### File Upload Handling

**Small Files (< 10 MiB):**
- Standard multipart/form-data
- All data loaded into memory

**Large Files (>= 10 MiB):**
- Streaming multipart encoding (requires `requests_toolbelt`)
- Uses `MultipartEncoder` for memory efficiency
- Supports files > 2 GiB (SSL overflow workaround)
- Falls back to standard upload if `requests_toolbelt` not installed

**File Detection:**
```python
# Automatically detects io.IOBase objects in data dict
# Moves them to files dict with proper Content-Type

data = {
    'filename': open('/path/to/iso', 'rb'),  # Will be streamed
    'content': 'iso',
}
result = proxmox.nodes('pve1').storage('local').upload.post(**data)
```

**Thresholds:**
```python
STREAMING_SIZE_THRESHOLD = 10 * 1024 * 1024  # 10 MiB
SSL_OVERFLOW_THRESHOLD = 2147483135  # 2^31 - 1 - 512
```

#### Session Management (ProxmoxHttpSession)

Custom `requests.Session` subclass with:
- Automatic auth from backend
- Cookie management from auth object
- SSL verification control
- Request timeout handling
- QEMU agent exec command splitting
- File stream detection and handling

**Special Handling:**
- QEMU agent exec commands are split using `shlex.split()` (except on Windows)
- Ensures proper argument parsing by Proxmox

#### IPv6 Support

**Automatic detection and formatting:**
```python
# Bare IPv6 address
ProxmoxAPI('2001:db8::1', ...)  # → https://[2001:db8::1]:8006/...

# IPv6 with port
ProxmoxAPI('[2001:db8::1]:8007', ...)  # → https://[2001:db8::1]:8007/...

# IPv6 in bracket notation
ProxmoxAPI('[2001:db8::1]', ...)  # → https://[2001:db8::1]:8006/...
```

#### Path Prefix Support

For reverse proxy or custom Proxmox installations:

```python
# URL: https://example.com/proxmox/api2/json/...
proxmox = ProxmoxAPI('example.com',
                     user='admin@pam',
                     password='secret',
                     path_prefix='proxmox')
```

### 2. SSH Backends (Paramiko & OpenSSH)

Execute Proxmox commands via SSH using the `pvesh` CLI utility.

#### ssh_paramiko Backend (backends/ssh_paramiko.py)

**Dependencies:** `paramiko` (required)

**Features:**
- Pure Python SSH implementation
- Password or key-based authentication
- SFTP for file uploads
- Cross-platform compatibility

**Example:**
```python
# Password authentication
proxmox = ProxmoxAPI('pve.example.com',
                     user='root',
                     password='secret',
                     backend='ssh_paramiko',
                     port=22)

# Key-based authentication
proxmox = ProxmoxAPI('pve.example.com',
                     user='root',
                     private_key_file='~/.ssh/id_rsa',
                     backend='ssh_paramiko')
```

**Implementation Details:**
- Uses `paramiko.SSHClient` with `AutoAddPolicy`
- Executes commands via `exec_command()`
- File uploads via SFTP (`putfo()`)
- Returns stdout, stderr, and exit code

#### openssh Backend (backends/openssh.py)

**Dependencies:** `openssh_wrapper` (required)

**Features:**
- Native OpenSSH client
- SSH config file support
- SSH agent forwarding
- Identity file specification

**Example:**
```python
proxmox = ProxmoxAPI('pve.example.com',
                     user='root',
                     backend='openssh',
                     identity_file='~/.ssh/id_rsa',
                     forward_ssh_agent=True,
                     config_file='~/.ssh/config')
```

**Implementation Details:**
- Uses `openssh_wrapper.SSHConnection`
- Respects SSH config (`~/.ssh/config`)
- File uploads via SCP
- Command execution with shell joining

#### Command Execution (CommandBaseSession)

**Shared base class** for all SSH and local backends.

**Command Building:**
1. Map HTTP method to pvesh command:
   - GET → `get`
   - POST → `create`
   - PUT → `set`
   - DELETE → `delete`

2. Build command: `{service}sh {command} {url} {options}`
   - Example: `pvesh get /nodes/pve1/qemu -vmid 100`

3. Add service-specific options:
   - PVE: `--output-format json`

4. Optional sudo prefix

**Option Handling:**
- Converts data/params dicts to `-key value` pairs
- Handles binary values (UTF-8 encode)
- Quotes values containing spaces
- Special handling for QEMU agent exec commands

**File Upload Workaround:**
- Creates temporary file on Proxmox host using Python
- Uploads file to temp location
- Passes temp filename to pvesh command
- Proxmox moves file to final location

**Response Parsing:**
- Parses HTTP status codes from stderr
- Detects task IDs (UPID) to determine success
- Returns Response object with status_code, exit_code, content

**Error Detection:**
```python
# Checks stderr for HTTP status codes (e.g., "400 Bad Request")
# Falls back to exit_code if no status found
# UPID detection overrides error status (task creation succeeded)
```

### 3. Local Backend (backends/local.py)

**Execute pvesh directly** on the Proxmox host itself.

**Dependencies:** None (standard library only)

**Features:**
- No network overhead
- No authentication needed (uses local permissions)
- Fastest execution
- Direct file system access

**Use Cases:**
- Scripts running on Proxmox host
- Cron jobs
- Local automation
- Debugging

**Example:**
```python
# Must run on a Proxmox host
proxmox = ProxmoxAPI(backend='local', service='PVE')

# With sudo (if script runs as non-root)
proxmox = ProxmoxAPI(backend='local', service='PVE', sudo=True)
```

**Implementation Details:**
- Uses `subprocess.Popen` for command execution
- Direct file copy via `shutil.copyfileobj`
- Inherits all command building from `CommandBaseSession`

### Backend Comparison

| Feature | HTTPS | ssh_paramiko | openssh | local |
|---------|-------|--------------|---------|-------|
| **Dependency** | requests | paramiko | openssh_wrapper | None |
| **Authentication** | password, token, 2FA | password, key | password, key, config | local permissions |
| **PVE Support** | ✅ | ✅ | ✅ | ✅ |
| **PMG Support** | ✅ | ✅ | ✅ | ✅ |
| **PBS Support** | ✅ | ❌ | ❌ | ❌ |
| **File Upload** | Native, streaming | SFTP | SCP | Direct copy |
| **Large Files (>2GB)** | ✅ (with toolbelt) | ✅ | ✅ | ✅ |
| **Network Required** | ✅ | ✅ | ✅ | ❌ |
| **SSL/TLS** | ✅ | SSH encryption | SSH encryption | N/A |
| **Proxy Support** | ✅ | ❌ | ❌ | N/A |
| **Session Persistence** | ✅ (cookies) | SSH connection | SSH connection | N/A |
| **Speed** | Medium | Slow (SSH overhead) | Slow (SSH overhead) | Fast |
| **Best For** | Remote API access | Cross-platform SSH | Native SSH tools | On-host scripts |

---

## Features & Capabilities

### 1. Dynamic Resource Navigation

**Attribute-based API traversal** - no need to manually build URLs.

```python
# Traditional approach (manual URL building)
url = f"/nodes/{node}/qemu/{vmid}/status/current"

# Proxmoxer approach (dynamic attributes)
proxmox.nodes(node).qemu(vmid).status.current.get()
```

**Multiple navigation styles:**
```python
# Attribute access
proxmox.nodes.pve1.qemu.get()

# Callable with resource ID
proxmox.nodes('pve1').qemu.get()

# Mixed
proxmox.nodes('pve1').qemu(100).status.current.get()

# Resource ID as list/tuple
proxmox.nodes(['pve1', 'qemu', '100']).status.current.get()

# Resource ID with slashes
proxmox.nodes('pve1/qemu/100').status.current.get()
```

### 2. RESTful Operations

**HTTP verb mapping:**

```python
# GET - retrieve resource
nodes = proxmox.nodes.get()

# POST - create resource
proxmox.nodes('pve1').lxc.post(
    vmid=101,
    ostemplate='local:vztmpl/debian-11-standard_11.3-1_amd64.tar.zst',
    hostname='container01',
    memory=512,
    rootfs='local-lvm:8'
)

# PUT - update resource
proxmox.nodes('pve1').qemu(100).config.put(memory=4096)

# DELETE - remove resource
proxmox.nodes('pve1').qemu(100).delete()

# Aliases
proxmox.nodes('pve1').qemu.create(...)  # alias for post()
proxmox.nodes('pve1').qemu(100).config.set(...)  # alias for put()
```

**Parameters vs Data:**
- GET/DELETE use `params` (query parameters)
- POST/PUT use `data` (request body)
- Both automatically filter None values

```python
# GET with params (builds: /nodes?type=qemu)
proxmox.nodes.get(type='qemu')

# POST with data (sends in body)
proxmox.nodes('pve1').qemu.post(vmid=100, name='test', memory=2048)

# None values are filtered
proxmox.nodes('pve1').qemu.post(vmid=100, name='test', cores=None)
# cores=None is removed, not sent to API
```

### 3. Multi-Service Support

**Single codebase, multiple Proxmox products:**

```python
# Proxmox Virtual Environment
pve = ProxmoxAPI('pve.example.com', user='admin@pam', password='secret', service='PVE')
vms = pve.nodes('pve1').qemu.get()

# Proxmox Mail Gateway
pmg = ProxmoxAPI('mail.example.com', user='admin@pmg', password='secret', service='PMG')
rules = pmg.config.ruledb.get()

# Proxmox Backup Server
pbs = ProxmoxAPI('backup.example.com', user='admin@pbs', password='secret', service='PBS')
datastores = pbs.datastore.get()
```

**Service-specific behavior:**
- Different default ports (PVE/PMG: 8006, PBS: 8007)
- Different token separators (PVE/PMG: `=`, PBS: `:`)
- Different CLI options (PVE adds `--output-format json`)
- Backend availability varies (PBS: HTTPS only)

### 4. File Operations

**Upload files to Proxmox storage:**

```python
# Upload ISO
with open('/path/to/debian.iso', 'rb') as f:
    proxmox.nodes('pve1').storage('local').upload.post(
        content='iso',
        filename=f
    )

# Upload container template
with open('/path/to/template.tar.zst', 'rb') as f:
    proxmox.nodes('pve1').storage('local').upload.post(
        content='vztmpl',
        filename=f
    )

# Large files automatically use streaming (if requests_toolbelt installed)
```

### 5. Task Management

**Built-in task utilities** (proxmoxer.tools.tasks)

```python
from proxmoxer.tools import Tasks

# Start a task
task_id = proxmox.nodes('pve1').qemu(100).status.start.post()

# Wait for completion (blocking)
status = Tasks.blocking_status(proxmox, task_id, timeout=300)

# Decode task ID
info = Tasks.decode_upid(task_id)
# Returns: {'upid': '...', 'node': 'pve1', 'pid': 12345, ...}

# Get formatted log
log_data = proxmox.nodes('pve1').tasks(task_id).log.get()
log_text = Tasks.decode_log(log_data)
print(log_text)
```

**Task UPID Format:**
```
UPID:{node}:{pid}:{pstart}:{starttime}:{type}:{id}:{user}:{comment}

Example:
UPID:pve1:0001E240:00A2F3E1:5F8B2D3C:qmstart:100:root@pam:
```

### 6. File Download/Upload Utilities

**Advanced file tools** (proxmoxer.tools.files)

```python
from proxmoxer.tools import Files

# Initialize
files = Files(proxmox, node='pve1', storage='local')

# Upload local file with automatic checksum
status = files.upload_local_file_to_storage(
    '/path/to/debian.iso',
    do_checksum_check=True,
    blocking_status=True
)

# Download file from URL to Proxmox storage
status = files.download_file_to_storage(
    'https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.0.0-amd64-netinst.iso',
    blocking_status=True
)

# Auto-discovers checksum from common patterns:
# - {url}.sha512, {url}.SHA512
# - https://example.com/SHA512SUMS (containing filename)
# - https://example.com/sha512sums (containing filename)
```

**Supported Checksums** (ordered by preference):
1. SHA512 (128 hex digits)
2. SHA256 (64 hex digits)
3. SHA224 (56 hex digits)
4. SHA384 (96 hex digits)
5. MD5 (32 hex digits)
6. SHA1 (40 hex digits)

**Checksum Discovery Strategies:**
1. Sibling file (e.g., `SHA512SUMS` in same directory)
2. Extension (e.g., `file.iso.sha512`)
3. Uppercase extension (e.g., `file.iso.SHA512`)

### 7. Error Handling

**ResourceException** - raised for API errors (status >= 400)

```python
from proxmoxer import ResourceException

try:
    proxmox.nodes('pve1').qemu(999).status.current.get()
except ResourceException as e:
    print(f"Status: {e.status_code}")      # HTTP status code
    print(f"Message: {e.status_message}")  # HTTP status message
    print(f"Content: {e.content}")         # Error details
    print(f"Errors: {e.errors}")           # API-specific errors
    print(f"Exit code: {e.exit_code}")     # CLI exit code (SSH/local)
```

**AuthenticationError** - raised for auth failures

```python
from proxmoxer import AuthenticationError

try:
    proxmox = ProxmoxAPI('pve.example.com',
                         user='admin@pam',
                         password='wrong')
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

**AnyEvent::HTTP Status Codes** (custom Proxmox codes):
- 595: Connection establishment errors
- 596: TLS negotiation errors
- 597: Body receiving/processing errors
- 598: User aborted request
- 599: Other non-retryable errors

### 8. Advanced Features

#### Automatic Parameter Cleaning

**None values are filtered** to prevent pvesh errors:

```python
# This:
proxmox.nodes('pve1').qemu(100).config.put(
    memory=4096,
    cores=None,    # Will be removed
    sockets=2,
    numa=None      # Will be removed
)

# Becomes equivalent to:
proxmox.nodes('pve1').qemu(100).config.put(
    memory=4096,
    sockets=2
)
```

#### QEMU Guest Agent Exec

**Special handling** for QEMU agent commands:

```python
# Command strings are automatically split
proxmox.nodes('pve1').qemu(100).agent.exec.post(
    command='ls -la /tmp'  # Split into ['ls', '-la', '/tmp']
)

# Or pass as list
proxmox.nodes('pve1').qemu(100).agent.exec.post(
    command=['ls', '-la', '/tmp']
)

# Windows hosts: no splitting (incompatible with shlex)
```

#### SSL/TLS Configuration

```python
# Disable SSL verification (development only!)
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     verify_ssl=False)

# Use custom CA certificate
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     verify_ssl=True,
                     cert='/path/to/ca-bundle.crt')

# Use client certificate
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     cert='/path/to/client-cert.pem')
```

#### Timeout Configuration

```python
# Set request timeout (default: 5 seconds)
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     timeout=30)  # 30 second timeout
```

#### HTTP Proxy Support

```python
# Configure HTTP(S) proxy
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     proxies={
                         'http': 'http://proxy.example.com:8080',
                         'https': 'http://proxy.example.com:8080'
                     })

# With proxy authentication
proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret',
                     proxies={
                         'https': 'http://user:pass@proxy.example.com:8080'
                     })
```

---

## Design Choices & Patterns

### 1. Dynamic Attribute Generation

**Pattern**: `__getattr__` magic method creates resource objects on-the-fly

**Rationale:**
- No need to maintain API endpoint definitions
- Automatically supports new Proxmox API endpoints
- Clean, readable Python code
- Type hints difficult (trade-off for flexibility)

**Implementation:**
```python
def __getattr__(self, item):
    if item.startswith("_"):
        raise AttributeError(item)
    
    kwargs = self._store.copy()
    kwargs["base_url"] = self.url_join(self._store["base_url"], item)
    
    return ProxmoxResource(**kwargs)
```

### 2. URL Building with posixpath

**Pattern**: Use `posixpath.join` instead of string concatenation

**Rationale:**
- Handles trailing slashes correctly
- Platform-independent (always forward slashes)
- Prevents double slashes
- Supports relative path resolution

**Implementation:**
```python
def url_join(self, base, *args):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(base)
    path = path if len(path) else "/"
    path = posixpath.join(path, *[str(x) for x in args])
    return urlparse.urlunsplit([scheme, netloc, path, query, fragment])
```

### 3. None Value Filtering

**Pattern**: Remove `None` values before sending requests

**Rationale:**
- pvesh CLI breaks with `None` values
- Allows default parameter values in functions
- Cleaner API (don't send unnecessary data)
- Consistent behavior across backends

**Implementation:**
```python
if params:
    params_none_keys = [k for (k, v) in params.items() if v is None]
    for key in params_none_keys:
        del params[key]

if data:
    data_none_keys = [k for (k, v) in data.items() if v is None]
    for key in data_none_keys:
        del data[key]
```

### 4. Backend Abstraction

**Pattern**: Common interface, pluggable implementations

**Rationale:**
- Single API for all connection types
- Easy to add new backends
- Consistent behavior across transports
- Service-specific configuration in one place

**Interface Contract:**
```python
class Backend:
    def get_base_url(self) -> str: ...
    def get_session(self) -> Session: ...
    def get_serializer(self) -> Serializer: ...
```

### 5. Service Configuration Dictionary

**Pattern**: Centralized service metadata

**Rationale:**
- Single source of truth for service differences
- Easy to add new services
- Validation at initialization time
- Clear documentation of service capabilities

**Benefits:**
- Prevents invalid backend/service combinations
- Ensures correct ports and token formats
- Service-specific CLI options handled automatically

### 6. Command Base Inheritance

**Pattern**: Shared base class for CLI backends (SSH, local)

**Rationale:**
- DRY principle (Don't Repeat Yourself)
- Consistent pvesh command building
- Single place to fix bugs
- Easy to add new CLI backends

**Shared Functionality:**
- Command building
- Option formatting
- Response parsing
- UPID detection
- File upload workaround

### 7. Response Object Design

**Pattern**: Mimic `requests.Response` interface for CLI backends

**Rationale:**
- Consistent interface across backends
- Easier error handling (same attributes)
- Simplifies serializer logic
- Familiar to users of requests library

**Attributes:**
```python
class Response:
    status_code: int   # HTTP-like status
    exit_code: int     # Process exit code
    content: bytes     # Raw output
    text: str          # String output
    headers: dict      # Fake headers
```

### 8. Lazy Error Decoding

**Pattern**: Only decode errors if status >= 400

**Rationale:**
- Performance (don't parse JSON twice)
- Handles non-JSON responses gracefully
- Separation of concerns (serializer vs error handler)

**Implementation:**
```python
if resp.status_code >= 400:
    errors = self._store["serializer"].loads_errors(resp)
    raise ResourceException(..., errors=errors)
elif 200 <= resp.status_code <= 299:
    return self._store["serializer"].loads(resp)
```

### 9. Ticket Renewal Strategy

**Pattern**: Auto-refresh auth ticket before expiration

**Rationale:**
- Long-running scripts don't fail after 2 hours
- Transparent to user (no manual renewal)
- Maintains session continuity
- Uses existing ticket as password (no credential storage)

**Implementation:**
```python
renew_age = 3600  # 1 hour (PVE tickets valid 2 hours)

def __call__(self, req):
    time_diff = time.monotonic() - self.birth_time
    if time_diff >= self.renew_age:
        self._get_new_tokens()  # Refresh using ticket as password
    # ... add auth headers
```

### 10. File Stream Detection

**Pattern**: Automatically detect file objects in POST data

**Rationale:**
- Pythonic API (just pass file object)
- Automatic Content-Type handling
- Memory-efficient streaming
- Transparent to user

**Implementation:**
```python
for k, v in data.copy().items():
    if isinstance(v, io.IOBase):
        files[k] = (
            requests.utils.guess_filename(v),
            v,
            "application/octet-stream"
        )
        del data[k]
```

---

## Technical Stack

### Core Dependencies

**Required:**
- Python 3.7+ (officially supports 3.10-3.14)
- Standard library only (core functionality)

**Optional Backend Dependencies:**

| Backend | Required Package | Version |
|---------|-----------------|---------|
| HTTPS | `requests` | Any recent |
| ssh_paramiko | `paramiko` | Any recent |
| openssh | `openssh_wrapper` | Any recent |
| local | None | N/A |

**Optional Feature Dependencies:**

| Feature | Required Package | Purpose |
|---------|-----------------|---------|
| Large file uploads (>10MB) | `requests_toolbelt` | Streaming multipart encoding |
| Files tools | `requests` | Checksum discovery via HTTP |

### Development Stack

**Testing & Quality:**
```toml
pytest                    # Test framework
pytest-cov               # Coverage reporting
pytest-mock              # Mocking utilities
bandit                   # Security linting
pre-commit               # Git hooks
black                    # Code formatting
isort                    # Import sorting
pylint                   # Static analysis
flake8                   # Linting
```

**CI/CD:**
- GitHub Actions
- Test matrix: Python 3.10, 3.11, 3.12, 3.13, 3.14
- Coverage tracking via Coveralls
- Automated releases to PyPI

**Code Style:**
- Black formatter (line length: 100)
- isort with Black profile
- PEP 8 compliant
- Type hints (minimal, for clarity not strict typing)

### Project Structure

```
proxmoxer/
├── proxmoxer/
│   ├── __init__.py              # Package entry point, version
│   ├── core.py                  # ProxmoxAPI, ProxmoxResource, exceptions
│   ├── backends/
│   │   ├── __init__.py
│   │   ├── command_base.py      # Base for CLI backends
│   │   ├── https.py             # HTTPS backend (requests)
│   │   ├── ssh_paramiko.py      # SSH backend (paramiko)
│   │   ├── openssh.py           # SSH backend (openssh_wrapper)
│   │   └── local.py             # Local backend (subprocess)
│   └── tools/
│       ├── __init__.py
│       ├── tasks.py             # Task management utilities
│       └── files.py             # File upload/download utilities
├── tests/                       # Pytest test suite
├── .devcontainer/               # VSCode dev container
├── .github/workflows/           # CI/CD pipelines
├── setup.py                     # Package setup (setuptools)
├── pyproject.toml               # Build config (black, isort)
├── setup.cfg                    # Tool config (pylint, flake8)
├── .pre-commit-config.yaml      # Pre-commit hooks
└── CHANGELOG.md                 # Version history

Total: ~1,383 lines of Python code
```

### Code Metrics

| Component | Lines of Code |
|-----------|--------------|
| core.py | 234 |
| backends/https.py | 415 |
| backends/command_base.py | 186 |
| backends/ssh_paramiko.py | 77 |
| backends/openssh.py | 67 |
| backends/local.py | 25 |
| tools/tasks.py | 84 |
| tools/files.py | 279 |
| **Total** | **~1,383** |

**Characteristics:**
- Small, focused codebase
- High test coverage (>90%)
- Clean separation of concerns
- Minimal external dependencies
- Well-documented with examples

---

## Code Examples

### Basic Usage Patterns

#### 1. List All VMs

```python
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI('pve.example.com', 
                     user='admin@pam', 
                     password='secret',
                     verify_ssl=False)

# Iterate through all nodes and VMs
for node in proxmox.nodes.get():
    node_name = node['node']
    print(f"\nNode: {node_name}")
    
    # QEMU VMs
    for vm in proxmox.nodes(node_name).qemu.get():
        print(f"  VM {vm['vmid']}: {vm['name']} - {vm['status']}")
    
    # LXC Containers
    for ct in proxmox.nodes(node_name).lxc.get():
        print(f"  CT {ct['vmid']}: {ct['name']} - {ct['status']}")
```

#### 2. Create and Configure VM

```python
from proxmoxer import ProxmoxAPI, ResourceException

proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     token_name='automation',
                     token_value='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')

node = 'pve1'
vmid = 200

try:
    # Create VM
    proxmox.nodes(node).qemu.post(
        vmid=vmid,
        name='webserver01',
        memory=4096,
        cores=2,
        sockets=1,
        net0='virtio,bridge=vmbr0',
        scsi0='local-lvm:32',
        ide2='local:iso/debian-12.0.0-amd64-netinst.iso,media=cdrom',
        ostype='l26',  # Linux 2.6+
        boot='order=scsi0;ide2'
    )
    print(f"VM {vmid} created successfully")
    
    # Start VM
    task_id = proxmox.nodes(node).qemu(vmid).status.start.post()
    print(f"Start task: {task_id}")
    
    # Wait for start to complete
    from proxmoxer.tools import Tasks
    result = Tasks.blocking_status(proxmox, task_id)
    print(f"VM started: {result}")
    
except ResourceException as e:
    print(f"Error: {e}")
```

#### 3. Backup and Restore

```python
from proxmoxer import ProxmoxAPI
from proxmoxer.tools import Tasks

proxmox = ProxmoxAPI('pve.example.com',
                     user='backup@pve',
                     password='secret')

node = 'pve1'
vmid = 100

# Create backup
task_id = proxmox.nodes(node).vzdump.post(
    vmid=vmid,
    mode='snapshot',
    compress='zstd',
    storage='backup-storage'
)

# Wait for backup to complete
status = Tasks.blocking_status(proxmox, task_id, timeout=3600)
print(f"Backup completed: {status}")

# List backups
backups = proxmox.nodes(node).storage('backup-storage').content.get(
    content='backup'
)

for backup in backups:
    if f'/{vmid}/' in backup['volid']:
        print(f"Backup: {backup['volid']}")
        
        # Restore from backup
        restore_task = proxmox.nodes(node).qemu.post(
            vmid=101,  # New VM ID
            archive=backup['volid'],
            storage='local-lvm'
        )
        print(f"Restore task: {restore_task}")
```

#### 4. Bulk Operations

```python
from proxmoxer import ProxmoxAPI
from concurrent.futures import ThreadPoolExecutor, as_completed

proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret')

node = 'pve1'
vm_ids = [100, 101, 102, 103, 104]

def shutdown_vm(vmid):
    try:
        task = proxmox.nodes(node).qemu(vmid).status.shutdown.post()
        return (vmid, task, None)
    except Exception as e:
        return (vmid, None, str(e))

# Shutdown multiple VMs in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(shutdown_vm, vmid): vmid 
               for vmid in vm_ids}
    
    for future in as_completed(futures):
        vmid, task, error = future.result()
        if error:
            print(f"VM {vmid} failed: {error}")
        else:
            print(f"VM {vmid} shutdown task: {task}")
```

#### 5. Storage Management

```python
from proxmoxer import ProxmoxAPI
from proxmoxer.tools import Files

proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret')

node = 'pve1'

# List storage
for storage in proxmox.nodes(node).storage.get():
    print(f"Storage: {storage['storage']}")
    print(f"  Type: {storage['type']}")
    print(f"  Content: {storage['content']}")
    
    # Get storage status
    status = proxmox.nodes(node).storage(storage['storage']).status.get()
    print(f"  Used: {status['used']} / {status['total']}")

# Upload ISO
files = Files(proxmox, node=node, storage='local')

# Download from URL
result = files.download_file_to_storage(
    'https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.0.0-amd64-netinst.iso',
    blocking_status=True
)
print(f"Download result: {result}")

# Upload local file
result = files.upload_local_file_to_storage(
    '/path/to/custom.iso',
    do_checksum_check=True,
    blocking_status=True
)
print(f"Upload result: {result}")
```

#### 6. Network Configuration

```python
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret')

node = 'pve1'
vmid = 100

# Get current network config
config = proxmox.nodes(node).qemu(vmid).config.get()
print(f"Current net0: {config.get('net0')}")

# Update network interface
proxmox.nodes(node).qemu(vmid).config.put(
    net0='virtio,bridge=vmbr1,firewall=1,tag=100'
)

# Add second network interface
proxmox.nodes(node).qemu(vmid).config.put(
    net1='virtio,bridge=vmbr2'
)

# For containers
proxmox.nodes(node).lxc(vmid).config.put(
    net0='name=eth0,bridge=vmbr0,ip=dhcp,ip6=dhcp'
)
```

#### 7. Monitoring and Metrics

```python
from proxmoxer import ProxmoxAPI
import time

proxmox = ProxmoxAPI('pve.example.com',
                     user='monitoring@pam',
                     password='secret')

node = 'pve1'
vmid = 100

# Node status
status = proxmox.nodes(node).status.get()
print(f"Node CPU: {status['cpu'] * 100:.1f}%")
print(f"Node Memory: {status['memory']['used']} / {status['memory']['total']}")

# VM status
vm_status = proxmox.nodes(node).qemu(vmid).status.current.get()
print(f"VM CPU: {vm_status.get('cpu', 0) * 100:.1f}%")
print(f"VM Memory: {vm_status.get('mem', 0)} / {vm_status.get('maxmem', 0)}")

# RRD data (historical metrics)
timeframe = 'hour'  # or 'day', 'week', 'month', 'year'
rrd = proxmox.nodes(node).qemu(vmid).rrddata.get(timeframe=timeframe)

for datapoint in rrd[:5]:  # First 5 points
    print(f"Time: {datapoint['time']}, CPU: {datapoint.get('cpu', 0)}")
```

#### 8. User and Permission Management

```python
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI('pve.example.com',
                     user='root@pam',
                     password='secret')

# Create user
proxmox.access.users.post(
    userid='testuser@pam',
    password='userpassword',
    comment='Test user account'
)

# Create API token
token = proxmox.access.users('testuser@pam').token('mytoken').post(
    comment='API access token'
)
print(f"Token value: {token['value']}")

# Grant permissions
proxmox.access.acl.put(
    path='/vms/100',
    roles='PVEVMAdmin',
    users='testuser@pam'
)

# Create group
proxmox.access.groups.post(
    groupid='developers',
    comment='Developer team'
)

# Add user to group
proxmox.access.groups('developers').put(
    users='testuser@pam'
)
```

#### 9. Cluster Operations

```python
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI('pve.example.com',
                     user='admin@pam',
                     password='secret')

# Cluster status
status = proxmox.cluster.status.get()
for node in status:
    if node['type'] == 'node':
        print(f"Node: {node['name']}")
        print(f"  Online: {node['online']}")
        print(f"  IP: {node['ip']}")

# Cluster resources (all VMs/CTs across cluster)
resources = proxmox.cluster.resources.get(type='vm')
for vm in resources:
    print(f"{vm['vmid']}: {vm['name']} on {vm['node']} - {vm['status']}")

# HA configuration
ha_resources = proxmox.cluster.ha.resources.get()
for resource in ha_resources:
    print(f"HA Resource: {resource['sid']}")
    print(f"  State: {resource['state']}")
    print(f"  Node: {resource.get('node', 'N/A')}")

# Add HA resource
proxmox.cluster.ha.resources.post(
    sid='vm:100',
    state='started',
    max_restart=3,
    max_relocate=3
)
```

#### 10. Error Handling Best Practices

```python
from proxmoxer import ProxmoxAPI, ResourceException, AuthenticationError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_api_call(func):
    """Decorator for safe API calls with retry logic"""
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except ResourceException as e:
                if e.status_code == 500 and attempt < max_retries - 1:
                    logger.warning(f"Retry {attempt + 1}/{max_retries}: {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"API call failed: {e}")
                    raise
            except AuthenticationError as e:
                logger.error(f"Authentication failed: {e}")
                raise
    return wrapper

@safe_api_call
def get_vm_status(proxmox, node, vmid):
    return proxmox.nodes(node).qemu(vmid).status.current.get()

# Usage
try:
    proxmox = ProxmoxAPI('pve.example.com',
                         user='admin@pam',
                         password='secret',
                         verify_ssl=False)
    
    status = get_vm_status(proxmox, 'pve1', 100)
    logger.info(f"VM status: {status['status']}")
    
except AuthenticationError:
    logger.error("Check credentials")
except ResourceException as e:
    if e.status_code == 404:
        logger.error("VM not found")
    elif e.status_code == 500:
        logger.error("Server error")
    else:
        logger.error(f"Unexpected error: {e}")
```

---

## Comparison with proxmox-openapi

### Architectural Approach

| Aspect | proxmoxer | proxmox-openapi |
|--------|-----------|-----------------|
| **API Discovery** | Dynamic (runtime) | Static (code generation) |
| **Type Safety** | Minimal (duck typing) | Strong (Pydantic models) |
| **IDE Support** | Limited autocomplete | Full autocomplete |
| **API Coverage** | Automatic (all endpoints) | Explicit (generated) |
| **Code Size** | Small (~1.4k LOC) | Larger (generated code) |
| **Maintenance** | Low (API-agnostic) | Medium (regenerate on API changes) |
| **Learning Curve** | Gentle (Pythonic) | Moderate (schema knowledge) |
| **Flexibility** | High (works with any endpoint) | High (customizable generation) |

### Design Philosophy

**proxmoxer**:
- Runtime discovery via `__getattr__`
- "Just works" with any API endpoint
- Minimal code, maximum flexibility
- Trade-off: limited type checking

**proxmox-openapi**:
- Compile-time code generation from OpenAPI spec
- Type-safe, IDE-friendly
- Explicit models and operations
- Trade-off: regeneration needed for API changes

### Use Case Recommendations

**Choose proxmoxer when:**
- Rapid prototyping and scripting
- Working with multiple Proxmox versions
- Need SSH/local backend access
- Prefer minimal dependencies
- Dynamic/exploratory API usage
- Legacy Proxmox versions without OpenAPI

**Choose proxmox-openapi when:**
- Building production applications
- Type safety is critical
- Team development (autocomplete helps onboarding)
- Integration with typed frameworks (FastAPI, etc.)
- Need OpenAPI schema for documentation
- Working with latest Proxmox versions

### Integration Opportunities

**Complementary Usage:**

1. **proxmoxer for runtime, proxmox-openapi for types**:
   ```python
   # Use proxmox-openapi models for validation
   from proxmox_openapi.models import VMConfig
   from proxmoxer import ProxmoxAPI
   
   config = VMConfig(name="test", memory=4096, cores=2)
   proxmox = ProxmoxAPI(...)
   proxmox.nodes('pve1').qemu.post(**config.dict())
   ```

2. **proxmoxer for backends, proxmox-openapi for API**:
   ```python
   # Use proxmoxer's SSH backend with proxmox-openapi's models
   # (would require adapter layer)
   ```

3. **Testing and Development**:
   ```python
   # Use proxmoxer for quick tests/scripts
   # Use proxmox-openapi for production code
   ```

### Feature Matrix

| Feature | proxmoxer | proxmox-openapi |
|---------|-----------|-----------------|
| HTTPS Backend | ✅ | ✅ |
| SSH Backends | ✅ (2 types) | ❌ |
| Local Backend | ✅ | ❌ |
| Type Hints | ⚠️ Minimal | ✅ Full |
| Pydantic Models | ❌ | ✅ |
| API Token Auth | ✅ | ✅ |
| 2FA/OTP | ✅ | ? |
| File Uploads | ✅ Native | ? |
| Task Utilities | ✅ | ? |
| File Utilities | ✅ | ? |
| OpenAPI Schema | ❌ | ✅ |
| Code Generation | ❌ | ✅ |
| Mock API | ❌ | ✅ |
| Multiple Services | ✅ PVE/PMG/PBS | ✅ PVE |

---

## Version History Highlights

### Recent Releases

**2.3.0 (2026-02-07)** - Current
- Two-factor authentication modern 2-step flow support
- Direct HTTP proxy configuration
- Exit code in ResourceException
- Improved pvesh output handling
- Better error handling for failed calls

**2.2.0 (2024-12-13)**
- Certificate support for TLS verification
- Fixed UPID handling in CLI backends
- Binary payload UTF-8 encoding
- Command path fixes for SSH/local backends

**2.1.0 (2024-08-10)**
- Files tools addition
- Python 3.12 support
- Improved repr for debugging
- QEMU exec command fixes

**2.0.0 (2022-11-27)** - Major Version
- Dropped Python 2 support (minimum: 3.7)
- Pytest migration
- Task tools addition
- Path prefix support
- Removed `ProxmoxResourceBase`
- Breaking: AuthenticationError moved to core
- Breaking: Removed ProxmoxHTTPTicketAuth

**1.3.0 (2022-03-13)**
- Local backend addition
- Command base refactoring
- IPv6 support
- Pre-commit hooks
- Dedicated documentation site

**1.2.0 (2021-10-07)**
- OTP/2FA support
- Large file upload support
- PMG and PBS support
- Detailed ResourceException

### Key Milestones

- **2013**: Initial release (0.1.1)
- **2015**: Python 3 compatibility (0.2.0)
- **2017**: Production stable (1.0.0)
- **2020**: API token auth (1.1.0)
- **2021**: Multi-service support (1.2.0)
- **2022**: Python 3 only, major refactor (2.0.0)
- **2022**: Local backend (1.3.0)
- **2024**: Files tools (2.1.0)
- **2026**: Modern 2FA, proxy support (2.3.0)

---

## Summary

**Proxmoxer** is a mature, battle-tested Python library providing:

✅ **Simple, Pythonic API** for Proxmox REST API access  
✅ **Multiple backends** (HTTPS, SSH, local) with unified interface  
✅ **Dynamic resource navigation** - works with any API endpoint  
✅ **Multi-service support** - PVE, PMG, and PBS  
✅ **Comprehensive authentication** - password, tokens, 2FA  
✅ **Production-ready** - 10+ years of development, high test coverage  
✅ **Minimal dependencies** - core library is pure Python  
✅ **Active maintenance** - regular updates and security fixes  

**Best suited for:**
- Scripts and automation
- Multi-backend scenarios (SSH/local access needed)
- Rapid development
- Working across multiple Proxmox versions
- Exploratory API usage

**Trade-offs:**
- Limited type safety
- Minimal IDE autocomplete
- Less structured than schema-based approaches

**Community:**
- 763 GitHub stars
- 90 forks
- Active issue tracking
- Regular releases
- MIT licensed (permissive)

For projects requiring strong typing and IDE support, consider **proxmox-openapi** as a complementary or alternative approach. Both libraries can coexist and serve different use cases in the Proxmox ecosystem.

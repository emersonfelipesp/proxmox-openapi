"""Rate limiting configuration for Proxmox OpenAPI server.

Uses slowapi middleware to enforce per-IP rate limiting, preventing abuse
and ensuring fair resource allocation across API clients.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter: Limiter = Limiter(key_func=get_remote_address)

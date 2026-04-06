"""Security utilities for codegen operations - SSRF protection and validation."""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse


class SSRFProtectionError(ValueError):
    """Raised when a URL fails SSRF validation."""

    pass


# Private IP ranges to block (SSRF protection)
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network("0.0.0.0/8"),  # "This" network
    ipaddress.IPv4Network("10.0.0.0/8"),  # Private network
    ipaddress.IPv4Network("127.0.0.0/8"),  # Loopback
    ipaddress.IPv4Network("169.254.0.0/16"),  # Link-local (AWS metadata, etc.)
    ipaddress.IPv4Network("172.16.0.0/12"),  # Private network
    ipaddress.IPv4Network("192.168.0.0/16"),  # Private network
    ipaddress.IPv4Network("224.0.0.0/4"),  # Multicast
    ipaddress.IPv4Network("240.0.0.0/4"),  # Reserved
]

PRIVATE_IPV6_RANGES = [
    ipaddress.IPv6Network("::1/128"),  # Loopback
    ipaddress.IPv6Network("fe80::/10"),  # Link-local
    ipaddress.IPv6Network("fc00::/7"),  # Unique local addresses
]

# Allowed domains for codegen source URLs (official Proxmox documentation)
ALLOWED_DOMAINS = [
    "pve.proxmox.com",
    "pmg.proxmox.com",
    "pbs.proxmox.com",
    "proxmox.com",
]


def validate_source_url(url: str, *, allow_http: bool = False) -> str:
    """Validate that a source URL is safe for external requests (SSRF protection).

    Args:
        url: The URL to validate
        allow_http: Whether to allow HTTP (default: False, HTTPS only)

    Returns:
        The validated URL (normalized)

    Raises:
        SSRFProtectionError: If the URL fails validation

    Security checks:
        1. Must use HTTPS (or HTTP if explicitly allowed)
        2. Must not target private IP ranges
        3. Must not target localhost/loopback
        4. Must not target link-local addresses (AWS metadata, etc.)
        5. Must not use file:// or other dangerous schemes
        6. Domain should be in the official Proxmox allowlist (warning if not)
    """
    if not url or not isinstance(url, str):
        raise SSRFProtectionError("URL must be a non-empty string")

    url = url.strip()
    if not url:
        raise SSRFProtectionError("URL must be a non-empty string")

    try:
        parsed = urlparse(url)
    except Exception as e:
        raise SSRFProtectionError(f"Invalid URL format: {e}") from e

    # Check scheme
    allowed_schemes = ["https"]
    if allow_http:
        allowed_schemes.append("http")

    if parsed.scheme not in allowed_schemes:
        raise SSRFProtectionError(
            f"Invalid URL scheme: {parsed.scheme!r}. Only {', '.join(allowed_schemes)} are allowed."
        )

    # Extract hostname
    hostname = parsed.hostname
    if not hostname:
        raise SSRFProtectionError("URL must have a valid hostname")

    # Check if hostname is an IP address (IPv4 or IPv6)
    try:
        ip_addr = ipaddress.ip_address(hostname)
    except ValueError:
        ip_addr = None

    if ip_addr is not None:
        # Check against private IPv4 ranges
        if isinstance(ip_addr, ipaddress.IPv4Address):
            for private_range in PRIVATE_IP_RANGES:
                if ip_addr in private_range:
                    raise SSRFProtectionError(
                        f"SSRF attempt blocked: URL targets private IP range {private_range}: {url}"
                    )

        # Check against private IPv6 ranges
        elif isinstance(ip_addr, ipaddress.IPv6Address):
            for private_range in PRIVATE_IPV6_RANGES:
                if ip_addr in private_range:
                    raise SSRFProtectionError(
                        f"SSRF attempt blocked: URL targets private IPv6 range {private_range}: {url}"
                    )
    else:
        # Not an IP address, it's a domain name - validate domain
        # Check against allowed domains
        hostname_lower = hostname.lower()

        # Check if it's in the allowlist or a subdomain of an allowed domain
        is_allowed = any(
            hostname_lower == domain or hostname_lower.endswith(f".{domain}")
            for domain in ALLOWED_DOMAINS
        )

        if not is_allowed:
            # Not in allowlist - this is a warning, not a hard block
            # Allow it but log a warning
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Source URL domain {hostname!r} is not in the official Proxmox allowlist. "
                f"Allowed domains: {', '.join(ALLOWED_DOMAINS)}. Proceeding anyway."
            )

    # Additional safety checks for localhost patterns in domain names
    localhost_patterns = [
        r"^localhost$",
        r"^127\.",
        r"^0\.0\.0\.0$",
        r"^::1$",
        r"^0:0:0:0:0:0:0:1$",
    ]

    for pattern in localhost_patterns:
        if re.match(pattern, hostname, re.IGNORECASE):
            raise SSRFProtectionError(f"SSRF attempt blocked: URL targets localhost: {url}")

    return url


def validate_version_tag(tag: str) -> str:
    """Validate that a version tag is safe for filesystem operations.

    Args:
        tag: The version tag to validate

    Returns:
        The validated tag (stripped)

    Raises:
        ValueError: If the tag contains path traversal sequences or invalid characters

    Security checks:
        1. Must not contain path separators (/, \\)
        2. Must not contain parent directory references (..)
        3. Must only contain alphanumeric characters, dots, dashes, and underscores
        4. Must not be empty
    """
    if not tag or not isinstance(tag, str):
        raise ValueError("version_tag must be a non-empty string")

    tag = tag.strip()
    if not tag:
        raise ValueError("version_tag must be a non-empty string")

    # Check for path traversal patterns
    if ".." in tag:
        raise ValueError("version_tag must not contain parent directory references (..)")

    if "/" in tag or "\\" in tag:
        raise ValueError("version_tag must not contain path separators")

    # Only allow safe characters: alphanumeric, dot, dash, underscore
    if not re.match(r"^[a-zA-Z0-9._-]+$", tag):
        raise ValueError(
            "version_tag must only contain alphanumeric characters, dots, dashes, and underscores"
        )

    return tag


__all__ = ["validate_source_url", "validate_version_tag", "SSRFProtectionError"]

import pytest

from proxmox_openapi.proxmox_codegen.security import (
    SSRFProtectionError,
    validate_source_url,
    validate_version_tag,
)


class TestSSRFProtection:
    def test_valid_urls(self):
        assert (
            validate_source_url("https://pve.proxmox.com/pve-docs/apidoc.html")
            == "https://pve.proxmox.com/pve-docs/apidoc.html"
        )
        assert (
            validate_source_url("https://pmg.proxmox.com/pmg-docs/api-viewer/index.html")
            == "https://pmg.proxmox.com/pmg-docs/api-viewer/index.html"
        )

    def test_http_blocked_by_default(self):
        with pytest.raises(SSRFProtectionError, match="Invalid URL scheme"):
            validate_source_url("http://pve.proxmox.com/pve-docs/apidoc.html")

    def test_http_allowed_explicitly(self):
        assert (
            validate_source_url("http://pve.proxmox.com/pve-docs/apidoc.html", allow_http=True)
            == "http://pve.proxmox.com/pve-docs/apidoc.html"
        )

    def test_localhost_blocked(self):
        with pytest.raises(
            SSRFProtectionError, match="SSRF attempt blocked: URL targets localhost"
        ):
            validate_source_url("https://localhost/api")
        with pytest.raises(
            SSRFProtectionError, match="SSRF attempt blocked: URL targets private IP range"
        ):
            validate_source_url("https://127.0.0.1/api")
        with pytest.raises(
            SSRFProtectionError, match="SSRF attempt blocked: URL targets private IP range"
        ):
            validate_source_url("https://0.0.0.0/api")

    def test_private_ips_blocked(self):
        with pytest.raises(SSRFProtectionError, match="private IP range"):
            validate_source_url("https://10.0.0.5/api")
        with pytest.raises(SSRFProtectionError, match="private IP range"):
            validate_source_url("https://192.168.1.1/api")
        with pytest.raises(SSRFProtectionError, match="private IP range"):
            validate_source_url("https://172.16.0.5/api")
        with pytest.raises(SSRFProtectionError, match="private IP range"):
            validate_source_url("https://169.254.169.254/metadata")  # AWS metadata

    def test_ipv6_blocked(self):
        with pytest.raises(SSRFProtectionError, match="private IPv6 range"):
            validate_source_url("https://[::1]/api")
        with pytest.raises(SSRFProtectionError, match="private IPv6 range"):
            validate_source_url("https://[fe80::1]/api")

    def test_invalid_scheme(self):
        with pytest.raises(SSRFProtectionError, match="Invalid URL scheme"):
            validate_source_url("file:///etc/passwd")
        with pytest.raises(SSRFProtectionError, match="Invalid URL scheme"):
            validate_source_url("gopher://127.0.0.1:6379/_INFO")

    def test_empty_url(self):
        with pytest.raises(SSRFProtectionError, match="URL must be a non-empty string"):
            validate_source_url("")
        with pytest.raises(SSRFProtectionError, match="URL must be a non-empty string"):
            validate_source_url("   ")

    def test_invalid_url_format(self):
        with pytest.raises(SSRFProtectionError):
            validate_source_url("https://[invalid-ipv6]/api")

    def test_non_allowlisted_domain_blocked_by_default(self):
        """Fix 1: Non-Proxmox domains must be rejected unless allow_any_domain=True."""
        with pytest.raises(SSRFProtectionError, match="not in the allowed domains list"):
            validate_source_url("https://evil.com/api")
        with pytest.raises(SSRFProtectionError, match="not in the allowed domains list"):
            validate_source_url("https://example.com/api")

    def test_non_allowlisted_domain_allowed_with_flag(self):
        """Fix 1: allow_any_domain=True permits non-Proxmox domains."""
        result = validate_source_url("https://example.com/api", allow_any_domain=True)
        assert result == "https://example.com/api"

    def test_ipv4_mapped_ipv6_blocked(self):
        """Fix 2: ::ffff:127.0.0.1 must be blocked (IPv4-mapped loopback)."""
        with pytest.raises(SSRFProtectionError, match="IPv6-mapped"):
            validate_source_url("https://[::ffff:127.0.0.1]/api")

    def test_ipv4_mapped_ipv6_private_ranges(self):
        """Fix 2: IPv4-mapped IPv6 private addresses must all be blocked."""
        with pytest.raises(SSRFProtectionError, match="IPv6-mapped"):
            validate_source_url("https://[::ffff:10.0.0.1]/api")
        with pytest.raises(SSRFProtectionError, match="IPv6-mapped"):
            validate_source_url("https://[::ffff:192.168.1.1]/api")
        with pytest.raises(SSRFProtectionError, match="IPv6-mapped"):
            validate_source_url("https://[::ffff:169.254.169.254]/api")

    def test_ipv4_mapped_ipv6_public_allowed(self):
        """Fix 2: IPv4-mapped IPv6 with a public IP passes the IP check."""
        # Public IP embedded in IPv6 — passes IP check, but needs allow_any_domain
        # since it's not a hostname in the Proxmox allowlist.
        result = validate_source_url("https://[::ffff:8.8.8.8]/api", allow_any_domain=True)
        assert result == "https://[::ffff:8.8.8.8]/api"


class TestVersionTagValidation:
    def test_valid_tags(self):
        assert validate_version_tag("v1.0") == "v1.0"
        assert validate_version_tag("latest") == "latest"
        assert validate_version_tag("my-custom_tag.1") == "my-custom_tag.1"
        assert validate_version_tag("  v2.0  ") == "v2.0"

    def test_path_traversal_blocked(self):
        with pytest.raises(ValueError, match="must not contain parent directory references"):
            validate_version_tag("../v1.0")
        with pytest.raises(ValueError, match="must not contain parent directory references"):
            validate_version_tag("v1.0/..")
        with pytest.raises(ValueError, match="must not contain path separators"):
            validate_version_tag("v1.0/test")
        with pytest.raises(ValueError, match="must not contain path separators"):
            validate_version_tag("v1.0\\test")

    def test_invalid_characters_blocked(self):
        with pytest.raises(ValueError, match="must only contain alphanumeric characters"):
            validate_version_tag("v1.0!")
        with pytest.raises(ValueError, match="must only contain alphanumeric characters"):
            validate_version_tag("v1.0@test")
        with pytest.raises(ValueError, match="must only contain alphanumeric characters"):
            validate_version_tag("v1.0 test")

    def test_empty_tag(self):
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_version_tag("")
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_version_tag("   ")

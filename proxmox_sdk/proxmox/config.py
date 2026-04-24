"""Configuration for Proxmox API connections."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from proxmox_sdk.sdk.auth.token import parse_token_id


def _load_config_file(config_file: str, logger: Any) -> dict[str, str]:
    """Load and parse a JSON or YAML config file, returning PROXMOX_API_ prefixed key dict."""
    import json
    import stat
    from pathlib import Path

    result: dict[str, str] = {}
    path = Path(config_file)
    if not path.exists():
        return result

    if path.is_symlink():
        logger.warning(
            f"Config file {config_file} is a symlink. Ensure it points to a trusted location."
        )
    st = path.stat()
    if hasattr(st, "st_mode") and bool(st.st_mode & (stat.S_IRWXG | stat.S_IRWXO)):
        logger.warning(
            f"Config file {config_file} has overly permissive permissions. "
            "It should be restricted to owner."
        )

    try:
        if path.suffix in (".yaml", ".yml"):
            import yaml  # deferred: only loaded when a YAML config file is present

            file_data = yaml.safe_load(path.read_text())
        else:
            file_data = json.loads(path.read_text())

        if isinstance(file_data, dict):
            for k, v in file_data.items():
                env_k = f"PROXMOX_API_{k.upper()}" if not k.startswith("PROXMOX_") else k.upper()
                result[env_k] = str(v)
    except Exception as e:
        logger.error(f"Failed to load config file {config_file}: {e}")

    return result


def _clear_sensitive_env() -> None:
    """Overwrite sensitive credentials in os.environ to prevent accidental re-reads."""
    for key in ("PROXMOX_API_TOKEN_SECRET", "PROXMOX_API_PASSWORD", "PROXMOX_API_OTP"):
        if key in os.environ:
            os.environ[key] = "********"


@dataclass(frozen=True)
class ProxmoxConfig:
    """Configuration for Proxmox API client.

    Supports both the FastAPI server layer and the standalone SDK.

    Environment variables (original, unchanged):
        PROXMOX_API_MODE: "mock" or "real" (default: "mock")
        PROXMOX_API_URL: Proxmox API base URL (e.g., "https://pve.example.com:8006")
        PROXMOX_API_TOKEN_ID: API token ID (e.g., "user@pam!mytoken")
        PROXMOX_API_TOKEN_SECRET: API token secret value
        PROXMOX_API_USERNAME: Username for password auth (alternative to token)
        PROXMOX_API_PASSWORD: Password for password auth (alternative to token)
        PROXMOX_API_VERIFY_SSL: Verify SSL certificates ("true" or "false", default: "true")

    Additional environment variables (SDK layer):
        PROXMOX_API_SERVICE: Service type — PVE, PMG, PBS (default: "PVE")
        PROXMOX_API_BACKEND: Transport backend (default: "https")
        PROXMOX_API_TIMEOUT: Request timeout in seconds (default: "5")
        PROXMOX_API_PATH_PREFIX: Reverse-proxy path prefix (default: "")
        PROXMOX_API_OTP: OTP/TOTP code for 2FA (default: None)
        PROXMOX_API_OTPTYPE: OTP type — "totp" (default: "totp")
    """

    # ---- Original fields (unchanged) ----
    api_mode: str
    api_url: str | None
    token_id: str | None
    token_secret: str | None
    username: str | None
    password: str | None
    verify_ssl: bool

    # ---- SDK fields (new, all have defaults) ----
    service: str = "PVE"
    backend: str = "https"
    timeout: int = 5
    connect_timeout: int | None = None
    port: int | None = None
    path_prefix: str = ""
    otp: str | None = None
    otptype: str = "totp"
    cert: str | None = None
    proxies: dict[str, str] | None = field(default=None, hash=False, compare=False)
    max_retries: int = 0
    retry_backoff: float = 0.5

    @classmethod
    def from_env(cls) -> ProxmoxConfig:
        """Load configuration from file and environment variables. Config file overrides env vars."""
        import logging

        _logger = logging.getLogger("proxmox_sdk")

        # Read only the specific env keys we need instead of copying the entire os.environ.
        _KEYS = (
            "PROXMOX_API_MODE",
            "PROXMOX_API_URL",
            "PROXMOX_API_TOKEN_ID",
            "PROXMOX_API_TOKEN_SECRET",
            "PROXMOX_API_USERNAME",
            "PROXMOX_API_PASSWORD",
            "PROXMOX_API_VERIFY_SSL",
            "PROXMOX_API_SERVICE",
            "PROXMOX_API_BACKEND",
            "PROXMOX_API_TIMEOUT",
            "PROXMOX_API_CONNECT_TIMEOUT",
            "PROXMOX_API_PATH_PREFIX",
            "PROXMOX_API_OTP",
            "PROXMOX_API_OTPTYPE",
            "PROXMOX_API_HTTP_PROXY",
            "PROXMOX_API_HTTPS_PROXY",
            "PROXMOX_API_RETRIES",
            "PROXMOX_API_RETRY_BACKOFF",
            "HTTP_PROXY",
            "HTTPS_PROXY",
            "http_proxy",
            "https_proxy",
            "PROXMOX_CONFIG_FILE",
        )
        env_config: dict[str, str] = {k: v for k in _KEYS if (v := os.environ.get(k)) is not None}

        config_file = os.environ.get("PROXMOX_CONFIG_FILE")
        if config_file:
            env_config.update(_load_config_file(config_file, _logger))

        api_mode = env_config.get("PROXMOX_API_MODE", "mock").lower()
        api_url = env_config.get("PROXMOX_API_URL")
        token_id = env_config.get("PROXMOX_API_TOKEN_ID")
        token_secret = env_config.get("PROXMOX_API_TOKEN_SECRET")
        username = env_config.get("PROXMOX_API_USERNAME")
        password = env_config.get("PROXMOX_API_PASSWORD")
        verify_ssl_str = env_config.get("PROXMOX_API_VERIFY_SSL", "true").lower()
        verify_ssl = verify_ssl_str in ("true", "1", "yes")

        _clear_sensitive_env()

        service = env_config.get("PROXMOX_API_SERVICE", "PVE").upper()
        backend = env_config.get("PROXMOX_API_BACKEND", "https").lower()
        timeout = int(env_config.get("PROXMOX_API_TIMEOUT", "5"))
        connect_timeout_str = env_config.get("PROXMOX_API_CONNECT_TIMEOUT")
        connect_timeout = int(connect_timeout_str) if connect_timeout_str else None
        path_prefix = env_config.get("PROXMOX_API_PATH_PREFIX", "")
        otp = env_config.get("PROXMOX_API_OTP") or None
        otptype = env_config.get("PROXMOX_API_OTPTYPE", "totp")
        max_retries = int(env_config.get("PROXMOX_API_RETRIES", "0"))
        retry_backoff = float(env_config.get("PROXMOX_API_RETRY_BACKOFF", "0.5"))

        proxies = None
        http_proxy = (
            env_config.get("PROXMOX_API_HTTP_PROXY")
            or env_config.get("HTTP_PROXY")
            or env_config.get("http_proxy")
        )
        https_proxy = (
            env_config.get("PROXMOX_API_HTTPS_PROXY")
            or env_config.get("HTTPS_PROXY")
            or env_config.get("https_proxy")
        )

        if http_proxy or https_proxy:
            proxies = {}
            if http_proxy:
                proxies["http"] = http_proxy
            if https_proxy:
                proxies["https"] = https_proxy

        return cls(
            api_mode=api_mode,
            api_url=api_url,
            token_id=token_id,
            token_secret=token_secret,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
            service=service,
            backend=backend,
            timeout=timeout,
            connect_timeout=connect_timeout,
            path_prefix=path_prefix,
            otp=otp,
            otptype=otptype,
            proxies=proxies,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
        )

    def validate_for_real_mode(self) -> None:
        """Validate that configuration is sufficient for real API mode.

        Raises:
            ValueError: If required configuration is missing.
        """
        if not self.api_url:
            raise ValueError("PROXMOX_API_URL is required for real API mode")

        if not ((self.token_id and self.token_secret) or (self.username and self.password)):
            raise ValueError(
                "Either (PROXMOX_API_TOKEN_ID + PROXMOX_API_TOKEN_SECRET) "
                "or (PROXMOX_API_USERNAME + PROXMOX_API_PASSWORD) is required for authentication"
            )

    def is_real_mode(self) -> bool:
        """Check if running in real API mode."""
        return self.api_mode == "real"

    def is_mock_mode(self) -> bool:
        """Check if running in mock API mode."""
        return self.api_mode == "mock"

    def to_sdk_kwargs(self) -> dict[str, Any]:
        """Convert to ``ProxmoxSDK`` constructor keyword arguments.

        Useful when bridging the FastAPI configuration to the SDK::

            config = ProxmoxConfig.from_env()
            proxmox = ProxmoxSDK(**config.to_sdk_kwargs())
        """
        from urllib.parse import urlsplit

        kwargs: dict[str, Any] = {
            "service": self.service,
            "backend": self.backend if self.api_mode != "mock" else "mock",
            "verify_ssl": self.verify_ssl,
            "timeout": self.timeout,
            "connect_timeout": self.connect_timeout,
            "path_prefix": self.path_prefix,
            "otptype": self.otptype,
            "max_retries": self.max_retries,
            "retry_backoff": self.retry_backoff,
        }

        if self.cert:
            kwargs["cert"] = self.cert
        if self.proxies:
            kwargs["proxies"] = self.proxies
        if self.otp:
            kwargs["otp"] = self.otp

        if self.api_mode == "mock":
            return kwargs

        # Real mode — extract host and credentials
        parsed = urlsplit(str(self.api_url or ""))
        kwargs["host"] = parsed.netloc or parsed.path

        if self.token_id and self.token_secret:
            user, token_name = parse_token_id(self.token_id)
            kwargs["user"] = user
            kwargs["token_name"] = token_name
            kwargs["token_value"] = self.token_secret
        else:
            kwargs["user"] = self.username
            kwargs["password"] = self.password

        return kwargs


__all__ = ["ProxmoxConfig"]

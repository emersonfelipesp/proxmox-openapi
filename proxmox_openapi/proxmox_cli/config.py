"""Configuration loading and management for the CLI."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from .exceptions import ConfigError

logger = logging.getLogger(__name__)


@dataclass
class BackendConfig:
    """Configuration for a backend connection."""

    name: str
    backend: str = "https"
    host: str | None = None
    port: int | None = None
    service: Literal["PVE", "PMG", "PBS"] = "PVE"
    user: str | None = None
    password: str | None = None
    token_name: str | None = None
    token_value: str | None = None
    verify_ssl: bool = True
    timeout: int = 30
    custom: dict = field(default_factory=dict)


@dataclass
class GlobalConfig:
    """Global CLI configuration."""

    output_format: str = "human"
    table_mode: str = "grid"
    colors: bool = True
    completion_shell: str | None = None
    verbose: bool = False
    quiet: bool = False


class ConfigManager:
    """Manages CLI configuration loading and override logic."""

    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".proxmox-cli" / "config.json",
        Path.home() / ".proxmoxrc",
        Path("/etc/proxmox-cli/config.json"),
    ]

    def __init__(self) -> None:
        """Initialize ConfigManager."""
        self.profiles: dict[str, BackendConfig] = {}
        self.global_config = GlobalConfig()
        self.default_profile: str | None = None

    def load_config(self, config_path: str | None = None) -> None:
        """Load configuration from file.

        Args:
            config_path: Optional custom config file path

        Raises:
            ConfigError: If config file is invalid
        """
        # Determine which config file to load
        config_file = None

        if config_path:
            config_file = Path(config_path)
        else:
            # Try default paths
            for path in self.DEFAULT_CONFIG_PATHS:
                if path.exists():
                    config_file = path
                    break

        if not config_file or not config_file.exists():
            logger.debug("No config file found, using defaults")
            return

        try:
            content = config_file.read_text()
            data = json.loads(content)
            self._parse_config_data(data)
            logger.debug(f"Loaded config from {config_file}")
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in {config_file}: {e}")
        except (IOError, OSError) as e:
            raise ConfigError(f"Cannot read {config_file}: {e}")

    def _parse_config_data(self, data: dict) -> None:
        """Parse configuration data.

        Args:
            data: Configuration dictionary

        Raises:
            ConfigError: If configuration is invalid
        """
        # Parse profiles
        profiles = data.get("profiles", {})
        if not isinstance(profiles, dict):
            raise ConfigError("profiles must be a dictionary")

        for profile_name, profile_data in profiles.items():
            if not isinstance(profile_data, dict):
                raise ConfigError(f"Profile '{profile_name}' must be a dictionary")

            self.profiles[profile_name] = BackendConfig(
                name=profile_name,
                backend=profile_data.get("backend", "https"),
                host=profile_data.get("host"),
                port=profile_data.get("port"),
                service=profile_data.get("service", "PVE"),
                user=profile_data.get("user"),
                password=profile_data.get("password"),
                token_name=profile_data.get("token_name"),
                token_value=profile_data.get("token_value"),
                verify_ssl=profile_data.get("verify_ssl", True),
                timeout=profile_data.get("timeout", 30),
                custom=profile_data.get("custom", {}),
            )

        # Parse global config
        global_cfg = data.get("global", {})
        if isinstance(global_cfg, dict):
            self.global_config = GlobalConfig(
                output_format=global_cfg.get("output_format", "human"),
                table_mode=global_cfg.get("table_mode", "grid"),
                colors=global_cfg.get("colors", True),
                completion_shell=global_cfg.get("completion_shell"),
                verbose=global_cfg.get("verbose", False),
                quiet=global_cfg.get("quiet", False),
            )

        # Set default profile
        self.default_profile = data.get("default_profile", "default")

    def get_profile(self, profile_name: str | None = None) -> BackendConfig:
        """Get a backend configuration profile.

        Args:
            profile_name: Profile name (uses default if not specified)

        Returns:
            BackendConfig instance

        Raises:
            ConfigError: If profile not found
        """
        name = profile_name or self.default_profile or "default"

        if name not in self.profiles:
            if name == "default":
                # Return default profile if not in config
                return BackendConfig(name="default")
            raise ConfigError(f"Profile '{name}' not found in configuration")

        return self.profiles[name]

    def list_profiles(self) -> list[BackendConfig]:
        """List available profiles."""
        return list(self.profiles.values())

    def add_profile(self, name: str, config: BackendConfig) -> None:
        """Add or replace a profile."""
        config.name = name
        self.profiles[name] = config

    def remove_profile(self, name: str) -> None:
        """Remove a profile by name."""
        if name not in self.profiles:
            raise ConfigError(f"Profile '{name}' not found in configuration")
        del self.profiles[name]

        if self.default_profile == name:
            self.default_profile = "default"

    def set_default_profile(self, name: str) -> None:
        """Set default profile by name."""
        if name != "default" and name not in self.profiles:
            raise ConfigError(f"Profile '{name}' not found in configuration")
        self.default_profile = name

    def save_config(self, config_path: str | Path | None = None) -> None:
        """Save current configuration to file.

        Args:
            config_path: Path to save configuration to

        Raises:
            ConfigError: If save fails
        """
        path = Path(config_path) if config_path else self.DEFAULT_CONFIG_PATHS[0]
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": "1.0",
            "default_profile": self.default_profile or "default",
            "profiles": {
                name: {
                    "backend": cfg.backend,
                    "host": cfg.host,
                    "port": cfg.port,
                    "service": cfg.service,
                    "user": cfg.user,
                    "password": cfg.password,
                    "token_name": cfg.token_name,
                    "token_value": cfg.token_value,
                    "verify_ssl": cfg.verify_ssl,
                    "timeout": cfg.timeout,
                    "custom": cfg.custom,
                }
                for name, cfg in self.profiles.items()
            },
            "global": {
                "output_format": self.global_config.output_format,
                "table_mode": self.global_config.table_mode,
                "colors": self.global_config.colors,
                "completion_shell": self.global_config.completion_shell,
                "verbose": self.global_config.verbose,
                "quiet": self.global_config.quiet,
            },
        }

        try:
            path.write_text(json.dumps(data, indent=2))
            logger.debug(f"Saved config to {path}")
        except (IOError, OSError) as e:
            raise ConfigError(f"Cannot write config to {path}: {e}")


def load_config_from_env() -> BackendConfig:
    """Load configuration from environment variables.

    Returns:
        BackendConfig with environment-based settings
    """
    import os

    return BackendConfig(
        name="env",
        backend=os.getenv("PROXMOX_CLI_BACKEND", "https"),
        host=os.getenv("PROXMOX_CLI_HOST"),
        port=int(port_str) if (port_str := os.getenv("PROXMOX_CLI_PORT")) else None,
        service=os.getenv("PROXMOX_CLI_SERVICE", "PVE"),  # type: ignore
        user=os.getenv("PROXMOX_CLI_USER"),
        password=os.getenv("PROXMOX_CLI_PASSWORD"),
        token_name=os.getenv("PROXMOX_CLI_TOKEN_NAME"),
        token_value=os.getenv("PROXMOX_CLI_TOKEN_VALUE"),
        verify_ssl=os.getenv("PROXMOX_CLI_VERIFY_SSL", "true").lower() == "true",
    )

"""Response caching for improved performance."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Optional

from proxmox_openapi.proxmox_cli.exceptions import ProxmoxCLIError


class Cache:
    """Simple cache implementation for API responses."""

    def __init__(self, cache_dir: Optional[Path] = None, ttl: int = 300) -> None:
        """Initialize cache.

        Args:
            cache_dir: Directory for cache files (default: ~/.proxmox-cli/cache)
            ttl: Time-to-live for cache entries in seconds (default: 5 minutes)
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".proxmox-cli" / "cache"

        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.

        Args:
            key: Cache key (usually API path)

        Returns:
            Cached value or None if not found/expired
        """
        cache_file = self._get_cache_file(key)

        if not cache_file.exists():
            return None

        try:
            with open(cache_file) as f:
                data = json.load(f)

            # Check if expired
            if time.time() - data["timestamp"] > self.ttl:
                cache_file.unlink()
                return None

            return data["value"]
        except (json.JSONDecodeError, KeyError):
            # Invalid cache file, remove it
            cache_file.unlink()
            return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON-serializable)
        """
        cache_file = self._get_cache_file(key)

        try:
            with open(cache_file, "w") as f:
                json.dump(
                    {"timestamp": time.time(), "value": value},
                    f,
                )
        except (TypeError, IOError) as e:
            raise ProxmoxCLIError(f"Failed to cache value: {e}")

    def clear(self, key: Optional[str] = None) -> None:
        """Clear cache entry or entire cache.

        Args:
            key: Specific key to clear, or None to clear all
        """
        if key is None:
            # Clear all
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
        else:
            cache_file = self._get_cache_file(key)
            if cache_file.exists():
                cache_file.unlink()

    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for key.

        Args:
            key: Cache key

        Returns:
            Path to cache file
        """
        # Hash the key to avoid filesystem issues with special characters
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"


class CacheableSDKBridge:
    """SDK bridge wrapper with caching support.

    Wraps ProxmoxSDKBridge and caches read-only operations.
    """

    def __init__(self, bridge: Any, cache: Optional[Cache] = None) -> None:
        """Initialize caching bridge.

        Args:
            bridge: ProxmoxSDKBridge instance
            cache: Cache instance (default: create new Cache)
        """
        self.bridge = bridge
        self.cache = cache or Cache()

    def get(self, path: str, use_cache: bool = True) -> Any:
        """Get resource with optional caching.

        Args:
            path: API path
            use_cache: Whether to use cache (default: True)

        Returns:
            API response
        """
        if use_cache:
            cached = self.cache.get(path)
            if cached is not None:
                return cached

        result = self.bridge.get(path)

        if use_cache and result is not None:
            self.cache.set(path, result)

        return result

    def post(self, path: str, **kwargs: Any) -> Any:
        """Create resource (cache is cleared for parent paths).

        Args:
            path: API path
            **kwargs: Request parameters

        Returns:
            API response
        """
        result = self.bridge.post(path, **kwargs)
        # Invalidate cache for parent paths
        self._invalidate_parent_paths(path)
        return result

    def put(self, path: str, **kwargs: Any) -> Any:
        """Update resource (cache is invalidated).

        Args:
            path: API path
            **kwargs: Request parameters

        Returns:
            API response
        """
        result = self.bridge.put(path, **kwargs)
        # Invalidate cache for this path and parents
        self.cache.clear(path)
        self._invalidate_parent_paths(path)
        return result

    def delete(self, path: str) -> Any:
        """Delete resource (cache is invalidated).

        Args:
            path: API path

        Returns:
            API response
        """
        result = self.bridge.delete(path)
        # Invalidate cache for this path and parents
        self.cache.clear(path)
        self._invalidate_parent_paths(path)
        return result

    def _invalidate_parent_paths(self, path: str) -> None:
        """Invalidate cache for parent paths.

        Args:
            path: Path to invalidate parents for
        """
        parts = path.split("/")
        for i in range(len(parts) - 1, 0, -1):
            parent_path = "/".join(parts[:i])
            if parent_path:
                self.cache.clear(parent_path)

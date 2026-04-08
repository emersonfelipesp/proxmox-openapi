"""Shared in-memory state for the generated Proxmox mock API."""

from __future__ import annotations

import atexit
import hashlib
import json
import os
import tempfile
import threading
from contextlib import contextmanager
from copy import deepcopy
from multiprocessing import shared_memory
from pathlib import Path
from typing import Any, Iterator

from proxmox_openapi.logger import logger

try:
    import fcntl
except ImportError:  # pragma: no cover - non-Unix fallback
    fcntl = None

_DEFAULT_STATE_BYTES = 8 * 1024 * 1024
_STATE_HEADER_BYTES = 8
_STATE_CACHE_LOCK = threading.RLock()
_STATE_CLIENTS: dict[str, "SharedMemoryMockStore"] = {}


def _process_exists(pid: int) -> bool:
    """Return whether the process with the given PID is still running."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def mock_state_owner_pid() -> int:
    """Return the long-lived owner pid used to scope reload-safe state."""

    try:
        from multiprocessing import parent_process

        parent = parent_process()
    except Exception:  # pragma: no cover - defensive import
        parent = None
    if parent is not None and parent.pid is not None:
        return parent.pid
    return os.getpid()


def _resolved_namespace(namespace: str | None) -> str:
    """Resolve the active shared-state namespace."""
    return namespace or os.environ.get("PROXMOX_MOCK_STATE_NAMESPACE", "default")


def _namespace_digest(namespace: str) -> str:
    """Return a stable digest for a namespace name."""
    return hashlib.sha256(namespace.encode("utf-8")).hexdigest()[:8]


def _state_basename(owner_pid: int, namespace: str) -> str:
    """Build the shared-memory base name for a namespace and owner PID."""
    return f"pmxmock_{_namespace_digest(namespace)}_{owner_pid}"


def _meta_path(owner_pid: int, namespace: str) -> Path:
    """Return the metadata file path for a shared mock state store."""
    return Path(tempfile.gettempdir()) / f"{_state_basename(owner_pid, namespace)}.meta"


def _lock_path(owner_pid: int, namespace: str) -> Path:
    """Return the lock file path for a shared mock state store."""
    return Path(tempfile.gettempdir()) / f"{_state_basename(owner_pid, namespace)}.lock"


@contextmanager
def _locked_file(path: Path, *, exclusive: bool = True) -> Iterator[None]:
    """Acquire an interprocess lock for a filesystem-backed state file.

    Uses LOCK_SH (shared) for read-only access so concurrent readers do not
    block each other, and LOCK_EX (exclusive) only for writes.
    """
    path.touch(exist_ok=True)
    with path.open("r+", encoding="utf-8") as handle:
        if fcntl is not None:
            lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
            fcntl.flock(handle.fileno(), lock_type)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class SharedMemoryMockStore:
    """JSON-backed state stored in a named shared-memory segment."""

    def __init__(
        self,
        *,
        owner_pid: int,
        namespace: str,
        shm: shared_memory.SharedMemory,
        state_bytes: int,
    ) -> None:
        """Initialize the shared-memory mock store."""
        self.owner_pid = owner_pid
        self.namespace = namespace
        self._shm = shm
        self._state_bytes = state_bytes
        self._lock_path = _lock_path(owner_pid, namespace)
        self._meta_path = _meta_path(owner_pid, namespace)

    def touch_schema(self, schema_fingerprint: str) -> bool:
        """Reset state when the schema fingerprint changes."""
        with self._locked_state() as state:
            if state["schema_fingerprint"] == schema_fingerprint:
                return False
            state["schema_fingerprint"] = schema_fingerprint
            state["objects"] = {}
            state["collections"] = {}
            state["deleted"] = []
            return True

    def reset(self) -> None:
        """Reset stored objects, collections, and tombstones."""
        with self._locked_state() as state:
            state["objects"] = {}
            state["collections"] = {}
            state["deleted"] = []

    def get_object(self, key: str) -> Any | None:
        """Return a deep copy of a stored object by key."""
        with self._locked_state(write=False) as state:
            value = state["objects"].get(key)
            return deepcopy(value)

    def set_object(self, key: str, value: Any) -> Any:
        """Store an object value and return the persisted copy."""
        with self._locked_state() as state:
            state["objects"][key] = deepcopy(value)
            if key in state["deleted"]:
                state["deleted"].remove(key)
            return deepcopy(state["objects"][key])

    def delete_object(self, key: str) -> None:
        """Delete an object and mark it as removed."""
        with self._locked_state() as state:
            state["objects"].pop(key, None)
            state["deleted"].add(key)

    def is_deleted(self, key: str) -> bool:
        """Return whether a key has been marked as deleted."""
        with self._locked_state(write=False) as state:
            return key in state["deleted"]

    def get_collection(self, key: str) -> list[Any] | None:
        """Return a list copy of a stored collection."""
        with self._locked_state(write=False) as state:
            members = state["collections"].get(key)
            if members is None:
                return None
            return [deepcopy(value) for value in members.values()]

    def replace_collection(self, key: str, values: list[Any]) -> list[Any]:
        """Replace a collection with the provided values."""
        with self._locked_state() as state:
            state["collections"][key] = {
                f"seed:{index}": deepcopy(value) for index, value in enumerate(values)
            }
            return [deepcopy(value) for value in state["collections"][key].values()]

    def upsert_collection_member(self, key: str, member_key: str, value: Any) -> list[Any]:
        """Insert or replace a member in a stored collection."""
        with self._locked_state() as state:
            members = state["collections"].setdefault(key, {})
            members[member_key] = deepcopy(value)
            if member_key in state["deleted"]:
                state["deleted"].remove(member_key)
            return [deepcopy(item) for item in members.values()]

    def delete_collection_member(self, key: str, member_key: str) -> list[Any]:
        """Remove a member from a stored collection."""
        with self._locked_state() as state:
            members = state["collections"].setdefault(key, {})
            members.pop(member_key, None)
            state["deleted"].add(member_key)
            return [deepcopy(item) for item in members.values()]

    @contextmanager
    def _locked_state(self, *, write: bool = True) -> Iterator[dict[str, Any]]:
        """Load the current state under a filesystem lock and optionally persist it.

        Read-only callers (write=False) acquire a shared lock so concurrent GETs
        do not block each other.  Write callers always use an exclusive lock.
        """
        with _locked_file(self._lock_path, exclusive=write):
            state = self._read_state()
            # Materialise 'deleted' as a set for O(1) membership checks at runtime.
            state["deleted"] = set(state["deleted"])
            yield state
            if write:
                # Serialise back to list for JSON compatibility.
                state["deleted"] = list(state["deleted"])
                self._write_state(state)

    def _read_state(self) -> dict[str, Any]:
        """Deserialize the shared-memory payload into a normalized state mapping."""
        try:
            length = int.from_bytes(self._shm.buf[:_STATE_HEADER_BYTES], "big")
        except (TypeError, ValueError):
            return self._default_state()

        max_bytes = self._state_bytes - _STATE_HEADER_BYTES
        if length <= 0 or length > max_bytes:
            return self._default_state()

        try:
            payload = bytes(self._shm.buf[_STATE_HEADER_BYTES : _STATE_HEADER_BYTES + length])
            state = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError):
            return self._default_state()

        return self._normalize_state(state)

    def _write_state(self, state: dict[str, Any]) -> None:
        """Serialize the state mapping back into shared memory."""
        payload = json.dumps(state, sort_keys=True, separators=(",", ":")).encode("utf-8")
        max_bytes = self._state_bytes - _STATE_HEADER_BYTES
        if len(payload) > max_bytes:
            raise RuntimeError(
                f"Shared mock state exceeded the allocated {max_bytes} byte capacity."
            )
        self._shm.buf[:_STATE_HEADER_BYTES] = len(payload).to_bytes(_STATE_HEADER_BYTES, "big")
        self._shm.buf[_STATE_HEADER_BYTES : _STATE_HEADER_BYTES + len(payload)] = payload

    def close(self, *, unlink: bool = False) -> None:
        """Close the shared-memory segment and optionally unlink its metadata."""
        try:
            self._shm.close()
        except FileNotFoundError:  # pragma: no cover - defensive cleanup
            return
        if unlink:
            try:
                self._shm.unlink()
            except FileNotFoundError:
                pass
            self._meta_path.unlink(missing_ok=True)
            self._lock_path.unlink(missing_ok=True)

    @staticmethod
    def _default_state() -> dict[str, Any]:
        """Return the default shared mock state structure."""
        return {
            "schema_fingerprint": "",
            "objects": {},
            "collections": {},
            "deleted": [],
        }

    @classmethod
    def _normalize_state(cls, state: Any) -> dict[str, Any]:
        """Coerce loaded state into the expected mapping shape."""
        default_state = cls._default_state()
        if not isinstance(state, dict):
            return default_state

        normalized = default_state.copy()
        schema_fingerprint = state.get("schema_fingerprint")
        if isinstance(schema_fingerprint, str):
            normalized["schema_fingerprint"] = schema_fingerprint

        objects = state.get("objects")
        if isinstance(objects, dict):
            normalized["objects"] = objects

        collections = state.get("collections")
        if isinstance(collections, dict):
            normalized["collections"] = collections

        deleted = state.get("deleted")
        if isinstance(deleted, list):
            normalized["deleted"] = deleted

        return normalized


def _cleanup_stale_states(namespace: str, owner_pid: int) -> None:
    """Remove stale shared-memory segments for a namespace."""
    digest = _namespace_digest(namespace)
    temp_root = Path(tempfile.gettempdir())
    for meta_file in temp_root.glob(f"pmxmock_{digest}_*.meta"):
        try:
            stale_owner = int(meta_file.stem.rsplit("_", 1)[-1])
        except ValueError:
            continue
        if stale_owner == owner_pid or _process_exists(stale_owner):
            continue

        shm_name = meta_file.read_text(encoding="utf-8").strip() or meta_file.stem
        try:
            stale_segment = shared_memory.SharedMemory(name=shm_name, create=False)
        except FileNotFoundError:
            stale_segment = None
        if stale_segment is not None:
            try:
                stale_segment.close()
            finally:
                try:
                    stale_segment.unlink()
                except FileNotFoundError:
                    pass
        meta_file.unlink(missing_ok=True)
        _lock_path(stale_owner, namespace).unlink(missing_ok=True)


def _create_or_attach_store(owner_pid: int, namespace: str) -> SharedMemoryMockStore:
    """Create a new shared-memory store or attach to an existing one."""
    state_bytes = int(os.environ.get("PROXMOX_MOCK_STATE_BYTES", str(_DEFAULT_STATE_BYTES)))
    basename = _state_basename(owner_pid, namespace)
    meta_file = _meta_path(owner_pid, namespace)

    with _locked_file(_lock_path(owner_pid, namespace)):
        try:
            shm = shared_memory.SharedMemory(name=basename, create=False)
        except FileNotFoundError:
            shm = shared_memory.SharedMemory(name=basename, create=True, size=state_bytes)
            shm.buf[:_STATE_HEADER_BYTES] = (0).to_bytes(_STATE_HEADER_BYTES, "big")
            meta_file.write_text(basename, encoding="utf-8")
            logger.info(
                "Created reload-safe Proxmox mock shared state",
                extra={
                    "namespace": namespace,
                    "owner_pid": owner_pid,
                    "state_name": basename,
                },
            )
        else:
            meta_file.write_text(basename, encoding="utf-8")

    return SharedMemoryMockStore(
        owner_pid=owner_pid,
        namespace=namespace,
        shm=shm,
        state_bytes=state_bytes,
    )


def _attach_existing_store(owner_pid: int, namespace: str) -> SharedMemoryMockStore:
    """Attach to an already-created shared-memory store."""
    state_bytes = int(os.environ.get("PROXMOX_MOCK_STATE_BYTES", str(_DEFAULT_STATE_BYTES)))
    basename = _state_basename(owner_pid, namespace)
    shm = shared_memory.SharedMemory(name=basename, create=False)
    return SharedMemoryMockStore(
        owner_pid=owner_pid,
        namespace=namespace,
        shm=shm,
        state_bytes=state_bytes,
    )


def shared_mock_store(
    schema_fingerprint: str,
    *,
    namespace: str | None = None,
    owner_pid: int | None = None,
) -> SharedMemoryMockStore:
    """Return a reload-safe shared state store for generated mock responses."""

    resolved_owner = owner_pid or mock_state_owner_pid()
    resolved_namespace = _resolved_namespace(namespace)
    cache_key = f"{resolved_namespace}:{resolved_owner}"

    with _STATE_CACHE_LOCK:
        cached = _STATE_CLIENTS.get(cache_key)
        if cached is None:
            _cleanup_stale_states(resolved_namespace, resolved_owner)
            cached = _create_or_attach_store(resolved_owner, resolved_namespace)
            _STATE_CLIENTS[cache_key] = cached
        cached.touch_schema(schema_fingerprint)
        return cached


def reset_shared_mock_state(*, namespace: str | None = None, owner_pid: int | None = None) -> None:
    """Reset the current live mock state back to the deterministic seed."""

    resolved_owner = owner_pid or mock_state_owner_pid()
    resolved_namespace = _resolved_namespace(namespace)
    cache_key = f"{resolved_namespace}:{resolved_owner}"

    with _STATE_CACHE_LOCK:
        cached = _STATE_CLIENTS.get(cache_key)
        if cached is None:
            try:
                cached = _attach_existing_store(resolved_owner, resolved_namespace)
            except FileNotFoundError:
                return
            _STATE_CLIENTS[cache_key] = cached
        cached.reset()


def _close_cached_stores() -> None:
    """Close cached shared-memory stores during interpreter shutdown."""
    current_pid = os.getpid()
    with _STATE_CACHE_LOCK:
        for store in _STATE_CLIENTS.values():
            store.close(unlink=store.owner_pid == current_pid)


atexit.register(_close_cached_stores)

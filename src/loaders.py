"""Load a directory into an in-memory VFS."""

import posixpath
from pathlib import Path

from .vfs import VFS, Node


def safe_path(value):
    """Reject traversal and ambiguous paths in serialized VFS sources."""
    if not isinstance(value, str) or not value:
        raise ValueError("VFS entry needs a nonempty path")
    if "\\" in value or "\x00" in value or ".." in value.split("/"):
        raise ValueError(f"unsafe VFS path: {value}")
    return "/" + posixpath.normpath(value).lstrip("/")


def ensure_parent(vfs, path):
    """Create missing parent directories in memory."""
    parent = posixpath.dirname(path)
    missing = []
    while parent not in vfs.nodes:
        missing.append(parent)
        parent = posixpath.dirname(parent)
    vfs.require_directory(parent)
    for item in reversed(missing):
        vfs.add(item, Node(directory=True, mode=0o755))


def insert(vfs, path, node):
    """Insert a source entry, allowing existing directories."""
    path = safe_path(path)
    ensure_parent(vfs, path)
    if path in vfs.nodes and node.directory:
        vfs.require_directory(path)
        return
    vfs.add(path, node)


def read_directory(vfs, source):
    """Snapshot a directory, rejecting links and special files."""
    if not source.is_dir():
        raise ValueError(f"not a directory: {source}")
    for item in sorted(source.rglob("*")):
        if item.is_symlink() or item.is_junction():
            raise ValueError(f"links are unsupported: {item}")
        directory = item.is_dir()
        if not directory and not item.is_file():
            raise ValueError(f"unsupported node: {item}")
        node = Node(directory, b"" if directory else item.read_bytes())
        node.mode = 0o755 if directory else 0o644
        insert(vfs, item.relative_to(source).as_posix(), node)


def load_vfs(path=None):
    """Load the required format, returning an empty VFS if unspecified."""
    if path is None:
        return VFS()
    source = Path(path)
    if source.is_symlink() or source.is_junction():
        raise ValueError("VFS source cannot be a link")
    vfs = VFS(source.name)
    read_directory(vfs, source)
    return vfs

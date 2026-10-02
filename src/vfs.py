"""Virtual nodes and POSIX paths; command operations never access disk."""

import base64
import hashlib
import json
import posixpath
from dataclasses import dataclass


@dataclass
class Node:
    """Represent a directory or a byte-preserving virtual file."""

    directory: bool = False
    data: bytes = b""
    mode: int = 0o644
    owner: str = "user"
    group: str = "users"
    modified: float = 0.0


class VFS:
    """Store a complete virtual filesystem in memory."""

    def __init__(self, name="default"):
        """Create an empty root directory."""
        self.name = name
        self.nodes = {"/": Node(directory=True, mode=0o755)}

    def resolve(self, path, cwd="/"):
        """Normalize absolute/relative POSIX paths and clamp at root."""
        if "\x00" in path:
            raise ValueError("NUL in virtual path")
        return "/" + posixpath.normpath(posixpath.join(cwd, path)).lstrip("/")

    def get(self, path):
        """Return a node or raise a readable missing-path error."""
        if path not in self.nodes:
            raise ValueError(f"no such file or directory: {path}")
        return self.nodes[path]

    def require_directory(self, path):
        """Validate a directory operand."""
        node = self.get(path)
        if not node.directory:
            raise ValueError(f"not a directory: {path}")
        return node

    def children(self, path):
        """Return immediate child paths in lexical order."""
        self.require_directory(path)
        return sorted(
            item
            for item in self.nodes
            if item != "/" and posixpath.dirname(item) == path
        )

    def add(self, path, node):
        """Insert a node after validating its parent and uniqueness."""
        if path in self.nodes:
            raise ValueError(f"path already exists: {path}")
        self.require_directory(posixpath.dirname(path))
        self.nodes[path] = node

    def text(self, path):
        """Decode a regular file as UTF-8."""
        node = self.get(path)
        if node.directory:
            raise ValueError(f"is a directory: {path}")
        return node.data.decode("utf-8")

    def digest(self):
        """Hash canonical paths, contents, and stable virtual metadata."""
        records = []
        for path, node in sorted(self.nodes.items()):
            records.append(
                [
                    path,
                    node.directory,
                    node.mode,
                    node.owner,
                    node.group,
                    base64.b64encode(node.data).decode("ascii"),
                ]
            )
        data = json.dumps(records, ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(data).hexdigest()

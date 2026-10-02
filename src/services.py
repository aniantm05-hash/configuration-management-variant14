"""Variant-specific VFS inspection and explicit physical reset."""

import shutil
from pathlib import Path

from .settings import SERVICES
from .vfs import VFS


def validate_reset_path(path):
    """Refuse filesystem roots, home, project ancestors, and symlinks."""
    original = Path(path).absolute()
    target = original.resolve()
    protected = {Path.cwd().resolve(), Path.home().resolve()}
    if target == Path(target.anchor):
        raise ValueError("cannot reset a filesystem root")
    if any(target == item or target in item.parents for item in protected):
        raise ValueError("cannot reset home or a project ancestor")
    if any(
        p.is_symlink() or p.is_junction()
        for p in [original, *original.parents]
    ):
        raise ValueError("cannot reset a source reached through a link")
    return target


def clear_source(path):
    """Reset exactly the configured source after verifying its boundary."""
    if path is None:
        return
    target = validate_reset_path(path)
    children = list(target.iterdir())
    for child in children:
        if child.is_symlink() or child.is_junction():
            raise ValueError("cannot reset a directory containing links")
        if not child.resolve().is_relative_to(target):
            raise ValueError("reset target escapes VFS source")
    for child in children:
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def install(shell, source):
    """Register only the service commands required by this variant."""

    def info(args):
        """Display the current VFS name and canonical SHA-256 hash."""
        if args:
            raise ValueError("usage: vfs-info")
        shell.output(f"{shell.vfs.name} SHA-256 {shell.vfs.digest()}")

    def reset(args):
        """Replace both the physical source and in-memory VFS with empty."""
        if args:
            raise ValueError("usage: vfs-init")
        clear_source(source)
        shell.vfs = VFS(shell.name)
        shell.cwd = "/"
        shell.output("VFS reset")

    handlers = {"vfs-info": info, "vfs-init": reset}
    shell.commands.update({name: handlers[name] for name in SERVICES})

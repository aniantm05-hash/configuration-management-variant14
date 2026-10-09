"""Mutating commands; all changes remain in the virtual node dictionary."""

import re

from .base_commands import BasicCommands
from .settings import EXTRA

MIN_METADATA_ARGUMENTS = 2


class Mutations(BasicCommands):
    """Implement ownership changes for variant 14."""


    def chown(self, args):
        """Set owner[:group], optionally recursively with -R."""
        recursive = args[:1] == ["-R"]
        values = args[1:] if recursive else args
        if len(values) < MIN_METADATA_ARGUMENTS:
            raise ValueError("usage: chown [-R] owner[:group] path ...")
        owner, separator, group = values[0].partition(":")
        if not re.fullmatch(r"[\w.][\w.-]*", owner):
            raise ValueError("invalid owner")
        if separator and not re.fullmatch(r"[\w.][\w.-]*", group):
            raise ValueError("invalid group")
        for node in self.metadata_targets(values[1:], recursive):
            node.owner = owner
            if separator:
                node.group = group

    def metadata_targets(self, paths, recursive):
        """Validate all metadata targets before applying any changes."""
        result = []
        for value in paths:
            path = self.path(value)
            result.append(self.shell.vfs.get(path))
            if recursive:
                prefix = path.rstrip("/") + "/"
                result.extend(
                    node
                    for item, node in self.shell.vfs.nodes.items()
                    if item != path and item.startswith(prefix)
                )
        return result


def install(shell):
    """Register only the mutating commands assigned to this variant."""
    handlers = Mutations(shell)
    for name in EXTRA:
        shell.commands[name] = getattr(handlers, name)

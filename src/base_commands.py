"""Read-only UNIX-like commands operating on the in-memory snapshot."""

import getpass
import posixpath

from .settings import BASIC

TAIL_ARGUMENTS_WITH_COUNT = 3
MIN_LINE_COUNT = 0


def operands(args, minimum=0, maximum=1):
    """Validate operand count before executing a command."""
    if not minimum <= len(args) <= maximum:
        raise ValueError("wrong number of arguments")


class BasicCommands:
    """Implement paths, listings, text inspection, and host information."""

    def __init__(self, shell):
        """Attach handlers to a running shell."""
        self.shell = shell

    def path(self, value="."):
        """Resolve a command operand relative to the current directory."""
        return self.shell.vfs.resolve(value, self.shell.cwd)

    def ls(self, args):
        """List a file/directory, with optional -a and -l flags."""
        flags, paths = self.listing_arguments(args)
        path = self.path(paths[0] if paths else ".")
        node = self.shell.vfs.get(path)
        entries = self.shell.vfs.children(path) if node.directory else [path]
        for item in entries:
            name = posixpath.basename(item)
            if name.startswith(".") and "a" not in flags:
                continue
            self.shell.output(self.listing_line(item, "l" in flags))

    def listing_arguments(self, args):
        """Split ls flags from its optional path operand."""
        flags, paths = set(), []
        for arg in args:
            if arg.startswith("-"):
                if not set(arg[1:]) <= {"a", "l"} or arg == "-":
                    raise ValueError("usage: ls [-a] [-l] [path]")
                flags.update(arg[1:])
            else:
                paths.append(arg)
        operands(paths)
        return flags, paths

    def listing_line(self, path, long_format):
        """Format a listing entry and optional virtual metadata."""
        current = self.shell.vfs.get(path)
        prefix = ""
        if long_format:
            kind = "d" if current.directory else "-"
            prefix = f"{kind}{current.mode:04o} {current.owner} "
            prefix += f"{current.group} {len(current.data)} "
        return prefix + posixpath.basename(path)

    def cd(self, args):
        """Change the virtual working directory; default to root."""
        operands(args)
        path = self.path(args[0] if args else "/")
        self.shell.vfs.require_directory(path)
        self.shell.cwd = path


    def tail(self, args):
        """Print the last ten lines, or an explicit nonnegative -n count."""
        count = 10
        if args[:1] == ["-n"]:
            if len(args) < TAIL_ARGUMENTS_WITH_COUNT:
                raise ValueError("usage: tail [-n count] file")
            count = int(args[1])
            args = args[2:]
        operands(args, 1, 1)
        if count < MIN_LINE_COUNT:
            raise ValueError("tail count must be nonnegative")
        lines = self.shell.vfs.text(self.path(args[0])).splitlines()
        self.shell.output("\n".join(lines[-count:]) if count else "")


    def who(self, args):
        """Identify the real account running this emulator session."""
        operands(args, 0, 0)
        self.shell.output(f"{getpass.getuser()} emulator")


    def wc(self, args):
        """Count newline characters, words, and bytes; support -l/-w/-c."""
        flag = args[0] if args and args[0].startswith("-") else None
        if flag:
            if flag not in {"-l", "-w", "-c"}:
                raise ValueError("usage: wc [-l|-w|-c] file")
            args = args[1:]
        operands(args, 1, 1)
        path = self.path(args[0])
        data = self.shell.vfs.get(path)
        if data.directory:
            raise ValueError(f"is a directory: {path}")
        counts = {
            "-l": data.data.count(b"\n"),
            "-w": len(data.data.split()),
            "-c": len(data.data),
        }
        values = [counts[flag]] if flag else counts.values()
        self.shell.output(" ".join(map(str, values)) + " " + args[0])


def install(shell):
    """Replace prototypes and install this variant's read-only commands."""
    handlers = BasicCommands(shell)
    for name in ["ls", "cd", *BASIC]:
        shell.commands[name] = getattr(handlers, name)

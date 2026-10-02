"""Command dispatch and user-facing error handling."""

import getpass
import socket
import time

from .parsing import parse
from .settings import HOST_PROMPT

MAX_CD_ARGUMENTS = 1


class Shell:
    """Keep a single interactive emulator session."""

    def __init__(self, name="default", output=print):
        """Initialize the prompt, lifecycle, and command table."""
        self.name = name
        self.output = output
        self.running = True
        self.cwd = "/"
        self.started = time.monotonic()
        self.commands = {
            "ls": self.stub_ls,
            "cd": self.stub_cd,
            "exit": self.exit_command,
        }

    def prompt(self):
        """Include the VFS name or actual host identity in the prompt."""
        identity = self.name
        if HOST_PROMPT:
            identity = f"{getpass.getuser()}@{socket.gethostname()}"
        return f"{identity}:{self.cwd}$ "

    def execute(self, line):
        """Execute one line and return success without leaking tracebacks."""
        try:
            parts = parse(line)
            if not parts:
                return True
            command, *args = parts
            if command not in self.commands:
                raise ValueError(f"unknown command: {command}")
            self.commands[command](args)
            return True
        except (ValueError, OSError, UnicodeError) as error:
            self.output(f"error: {error}")
            return False

    def stub_ls(self, args):
        """Show the ls prototype invocation."""
        self.output(f"ls {args!r}")

    def stub_cd(self, args):
        """Show the cd prototype invocation and reject extra operands."""
        if len(args) > MAX_CD_ARGUMENTS:
            raise ValueError("usage: cd [path]")
        self.output(f"cd {args!r}")

    def exit_command(self, args):
        """End the session after validating arguments."""
        if args:
            raise ValueError("usage: exit")
        self.running = False

"""Shared fixture setup without duplicating command tests."""

import tempfile
import unittest
from pathlib import Path

from src.base_commands import install
from src.fixtures import write_fixture
from src.loaders import load_vfs
from src.shell import Shell


class FixtureCase(unittest.TestCase):
    """Prepare a temporary directory and an output-capturing shell."""

    def setUp(self):
        """Prepare the assigned source format and captured shell."""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / "deep"
        write_fixture(self.source, "deep")
        self.output = []
        self.shell = Shell(output=self.output.append)
        self.shell.vfs = load_vfs(self.source)
        install(self.shell)

    def execute(self, line):
        """Execute a successful command and return its joined output."""
        self.output.clear()
        self.assertTrue(self.shell.execute(line), self.output)
        return "\n".join(self.output)


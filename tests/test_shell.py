"""Verify parsing, prompt, command dispatch, and exit semantics."""

import getpass
import socket
import unittest

from src.parsing import parse
from src.settings import HOST_PROMPT
from src.shell import Shell


class ShellTests(unittest.TestCase):
    """Exercise the frontend-independent session contract."""

    def setUp(self):
        """Create a session with captured text output."""
        self.output = []
        self.shell = Shell("sample", self.output.append)

    def test_blank_and_unknown(self):
        """Whitespace is harmless and unknown commands report errors."""
        self.assertTrue(self.shell.execute("   "))
        self.assertFalse(self.shell.execute("not-a-command"))
        self.assertIn("unknown command", self.output[-1])

    def test_exit(self):
        """Invalid exit arguments leave the session running."""
        self.assertFalse(self.shell.execute("exit extra"))
        self.assertTrue(self.shell.running)
        self.assertTrue(self.shell.execute("exit"))
        self.assertFalse(self.shell.running)

    def test_prompt(self):
        """Prompt identity comes from the variant's required source."""
        identity = "sample"
        if HOST_PROMPT:
            identity = f"{getpass.getuser()}@{socket.gethostname()}"
        self.assertIn(identity, self.shell.prompt())


    def test_parser(self):
        """Whitespace splits tokens; quotes remain literal characters."""
        self.assertEqual(parse('cd "a b"'), ["cd", '"a', 'b"'])
        self.assertEqual(parse("  ls   /docs  "), ["ls", "/docs"])

    def test_stubs(self):
        """Prototype handlers echo commands and validate cd arguments."""
        self.assertTrue(self.shell.execute("ls /docs"))
        self.assertIn("/docs", self.output[-1])
        self.assertTrue(self.shell.execute("cd /docs"))
        self.assertFalse(self.shell.execute("cd a b"))

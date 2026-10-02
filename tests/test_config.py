"""Test configuration precedence and startup script error policies."""

import tempfile
import unittest
from pathlib import Path

from src.config import load_options
from src.settings import COMMENTS, STOP_ON_ERROR
from src.shell import Shell
from src.startup import remove_comment, run_script


class ConfigurationTests(unittest.TestCase):
    """Exercise options and file-based command execution."""

    def test_options(self):
        """Both source and script paths survive CLI parsing."""
        options = load_options(["--vfs", "a", "--script", "b", "--batch"])
        self.assertEqual((options.vfs, options.script), ("a", "b"))
        self.assertTrue(options.batch)

    def test_policy(self):
        """A failed command stops or continues exactly as specified."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text("unknown\nexit\n", encoding="utf-8")
            output = []
            shell = Shell(output=output.append)
            self.assertFalse(run_script(shell, path))
            self.assertEqual(shell.running, STOP_ON_ERROR)
            self.assertTrue(any(":1" in line for line in output))
            self.assertIn("$ unknown", output[0])

    def test_exit_stops_script(self):
        """Commands following exit are never executed."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text("exit\nunknown\n", encoding="utf-8")
            output = []
            self.assertTrue(run_script(Shell(output=output.append), path))
            self.assertEqual(len(output), 1)

    def test_comments(self):
        """Comment stripping preserves quoted hash characters."""
        self.assertEqual(remove_comment('ls "a#b" # comment'), 'ls "a#b" ')
        if not COMMENTS:
            return
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text("# comment\nexit # done\n", encoding="utf-8")
            self.assertTrue(run_script(Shell(output=lambda text: None), path))



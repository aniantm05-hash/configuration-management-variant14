"""Read-only command behavior, flags, and virtual path errors."""

from src.settings import BASIC
from tests.helpers import FixtureCase


class CommandTests(FixtureCase):
    """Run commands against a fresh three-level snapshot."""


    def test_ls_modes(self):
        """Listings support hidden entries, metadata, and direct files."""
        self.assertNotIn(".hidden", self.execute("ls"))
        self.assertIn(".hidden", self.execute("ls -a"))
        self.assertIn("0644", self.execute("ls -l /readme.txt"))
        self.assertIn(".hidden", self.execute("ls -al"))
        self.assertFalse(self.shell.execute("ls -z"))
        self.assertFalse(self.shell.execute("ls /missing"))

    def test_cd_modes(self):
        """Absolute, relative, parent, and default paths affect only cwd."""
        self.execute("cd /docs/notes/deep")
        self.execute("cd ..")
        self.assertEqual(self.shell.cwd, "/docs/notes")
        self.execute("cd")
        self.assertEqual(self.shell.cwd, "/")
        self.assertFalse(self.shell.execute("cd /readme.txt"))
        self.assertFalse(self.shell.execute("cd a b"))

    def test_assigned_commands(self):
        """Each assigned command produces the expected semantic result."""
        cases = {
            "tail": ("tail -n 1 /readme.txt", "third line"),
            "who": ("who", "emulator"),
            "wc": ("wc /readme.txt", "3 6 34"),
        }
        for command in BASIC:
            line, expected = cases[command]
            with self.subTest(command=command):
                self.assertIn(expected, self.execute(line))

    def test_text_modes(self):
        """Zero/default tail counts and all wc selectors work."""
        if "tail" in BASIC:
            self.assertEqual(self.execute("tail -n 0 /readme.txt"), "")
            self.assertIn("first line", self.execute("tail /readme.txt"))
            self.assertFalse(self.shell.execute("tail -n -1 /readme.txt"))
            self.assertFalse(self.shell.execute("tail /docs"))
            self.assertFalse(self.shell.execute("tail /binary.bin"))
        if "wc" in BASIC:
            for flag, expected in [("-l", "3"), ("-w", "6"), ("-c", "34")]:
                self.assertEqual(
                    self.execute(f"wc {flag} /readme.txt"),
                    expected + " /readme.txt",
                )

    def test_invalid_operands(self):
        """Commands reject invalid modes or nonexistent file arguments."""
        for name in BASIC:
            with self.subTest(name=name):
                self.assertFalse(self.shell.execute(f"{name} /missing -z"))


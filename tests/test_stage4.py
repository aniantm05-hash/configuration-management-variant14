"""Check integrated commands and byte-based counts."""

import getpass

from src.config import load_options
from src.main import create_shell
from tests.helpers import FixtureCase


class Stage4Tests(FixtureCase):
    """Verify observable behavior beyond isolated handlers."""

    def test_main_installs_commands(self):
        """The real entry point registers all stage-four handlers."""
        options = load_options(["--vfs", str(self.source)])
        shell = create_shell(options)
        shell.output = self.output.append
        self.assertTrue(shell.execute("cd /docs/notes/deep"))
        self.assertEqual(shell.cwd, "/docs/notes/deep")
        self.assertTrue(shell.execute("wc info.txt"))
        self.assertEqual(self.output[-1], "3 6 34 info.txt")
        self.assertTrue(shell.execute("who"))
        self.assertIn(getpass.getuser(), self.output[-1])

    def test_main_installs_chown(self):
        """The real entry point installs ownership changes."""
        shell = create_shell(load_options(["--vfs", str(self.source)]))
        shell.output = self.output.append
        self.assertTrue(shell.execute("chown student /readme.txt"))
        self.assertEqual(shell.vfs.get("/readme.txt").owner, "student")

    def test_binary_and_unterminated_counts(self):
        """Byte count accepts binary; lines count newline bytes."""
        self.assertEqual(
            self.execute("wc -c /binary.bin"), "256 /binary.bin"
        )
        self.shell.vfs.get("/readme.txt").data = "один два".encode()
        self.assertEqual(self.execute("wc /readme.txt"), "0 2 15 /readme.txt")

    def test_cd_failed_keeps_directory(self):
        """Invalid transitions keep the previous working path."""
        self.execute("cd /docs")
        self.assertFalse(self.shell.execute("cd /readme.txt"))
        self.assertEqual(self.shell.cwd, "/docs")
        self.execute("cd ../../..")
        self.assertEqual(self.shell.cwd, "/")

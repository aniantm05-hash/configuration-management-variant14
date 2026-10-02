"""Exercise UI event wiring without opening a desktop window."""

import unittest
from unittest.mock import patch

from src.interface import TerminalWindow, cli
from src.shell import Shell


class InterfaceTests(unittest.TestCase):
    """Check CLI lifecycle and Tk command entry/output wiring."""

    def test_cli_exit(self):
        """Terminal input dispatches commands and exits normally."""
        shell = Shell(output=lambda text: None)
        with patch("builtins.input", side_effect=["unknown", "exit"]):
            cli(shell)
        self.assertFalse(shell.running)

    def test_cli_eof(self):
        """EOF does not produce a traceback."""
        with patch("builtins.input", side_effect=EOFError):
            cli(Shell())

    def test_gui_submit(self):
        """Return echoes input, dispatches it, and exit closes the window."""
        with (
            patch("tkinter.Tk"),
            patch("tkinter.Entry"),
            patch("tkinter.scrolledtext.ScrolledText"),
        ):
            shell = Shell("example")
            window = TerminalWindow(shell)
            window.entry.get.return_value = "unknown"
            window.submit()
            rendered = str(window.history.insert.call_args_list)
            self.assertIn("unknown command", rendered)
            window.entry.get.return_value = "exit"
            window.submit()
            window.root.destroy.assert_called_once()

    def test_gui_title(self):
        """Window title contains the required host or VFS identity."""
        with (
            patch("tkinter.Tk"),
            patch("tkinter.Entry"),
            patch("tkinter.scrolledtext.ScrolledText"),
        ):
            shell = Shell("sample")
            window = TerminalWindow(shell)
            title = window.root.title.call_args.args[0]
            identity = shell.prompt().split(":")[0]
            self.assertEqual(title, f"Эмулятор - [{identity}]")

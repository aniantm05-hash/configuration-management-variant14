"""Application lifecycle: configuration, script, and interactive UI."""

import sys
from pathlib import Path

from .base_commands import install as install_basic
from .config import load_options
from .interface import TerminalWindow, cli
from .loaders import load_vfs
from .services import install as install_services
from .settings import GUI
from .shell import Shell
from .startup import run_script


def create_shell(options):
    """Create a configured prototype session."""
    name = Path(options.vfs).name if options.vfs else "default"
    shell = Shell(name)
    shell.vfs = load_vfs(options.vfs)
    install_services(shell, options.vfs)
    install_basic(shell)
    return shell


def run(options):
    """Display options and startup dialogue in the selected interface."""
    shell = create_shell(options)
    window = TerminalWindow(shell) if GUI and not options.batch else None
    shell.output("configuration: " + repr(vars(options)))
    success = True
    if options.script:
        success = run_script(shell, options.script)
    if not options.batch:
        if window:
            window.run()
        elif shell.running:
            cli(shell)
    return 0 if success else 1


def main(argv=None):
    """Handle input/configuration errors with a nonzero process status."""
    try:
        return run(load_options(argv))
    except (ValueError, OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

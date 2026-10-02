"""Startup parameters for variant 14."""

import argparse


def load_options(argv=None):
    """Parse the VFS path, startup script, and batch flag."""
    parser = argparse.ArgumentParser(description="In-memory UNIX emulator")
    parser.add_argument("--vfs", help="VFS source path")
    parser.add_argument("--script", help="UTF-8 startup command file")
    parser.add_argument("--batch", action="store_true", help="skip REPL")
    options = parser.parse_args(argv)
    return options



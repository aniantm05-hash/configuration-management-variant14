"""Startup script execution with variant-specific error policy."""

from pathlib import Path

from .settings import COMMENTS, STOP_ON_ERROR


def remove_comment(line):
    """Strip Python-style comments outside quoted strings."""
    quote = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote:
            quote = None
        elif char in "\"'" and quote is None:
            quote = char
        elif char == "#" and quote is None:
            return line[:index]
    return line


def run_script(shell, path):
    """Echo commands, report line numbers, and respect exit and errors."""
    lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    success = True
    for number, original in enumerate(lines, start=1):
        if not shell.running:
            break
        line = remove_comment(original) if COMMENTS else original
        if not line.strip():
            continue
        shell.output(shell.prompt() + original)
        if not shell.execute(line):
            success = False
            shell.output(f"script error: {path}:{number}")
            if STOP_ON_ERROR:
                break
    return success

"""Launch the interactive REPL prototype."""

from .interface import interact
from .shell import Shell


def main():
    """Start the variant's CLI or GUI session."""
    interact(Shell())


if __name__ == "__main__":
    main()

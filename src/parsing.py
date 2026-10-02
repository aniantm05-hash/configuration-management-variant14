"""Split commands and arguments by whitespace for variant 14."""


def parse(line):
    """Return command tokens without interpreting quotes or variables."""
    return line.split()

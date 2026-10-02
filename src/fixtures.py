"""Generate ignored VFS fixtures from reviewable text definitions."""

import base64
from pathlib import Path


PAYLOAD = b"first line\nsecond line\nthird line\n"


def fixture_records(kind):
    """Return minimal, multiple-file, or three-level fixture contents."""
    records = []
    if kind == "minimal":
        return records
    files = {"readme.txt": PAYLOAD, ".hidden": b"hidden\n"}
    files["binary.bin"] = bytes(range(256))
    files["motd"] = b"Welcome to the virtual shell!\n"
    if kind == "deep":
        files["docs/notes/deep/info.txt"] = PAYLOAD
        files["docs/notes/deep/other.txt"] = b"extra\n"
        files["space name.txt"] = b"quoted filename\n"
    directories = set()
    for path in files:
        parent = Path(path).parent
        while parent != Path("."):
            directories.add(parent.as_posix())
            parent = parent.parent
    records.extend({"path": p, "type": "dir"} for p in sorted(directories))
    for path, data in files.items():
        records.append(
            {
                "path": path,
                "type": "file",
                "data": base64.b64encode(data).decode("ascii"),
            }
        )
    return records


def write_fixture(target, kind):
    """Serialize one fixture using the variant's physical format."""
    target = Path(target)
    records = fixture_records(kind)
    target.parent.mkdir(parents=True, exist_ok=True)
    write_directory(target, records)


def write_directory(target, records):
    """Create a fixture directory without deleting existing data."""
    target.mkdir(parents=True, exist_ok=True)
    for record in records:
        path = target / record["path"]
        if record["type"] == "dir":
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.write_bytes(base64.b64decode(record["data"]))


def main():
    """Generate all documented fixtures under ignored .generated/."""
    for kind in ["minimal", "files", "deep"]:
        target = Path(".generated") / kind
        write_fixture(target, kind)
        print(target)


if __name__ == "__main__":
    main()

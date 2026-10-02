"""Validate snapshots, binary preservation, formats, and services."""

import tempfile
import unittest
from pathlib import Path

from src.fixtures import write_fixture
from src.loaders import load_vfs, safe_path
from src.services import install, validate_reset_path
from src.settings import FORMAT, SERVICES
from src.shell import Shell
from src.vfs import VFS, Node


class VFSTests(unittest.TestCase):
    """Exercise loading without modifying or extracting the source."""

    def setUp(self):
        """Create fixtures inside an isolated temporary directory."""
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        suffix = "" if FORMAT == "directory" else "." + FORMAT
        self.source = Path(self.temporary.name) / ("sample" + suffix)
        write_fixture(self.source, "deep")

    def test_contents(self):
        """Nested paths and all byte values survive serialization."""
        vfs = load_vfs(self.source)
        self.assertEqual(vfs.get("/binary.bin").data, bytes(range(256)))
        self.assertIn("third line", vfs.text("/docs/notes/deep/info.txt"))
        self.assertEqual(vfs.resolve("../../..", "/docs"), "/")

    def test_memory_isolation(self):
        """Changing memory cannot change the physical source."""
        vfs = load_vfs(self.source)
        digest = vfs.digest()
        vfs.get("/readme.txt").data = b"changed"
        self.assertNotEqual(vfs.digest(), digest)
        self.assertEqual(load_vfs(self.source).digest(), digest)

    def test_three_layouts(self):
        """Minimal and multi-file fixtures load alongside deep layouts."""
        for kind in ["minimal", "files"]:
            target = self.source.with_name(kind + self.source.suffix)
            write_fixture(target, kind)
            vfs = load_vfs(target)
            self.assertEqual("/readme.txt" in vfs.nodes, kind == "files")

    def test_invalid_source(self):
        """Missing and malformed physical sources raise normal errors."""
        with self.assertRaises((ValueError, OSError)):
            load_vfs(self.source.with_name("missing"))
        invalid = self.source.with_name("invalid")
        invalid.write_text("broken", encoding="utf-8")
        with self.assertRaises((ValueError, OSError)):
            load_vfs(invalid)

    def test_path_validation(self):
        """Serialized traversal and ambiguous separators are rejected."""
        for value in ["../escape", "a/../b", "a\\b", "a\x00b", None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_path(value)

    def test_services(self):
        """Information and reset commands match the assigned variant."""
        output = []
        shell = Shell(self.source.name, output.append)
        shell.vfs = load_vfs(self.source)
        install(shell, str(self.source))
        if "vfs-info" in SERVICES:
            self.assertTrue(shell.execute("vfs-info"))
            self.assertIn(shell.vfs.digest(), output[-1])
            self.assertFalse(shell.execute("vfs-info extra"))
        if "vfs-init" in SERVICES:
            shell.cwd = "/docs"
            self.assertTrue(shell.execute("vfs-init"))
            self.assertEqual(set(shell.vfs.nodes), {"/"})
            self.assertEqual(set(load_vfs(self.source).nodes), {"/"})
            self.assertEqual(shell.cwd, "/")

    def test_reset_protects_project(self):
        """A service reset cannot erase the project or home directory."""
        for path in [Path.cwd(), Path.home(), Path.cwd().anchor]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_reset_path(path)

    def test_default(self):
        """Unspecified sources create a valid memory-only root."""
        self.assertEqual(set(load_vfs().nodes), {"/"})
        vfs = VFS()
        with self.assertRaises(ValueError):
            vfs.add("/missing/file", Node())

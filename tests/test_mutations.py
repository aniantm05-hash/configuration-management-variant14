"""Verify mutations, error atomicity, metadata, and source isolation."""

from src.loaders import load_vfs
from src.mutations import install
from src.settings import EXTRA
from tests.helpers import FixtureCase


class MutationTests(FixtureCase):
    """Add mutating handlers to the standard command fixture."""

    def setUp(self):
        """Keep a digest of the physical source before modifications."""
        super().setUp()
        self.original_digest = self.shell.vfs.digest()
        install(self.shell)

    def tearDown(self):
        """Every mutation must leave the original disk source unchanged."""
        self.assertEqual(load_vfs(self.source).digest(), self.original_digest)


    def test_chown(self):
        """Owners and groups can be assigned recursively or individually."""
        if "chown" not in EXTRA:
            return
        self.execute("chown alice /readme.txt")
        self.assertEqual(self.shell.vfs.get("/readme.txt").owner, "alice")
        self.execute("chown -R bob:staff /docs")
        node = self.shell.vfs.get("/docs/notes/deep/info.txt")
        self.assertEqual((node.owner, node.group), ("bob", "staff"))
        self.assertFalse(self.shell.execute("chown :staff /docs"))
        self.assertFalse(self.shell.execute("chown alice /missing"))


    def test_invalid_mutation_operands(self):
        """All assigned mutations reject missing operands."""
        for name in EXTRA:
            with self.subTest(command=name):
                self.assertFalse(self.shell.execute(name))

    def test_invalid_targets_are_atomic(self):
        """A missing later operand must not change earlier owners."""
        digest = self.shell.vfs.digest()
        self.assertFalse(
            self.shell.execute("chown alice /readme.txt /missing")
        )
        self.assertEqual(self.shell.vfs.digest(), digest)

    def test_recursive_root(self):
        """Recursive root ownership applies to every virtual node."""
        self.execute("chown -R anna:students /")
        for node in self.shell.vfs.nodes.values():
            self.assertEqual((node.owner, node.group), ("anna", "students"))

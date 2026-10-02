# Функции и классы


## config.py

- `load_options` — Parse the VFS path, startup script, and batch flag.

## fixtures.py

- `fixture_records` — Return minimal, multiple-file, or three-level fixture contents.
- `write_fixture` — Serialize one fixture using the variant's physical format.
- `write_directory` — Create a fixture directory without deleting existing data.
- `main` — Generate all documented fixtures under ignored .generated/.

## interface.py

- `cli` — Read terminal commands until exit, EOF, or an interrupt.
- `TerminalWindow` — Display command input and output in a Tk terminal window.
- `TerminalWindow.__init__` — Construct the window without starting its event loop.
- `TerminalWindow.write` — Append plain text without interpreting escape sequences.
- `TerminalWindow.submit` — Echo and execute one line from the entry widget.
- `TerminalWindow.run` — Enter the event loop unless a startup script already exited.
- `interact` — Select the user interface specified by the assignment.

## loaders.py

- `safe_path` — Reject traversal and ambiguous paths in serialized VFS sources.
- `ensure_parent` — Create missing parent directories in memory.
- `insert` — Insert a source entry, allowing existing directories.
- `read_directory` — Snapshot a directory, rejecting links and special files.
- `load_vfs` — Load the required format, returning an empty VFS if unspecified.

## main.py

- `create_shell` — Create a configured prototype session.
- `run` — Display options and startup dialogue in the selected interface.
- `main` — Handle input/configuration errors with a nonzero process status.

## parsing.py

- `parse` — Return command tokens without interpreting quotes or variables.

## services.py

- `validate_reset_path` — Refuse filesystem roots, home, project ancestors, and symlinks.
- `clear_source` — Reset exactly the configured source after verifying its boundary.
- `install` — Register only the service commands required by this variant.

## shell.py

- `Shell` — Keep a single interactive emulator session.
- `Shell.__init__` — Initialize the prompt, lifecycle, and command table.
- `Shell.prompt` — Include the VFS name or actual host identity in the prompt.
- `Shell.execute` — Execute one line and return success without leaking tracebacks.
- `Shell.stub_ls` — Show the ls prototype invocation.
- `Shell.stub_cd` — Show the cd prototype invocation and reject extra operands.
- `Shell.exit_command` — End the session after validating arguments.

## startup.py

- `remove_comment` — Strip Python-style comments outside quoted strings.
- `run_script` — Echo commands, report line numbers, and respect exit and errors.

## vfs.py

- `Node` — Represent a directory or a byte-preserving virtual file.
- `VFS` — Store a complete virtual filesystem in memory.
- `VFS.__init__` — Create an empty root directory.
- `VFS.resolve` — Normalize absolute/relative POSIX paths and clamp at root.
- `VFS.get` — Return a node or raise a readable missing-path error.
- `VFS.require_directory` — Validate a directory operand.
- `VFS.children` — Return immediate child paths in lexical order.
- `VFS.add` — Insert a node after validating its parent and uniqueness.
- `VFS.text` — Decode a regular file as UTF-8.
- `VFS.digest` — Hash canonical paths, contents, and stable virtual metadata.

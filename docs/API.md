# Функции проекта

## __init__.py


## base_commands.py

- `operands` - Validate operand count before executing a command.
- `install` - Replace prototypes and install this variant's read-only commands.
- `__init__` - Attach handlers to a running shell.
- `path` - Resolve a command operand relative to the current directory.
- `ls` - List a file/directory, with optional -a and -l flags.
- `listing_arguments` - Split ls flags from its optional path operand.
- `listing_line` - Format a listing entry and optional virtual metadata.
- `cd` - Change the virtual working directory; default to root.
- `tail` - Print the last ten lines, or an explicit nonnegative -n count.
- `who` - Identify the real account running this emulator session.
- `wc` - Count newline characters, words, and bytes; support -l/-w/-c.

## config.py

- `load_options` - Parse the VFS path, startup script, and batch flag.

## fixtures.py

- `fixture_records` - Return minimal, multiple-file, or three-level fixture contents.
- `write_fixture` - Serialize one fixture using the variant's physical format.
- `write_directory` - Create a fixture directory without deleting existing data.
- `main` - Generate all documented fixtures under ignored .generated/.

## interface.py

- `cli` - Read terminal commands until exit, EOF, or an interrupt.
- `interact` - Select the user interface specified by the assignment.
- `__init__` - Construct the window without starting its event loop.
- `write` - Append plain text without interpreting escape sequences.
- `submit` - Echo and execute one line from the entry widget.
- `run` - Enter the event loop unless a startup script already exited.

## loaders.py

- `safe_path` - Reject traversal and ambiguous paths in serialized VFS sources.
- `ensure_parent` - Create missing parent directories in memory.
- `insert` - Insert a source entry, allowing existing directories.
- `read_directory` - Snapshot a directory, rejecting links and special files.
- `load_vfs` - Load the required format, returning an empty VFS if unspecified.

## main.py

- `create_shell` - Create a configured prototype session.
- `run` - Display options and startup dialogue in the selected interface.
- `main` - Handle input/configuration errors with a nonzero process status.

## parsing.py

- `parse` - Return command tokens without interpreting quotes or variables.

## services.py

- `validate_reset_path` - Refuse filesystem roots, home, project ancestors, and symlinks.
- `clear_source` - Reset exactly the configured source after verifying its boundary.
- `install` - Register only the service commands required by this variant.
- `info` - Display the current VFS name and canonical SHA-256 hash.
- `reset` - Replace both the physical source and in-memory VFS with empty.

## settings.py


## shell.py

- `__init__` - Initialize the prompt, lifecycle, and command table.
- `prompt` - Include the VFS name or actual host identity in the prompt.
- `execute` - Execute one line and return success without leaking tracebacks.
- `stub_ls` - Show the ls prototype invocation.
- `stub_cd` - Show the cd prototype invocation and reject extra operands.
- `exit_command` - End the session after validating arguments.

## startup.py

- `remove_comment` - Strip Python-style comments outside quoted strings.
- `run_script` - Echo commands, report line numbers, and respect exit and errors.

## vfs.py

- `__init__` - Create an empty root directory.
- `resolve` - Normalize absolute/relative POSIX paths and clamp at root.
- `get` - Return a node or raise a readable missing-path error.
- `require_directory` - Validate a directory operand.
- `children` - Return immediate child paths in lexical order.
- `add` - Insert a node after validating its parent and uniqueness.
- `text` - Decode a regular file as UTF-8.
- `digest` - Hash canonical paths, contents, and stable virtual metadata.

# Функции и классы


## interface.py

- `cli` — Read terminal commands until exit, EOF, or an interrupt.
- `TerminalWindow` — Display command input and output in a Tk terminal window.
- `TerminalWindow.__init__` — Construct the window without starting its event loop.
- `TerminalWindow.write` — Append plain text without interpreting escape sequences.
- `TerminalWindow.submit` — Echo and execute one line from the entry widget.
- `TerminalWindow.run` — Enter the event loop unless a startup script already exited.
- `interact` — Select the user interface specified by the assignment.

## main.py

- `main` — Start the variant's CLI or GUI session.

## parsing.py

- `parse` — Return command tokens without interpreting quotes or variables.

## shell.py

- `Shell` — Keep a single interactive emulator session.
- `Shell.__init__` — Initialize the prompt, lifecycle, and command table.
- `Shell.prompt` — Include the VFS name or actual host identity in the prompt.
- `Shell.execute` — Execute one line and return success without leaking tracebacks.
- `Shell.stub_ls` — Show the ls prototype invocation.
- `Shell.stub_cd` — Show the cd prototype invocation and reject extra operands.
- `Shell.exit_command` — End the session after validating arguments.

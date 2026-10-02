"""CLI and optional Tk frontend for the same shell session."""

from .settings import GUI


def cli(shell):
    """Read terminal commands until exit, EOF, or an interrupt."""
    while shell.running:
        try:
            line = input(shell.prompt())
        except (EOFError, KeyboardInterrupt):
            break
        shell.execute(line)


class TerminalWindow:
    """Display command input and output in a Tk terminal window."""

    def __init__(self, shell):
        """Construct the window without starting its event loop."""
        import tkinter as tk
        from tkinter.scrolledtext import ScrolledText

        self.shell = shell
        self.root = tk.Tk()
        identity = shell.prompt().split(":")[0]
        self.root.title(f"Эмулятор - [{identity}]")
        self.root.geometry("820x520")
        self.history = ScrolledText(self.root, state="disabled")
        self.history.pack(fill="both", expand=True)
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()
        shell.output = self.write

    def write(self, text):
        """Append plain text without interpreting escape sequences."""
        self.history.configure(state="normal")
        self.history.insert("end", str(text) + "\n")
        self.history.see("end")
        self.history.configure(state="disabled")

    def submit(self, event=None):
        """Echo and execute one line from the entry widget."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.write(self.shell.prompt() + line)
        self.shell.execute(line)
        if not self.shell.running:
            self.root.destroy()

    def run(self):
        """Enter the event loop unless a startup script already exited."""
        if self.shell.running:
            self.root.mainloop()
        else:
            self.root.destroy()


def interact(shell):
    """Select the user interface specified by the assignment."""
    if GUI:
        TerminalWindow(shell).run()
    else:
        cli(shell)

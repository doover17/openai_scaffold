from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel

# Create a custom theme for your application
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "user": "green",
    "assistant": "blue",
    "system": "yellow",
})

# Create a console with our theme
console = Console(theme=custom_theme)

def print_user_message(message):
    """Format and print a user message."""
    console.print(Panel(message, style="user", title="You", title_align="left"))

def print_assistant_message(message):
    """Format and print an assistant message with markdown support."""
    # Process markdown in the assistant's response
    markdown = Markdown(message)
    console.print(Panel(markdown, style="assistant", title="Assistant", title_align="left"))

def print_system_message(message):
    """Format and print a system message."""
    console.print(f"[system]{message}[/system]")

def print_code(code, language="python"):
    """Format and print code with syntax highlighting."""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=f"{language} code", title_align="left"))

def print_error(message):
    """Format and print an error message."""
    console.print(f"[danger]Error: {message}[/danger]")
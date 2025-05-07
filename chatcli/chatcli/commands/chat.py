import click
import os
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from rich.progress import Progress, SpinnerColumn, TextColumn
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from chatcli.utils.formatting import (
    console,
    print_user_message,
    print_assistant_message,
    print_system_message,
    print_error,
)

# Replace click.echo statements with rich formatting
# For example, change:
# click.echo(f"\nYou> {user_input}")
# To:
# print_user_message(user_input)

# And change:
# click.echo(f"\nAssistant> {assistant_message}")
# To:
# print_assistant_message(assistant_message)


@click.command()
@click.option(
    "--interactive/--no-interactive",
    "-i/-n",
    default=True,
    help="Run in interactive mode or process a single query.",
)
@click.option(
    "--model", "-m", default="gpt-4o-mini", help="OpenAI model to use for chat."
)
@click.option("--query", "-q", help="Single query to process (non-interactive mode).")
@click.option(
    "--history-file",
    "-f",
    default="~/.chatcli_history.json",
    help="File to store chat history.",
)
@click.option(
    "--system-prompt",
    "-s",
    default="You are a helpful assistant responding to queries from the command line.",
    help="System prompt to set the AI behavior.",
)
@click.pass_context
def chat(ctx, interactive, model, query, history_file, system_prompt):
    """
    Start an interactive chat session with an AI assistant.

    This command allows you to have a conversation with an OpenAI model from the
    command line. It supports both interactive mode with persistent history and
    single-query mode.
    """
    # Expand the history file path
    history_path = Path(os.path.expanduser(history_file))

    # Load history if it exists
    history = []
    if history_path.exists():
        try:
            with open(history_path, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            click.echo("Warning: History file is corrupt. Starting fresh.")

    # Initialize OpenAI client
    client = ctx.obj["client"]

    # Create a new conversation if needed
    if not history or not interactive:
        conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        history.append(
            {
                "id": conversation_id,
                "created_at": datetime.now().isoformat(),
                "messages": [{"role": "system", "content": system_prompt}],
            }
        )

    current_conversation = history[-1]

    if not interactive:
        # Single query mode
        if not query:
            click.echo(
                "Error: --query/-q is required in non-interactive mode.", err=True
            )
            return

        current_conversation["messages"].append({"role": "user", "content": query})
        process_response(client, current_conversation, model)
        save_history(history, history_path)
        return

    # Interactive mode
    click.echo(
        f"Chat session started. Type 'exit', 'quit', or press Ctrl+C to end the conversation."
    )
    click.echo(f"Using model: {model}")

    try:
        while True:
            user_input = click.prompt("\nYou", prompt_suffix="> ")

            if user_input.lower() in ["exit", "quit"]:
                break

            current_conversation["messages"].append(
                {"role": "user", "content": user_input}
            )
            process_response(client, current_conversation, model)
            save_history(history, history_path)

    except KeyboardInterrupt:
        click.echo("\nChat session ended.")

    click.echo(f"Chat history saved to {history_path}")


def process_response(client, conversation, model):
    """Process a message and get a response from the API."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Thinking...", total=None)
        try:
            response = client.chat.completions.create(
                model=model, messages=conversation["messages"]
            )

            assistant_message = response.choices[0].message.content
            conversation["messages"].append(
                {"role": "assistant", "content": assistant_message}
            )

            print_assistant_message(assistant_message)

        except Exception as e:
            print_error(str(e))


def save_history(history, history_path):
    """Save chat history to a file."""
    history_path.parent.mkdir(parents=True, exist_ok=True)

    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

def chat_with_prompt_toolkit(ctx, model, history_file, system_prompt):
    """Interactive chat with keyboard shortcuts."""
    # Create key bindings
    bindings = KeyBindings()
    
    # Ctrl+C to exit
    @bindings.add('c-c')
    def _(event):
        event.app.exit()
    
    # Ctrl+Up to browse history
    @bindings.add('c-up')
    def _(event):
        # Implementation for browsing history up
        pass
    
    # Ctrl+Down to browse history
    @bindings.add('c-down')
    def _(event):
        # Implementation for browsing history down
        pass
    
    # Create session
    session = PromptSession(key_bindings=bindings)
    
    # Display available shortcuts
    print_system_message("Keyboard shortcuts:")
    print_system_message("Ctrl+C: Exit chat")
    print_system_message("Ctrl+Up: Browse history up")
    print_system_message("Ctrl+Down: Browse history down")
    
    # Chat loop
    while True:
        try:
            user_input = session.prompt("\nYou> ")
            
            if user_input.lower() in ['exit', 'quit']:
                break
                
            # Process response...
            
        except KeyboardInterrupt:
            break
import click


@click.command()
@click.option(
    "--history-file",
    "-f",
    default="~/.chatcli_history.json",
    help="File to store chat history.",
)
@click.option(
    "--model", "-m", default="gpt-4o-mini", help="OpenAI model to use for chat."
)
def tui(history_file, model):
    """
    Launch the full terminal user interface for ChatCLI.

    This provides a more interactive and visually appealing way to chat with the AI.
    """
    from chatcli.tui.app import run_tui

    run_tui(history_file=history_file, model=model)

#!/usr/bin/env python3
"""
ChatCLI - An interactive CLI chat application that uses OpenAI models to provide intelligent responses

A CLI application using Click and OpenAI.
"""
import os
import sys
import click
from openai import OpenAI
from dotenv import load_dotenv
from chatcli.commands import hello, chat
from chatcli.commands import tui

# Load environment variables from .env file
load_dotenv()

@click.group()
@click.version_option(version='0.1.0')
@click.pass_context
def cli(ctx):
    """
    An interactive CLI chat application that uses OpenAI models to provide intelligent responses
    """
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OPENAI_API_KEY environment variable not set.", err=True)
        click.echo("Please create a .env file with your OpenAI API key or set it in your environment.", err=True)
        sys.exit(1)
    
    # Create OpenAI client and add to context
    ctx.obj = {"client": OpenAI(api_key=api_key)}


# Register commands
cli.add_command(hello)
cli.add_command(chat)
cli.add_command(tui)

if __name__ == "__main__":
    cli()

import click
from openai import OpenAI
import json

@click.command()
@click.option('--name', '-n', default="world", help="Name to greet.")
@click.option('--ai', is_flag=True, help="Use AI to generate a response.")
@click.pass_context
def hello(ctx, name, ai):
    """
    Say hello to someone.
    
    Basic example command showing how to use OpenAI in a Click command.
    """
    if ai:
        client: OpenAI = ctx.obj["client"]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a friendly assistant."},
                {"role": "user", "content": f"Generate a creative greeting for a person named {name}."}
            ]
        )
        click.echo(response.choices[0].message.content)
    else:
        click.echo(f"Hello, {name}!")

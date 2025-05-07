# OpenAI Scaffold

A CLI tool to generate fully-structured Python projects that integrate Click and OpenAI.

## Overview

The `openai_scaffold.py` script creates complete project structures for building command-line applications that use Click for the CLI interface and OpenAI for AI capabilities. This tool eliminates the boilerplate work of setting up a new project and ensures you follow best practices for Python package development.

## Features

- ✅ Complete project structure generation
- ✅ Click-based command system with extensibility
- ✅ OpenAI API integration with proper authentication
- ✅ Testing framework with example tests
- ✅ Package setup for PyPI distribution
- ✅ Environment management for API keys
- ✅ Development tooling configuration

## Requirements

- Python 3.8+
- Click package (`pip install click`)
- Optional: `python-dotenv` for environment management
- Optional: `venv` module for virtual environment setup

## Installation

1. Download the `openai_scaffold.py` script:

```bash
curl -O https://raw.githubusercontent.com/yourusername/openai_scaffold/main/openai_scaffold.py
# or wget:
# wget https://raw.githubusercontent.com/yourusername/openai_scaffold/main/openai_scaffold.py
```

2. Make it executable:

```bash
chmod +x openai_scaffold.py
```

3. Install required dependencies:

```bash
pip install click
```

## Usage

### Basic Usage

Run the script and follow the interactive prompts:

```bash
./openai_scaffold.py
```

The script will ask for:
- Project name
- Project description
- Author name
- Author email
- Project URL (GitHub/GitLab repository)
- Other optional information

### Command-line Options

You can also provide information directly as command-line options:

```bash
./openai_scaffold.py \
  --project-name "My OpenAI CLI" \
  --project-description "A powerful CLI tool using OpenAI" \
  --author "Your Name" \
  --author-email "your.email@example.com" \
  --project-url "https://github.com/yourusername/my-openai-cli" \
  --setup-venv \
  --install-deps
```

### All Available Options

| Option | Description |
|--------|-------------|
| `--project-name` | Name of the project |
| `--project-slug` | Project slug for package name (default: derived from project name) |
| `--project-command` | CLI command name (default: derived from project slug) |
| `--project-description` | Short description of the project |
| `--version` | Initial version (default: 0.1.0) |
| `--author` | Author's name |
| `--author-email` | Author's email |
| `--project-url` | URL of the project repository |
| `--project-keywords` | Comma-separated keywords (default: "openai,ai,cli") |
| `--output-dir` | Directory to create the project in (default: current directory) |
| `--setup-venv` | Set up a virtual environment |
| `--install-deps` | Install dependencies after creation |

## Generated Project Structure

```
your_project/
├── your_project/            # Main package directory
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Main CLI entry point
│   └── commands/            # Command modules
│       ├── __init__.py
│       └── hello.py         # Example command
├── tests/                   # Test directory
│   ├── __init__.py
│   └── test_hello.py        # Example tests
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore file
├── README.md                # Project README
├── pyproject.toml           # Project configuration
└── setup.py                 # Package setup
```

## Using Your Generated Project

After generating your project:

1. Change to the project directory:

```bash
cd your_project
```

2. Create a `.env` file with your OpenAI API key:

```bash
cp .env.example .env
# Edit .env with your API key
```

3. Install the package in development mode:

```bash
pip install -e .
```

4. Run your CLI:

```bash
your-project-command --help
```

5. Test the example command:

```bash
your-project-command hello --name "Your Name"
```

6. Try the AI-powered example:

```bash
your-project-command hello --name "Your Name" --ai
```

## Extending Your Project

### Adding New Commands

1. Create a new file in the `commands` directory:

```python
# your_project/your_project/commands/new_command.py
import click

@click.command()
@click.option('--option', help='Description of the option')
@click.pass_context
def new_command(ctx, option):
    """
    Description of what the command does.
    """
    client = ctx.obj["client"]  # Access the OpenAI client
    click.echo(f"Executing new command with option: {option}")
    # Add your OpenAI implementation here
```

2. Register your command in `commands/__init__.py`:

```python
from .hello import hello
from .new_command import new_command
# Import your other commands here
```

3. Add the command to the CLI group in `main.py`:

```python
# Add to the imports
from .commands import hello, new_command

# Add to the registration
cli.add_command(hello)
cli.add_command(new_command)
```

## Testing

The generated project includes a testing framework using pytest:

```bash
pip install pytest
pytest
```

## Distribution

When ready to distribute your package:

```bash
pip install build twine
python -m build
twine upload dist/*
```

## License

This script is provided under the MIT License.
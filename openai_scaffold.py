#!/usr/bin/env python3
"""
openai_scaffold - A CLI tool to generate a fully-structured Click + OpenAI project

This tool creates a complete project structure with all necessary files for a Python CLI 
application that uses Click for the command-line interface and OpenAI for AI capabilities.
"""
import os
import sys
import click
import shutil
from pathlib import Path
import subprocess

TEMPLATE_FILES = {
    "main.py": """#!/usr/bin/env python3
\"\"\"
{project_name} - {project_description}

A CLI application using Click and OpenAI.
\"\"\"
import os
import sys
import click
from openai import OpenAI
from dotenv import load_dotenv
from .commands import *

# Load environment variables from .env file
load_dotenv()

@click.group()
@click.version_option(version='{version}')
@click.pass_context
def cli(ctx):
    \"\"\"
    {project_description}
    \"\"\"
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OPENAI_API_KEY environment variable not set.", err=True)
        click.echo("Please create a .env file with your OpenAI API key or set it in your environment.", err=True)
        sys.exit(1)
    
    # Create OpenAI client and add to context
    ctx.obj = {{"client": OpenAI(api_key=api_key)}}


# Register commands
cli.add_command(hello)

if __name__ == "__main__":
    cli()
""",
    "commands/hello.py": """import click
from openai import OpenAI
import json

@click.command()
@click.option('--name', '-n', default="world", help="Name to greet.")
@click.option('--ai', is_flag=True, help="Use AI to generate a response.")
@click.pass_context
def hello(ctx, name, ai):
    \"\"\"
    Say hello to someone.
    
    Basic example command showing how to use OpenAI in a Click command.
    \"\"\"
    if ai:
        client: OpenAI = ctx.obj["client"]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {{"role": "system", "content": "You are a friendly assistant."}},
                {{"role": "user", "content": f"Generate a creative greeting for a person named {{name}}."}}
            ]
        )
        click.echo(response.choices[0].message.content)
    else:
        click.echo(f"Hello, {{name}}!")
""",
    "commands/__init__.py": """from .hello import hello
# Import your other commands here
""",
    "setup.py": """from setuptools import setup, find_packages

setup(
    name="{project_slug}",
    version="{version}",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points='''
        [console_scripts]
        {project_command}={project_slug}.main:cli
    ''',
    python_requires='>=3.8',
    author="{author}",
    author_email="{author_email}",
    description="{project_description}",
    keywords="{project_keywords}",
    url="{project_url}",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
""",
    "__init__.py": """\"\"\"
{project_name} package.
\"\"\"

__version__ = '{version}'
""",
    "README.md": """# {project_name}

{project_description}

## Installation

```bash
pip install {project_slug}
```

Or for development:

```bash
git clone {project_url}.git
cd {project_slug}
pip install -e .
```

## Environment Setup

Create a `.env` file in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

```bash
{project_command} --help
```

### Commands

#### hello

```bash
{project_command} hello --name YourName
{project_command} hello --name YourName --ai
```

## Development

### Running Tests

```bash
pytest
```

## License

MIT
""",
    ".env.example": """# OpenAI API key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Optional configurations
# OPENAI_ORG_ID=your_organization_id
""",
    ".gitignore": """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# Virtual environments
venv/
env/
.env

# IDE files
.vscode/
.idea/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Local development
*.log
.DS_Store
""",
    "tests/__init__.py": "",
    "tests/test_hello.py": """import pytest
from click.testing import CliRunner
from {project_slug}.main import cli

def test_hello_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['hello'])
    assert result.exit_code == 0
    assert 'Hello, world!' in result.output

def test_hello_with_name():
    runner = CliRunner()
    result = runner.invoke(cli, ['hello', '--name', 'Test'])
    assert result.exit_code == 0
    assert 'Hello, Test!' in result.output
""",
    "pyproject.toml": """[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
""",
}


@click.command()
@click.option("--project-name", prompt="Project name", help="Name of the project")
@click.option("--project-slug", help="Project slug (used for package name)", default=None)
@click.option("--project-command", help="CLI command name to use", default=None)
@click.option("--project-description", prompt="Project description", help="Short description of the project")
@click.option("--version", default="0.1.0", help="Initial version")
@click.option("--author", prompt="Author name", help="Author's name")
@click.option("--author-email", prompt="Author email", help="Author's email")
@click.option("--project-url", prompt="Project URL", help="URL of the project repository")
@click.option("--project-keywords", default="openai,ai,cli", help="Comma-separated keywords")
@click.option("--output-dir", default=".", help="Directory to create the project in")
@click.option("--setup-venv", is_flag=True, help="Set up a virtual environment")
@click.option("--install-deps", is_flag=True, help="Install dependencies after creation")
def create_project(
    project_name, project_slug, project_command, project_description, version, 
    author, author_email, project_url, project_keywords, output_dir, 
    setup_venv, install_deps
):
    """
    Generate a fully-structured Click + OpenAI project.
    
    This command creates a complete project structure with all necessary files
    for a Python CLI application that uses Click for the command-line interface
    and OpenAI for AI capabilities.
    """
    # Set defaults for optional parameters
    if not project_slug:
        project_slug = project_name.lower().replace(" ", "_").replace("-", "_")
    
    if not project_command:
        project_command = project_slug.replace("_", "-")
    
    # Create project directory
    project_dir = Path(output_dir) / project_slug
    if project_dir.exists():
        if click.confirm(f"Directory {project_dir} already exists. Overwrite?", default=False):
            shutil.rmtree(project_dir)
        else:
            click.echo("Aborted.")
            return
    
    # Create package directory
    package_dir = project_dir / project_slug
    package_dir.mkdir(parents=True)
    (package_dir / "commands").mkdir()
    (project_dir / "tests").mkdir()
    
    # Create files from templates
    context = {
        "project_name": project_name,
        "project_slug": project_slug,
        "project_command": project_command,
        "project_description": project_description,
        "version": version,
        "author": author,
        "author_email": author_email,
        "project_url": project_url,
        "project_keywords": project_keywords,
    }
    
    click.echo(f"Creating project structure in {project_dir}...")
    
    # Create files
    for filename, template in TEMPLATE_FILES.items():
        if filename.startswith("__init__"):
            filepath = package_dir / filename
        elif filename.startswith("commands/"):
            filepath = package_dir / "commands" / filename.split("/")[1]
        elif filename.startswith("tests/"):
            filepath = project_dir / "tests" / filename.split("/")[1]
        else:
            filepath = project_dir / filename
        
        # Format template with context
        content = template.format(**context)
        
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(filepath, "w") as f:
            f.write(content)
    
    # Create virtual environment if requested
    if setup_venv:
        click.echo("Setting up virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(project_dir / "venv")], check=True)
            click.echo("Virtual environment created.")
        except subprocess.CalledProcessError:
            click.echo("Failed to create virtual environment.", err=True)
    
    # Install dependencies if requested
    if install_deps:
        click.echo("Installing dependencies...")
        pip_cmd = str(project_dir / "venv" / "bin" / "pip") if setup_venv else "pip"
        
        try:
            subprocess.run([pip_cmd, "install", "-e", "."], cwd=project_dir, check=True)
            click.echo("Dependencies installed.")
        except subprocess.CalledProcessError:
            click.echo("Failed to install dependencies.", err=True)
    
    click.echo(f"""
Project '{project_name}' created successfully!

Next steps:
1. Change to project directory: cd {project_slug}
2. Create a .env file with your OpenAI API key (copy from .env.example)
3. Install the package: pip install -e .
4. Run your CLI: {project_command} --help

Enjoy building with Click and OpenAI!
""")


if __name__ == "__main__":
    create_project()
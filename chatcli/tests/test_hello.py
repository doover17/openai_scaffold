import pytest
from click.testing import CliRunner
from chatcli.main import cli

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

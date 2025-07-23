"""Tests for CLI interface."""

from click.testing import CliRunner

from stacking_pr.cli import cli


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "stacking-pr: A tool for managing stacked pull requests" in result.output
    assert "Commands:" in result.output


def test_cli_version():
    """Test CLI version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_cli_commands_available():
    """Test that all expected commands are available."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    expected_commands = ["init", "create", "push", "merge", "status"]

    for cmd in expected_commands:
        assert cmd in result.output

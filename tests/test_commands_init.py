"""Tests for init command."""

from unittest.mock import patch

from click.testing import CliRunner

from stacking_pr.cli import cli


@patch("stacking_pr.commands.init.is_git_repo")
@patch("stacking_pr.commands.init.init_git_repo")
@patch("stacking_pr.commands.init.save_config")
def test_init_creates_git_repo(mock_save_config, mock_init_git, mock_is_git):
    """Test init creates git repo when not in one."""
    mock_is_git.return_value = False
    mock_init_git.return_value = True
    mock_save_config.return_value = True

    runner = CliRunner()
    result = runner.invoke(cli, ["init"])

    assert result.exit_code == 0
    assert "Initialized new git repository" in result.output
    mock_init_git.assert_called_once()


@patch("stacking_pr.commands.init.is_git_repo")
@patch("stacking_pr.commands.init.save_config")
def test_init_in_existing_repo(mock_save_config, mock_is_git):
    """Test init in existing git repo."""
    mock_is_git.return_value = True
    mock_save_config.return_value = True

    runner = CliRunner()
    result = runner.invoke(cli, ["init"])

    assert result.exit_code == 0
    assert "Repository configured for stacking-pr" in result.output


@patch("stacking_pr.commands.init.is_git_repo")
@patch("stacking_pr.commands.init.init_git_repo")
def test_init_git_creation_fails(mock_init_git, mock_is_git):
    """Test init when git repo creation fails."""
    mock_is_git.return_value = False
    mock_init_git.return_value = False

    runner = CliRunner()
    result = runner.invoke(cli, ["init"])

    assert result.exit_code == 1
    assert "Failed to initialize git repository" in result.output

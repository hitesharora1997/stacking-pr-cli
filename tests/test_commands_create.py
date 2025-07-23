"""Tests for create command."""

from unittest.mock import patch

from click.testing import CliRunner

from stacking_pr.cli import cli


@patch("stacking_pr.commands.create.is_git_repo")
def test_create_not_in_git_repo(mock_is_git):
    """Test create command when not in a git repository."""
    mock_is_git.return_value = False

    runner = CliRunner()
    result = runner.invoke(cli, ["create", "feature"])

    assert result.exit_code == 1
    assert "Not in a git repository" in result.output


@patch("stacking_pr.commands.create.is_git_repo")
@patch("stacking_pr.commands.create.branch_exists")
def test_create_branch_already_exists(mock_branch_exists, mock_is_git):
    """Test create when branch already exists."""
    mock_is_git.return_value = True
    mock_branch_exists.return_value = True

    runner = CliRunner()
    result = runner.invoke(cli, ["create", "feature"])

    assert result.exit_code == 1
    assert "Branch 'feature' already exists" in result.output


@patch("stacking_pr.commands.create.is_git_repo")
@patch("stacking_pr.commands.create.branch_exists")
@patch("stacking_pr.commands.create.get_current_branch")
@patch("stacking_pr.commands.create.create_branch")
@patch("stacking_pr.commands.create.add_to_stack")
def test_create_branch_success(
    mock_add_to_stack,
    mock_create_branch,
    mock_get_current,
    mock_branch_exists,
    mock_is_git,
):
    """Test successful branch creation."""
    mock_is_git.return_value = True
    mock_branch_exists.return_value = False
    mock_get_current.return_value = "main"
    mock_create_branch.return_value = True
    mock_add_to_stack.return_value = True

    runner = CliRunner()
    result = runner.invoke(cli, ["create", "feature"])

    assert result.exit_code == 0
    assert "Created branch 'feature'" in result.output
    mock_create_branch.assert_called_once_with("feature", "main")
    mock_add_to_stack.assert_called_once_with("feature", "main")

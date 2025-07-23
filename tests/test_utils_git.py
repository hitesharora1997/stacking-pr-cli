"""Tests for git utilities."""

from unittest.mock import MagicMock, patch

from stacking_pr.utils.git import (
    branch_exists,
    create_branch,
    get_current_branch,
    init_git_repo,
    is_git_repo,
    run_git_command,
)


@patch("os.path.exists")
def test_is_git_repo_true(mock_exists):
    """Test is_git_repo returns True when in a git repo."""
    mock_exists.return_value = True
    assert is_git_repo() is True
    mock_exists.assert_called_once_with(".git")


@patch("os.path.exists")
def test_is_git_repo_false(mock_exists):
    """Test is_git_repo returns False when not in a git repo."""
    mock_exists.return_value = False
    assert is_git_repo() is False


@patch("subprocess.run")
def test_run_git_command(mock_run):
    """Test run_git_command executes git commands."""
    mock_run.return_value = MagicMock(returncode=0, stdout="output\n")
    result = run_git_command(["status"])
    assert result == "output"
    mock_run.assert_called_once_with(
        ["git", "status"],
        capture_output=True,
        text=True,
        check=True,
    )


@patch("stacking_pr.utils.git.run_git_command")
def test_get_current_branch(mock_run_git):
    """Test get_current_branch returns current branch name."""
    mock_run_git.return_value = "feature-branch"
    assert get_current_branch() == "feature-branch"
    mock_run_git.assert_called_once_with(["rev-parse", "--abbrev-ref", "HEAD"])


@patch("stacking_pr.utils.git.run_git_command")
def test_branch_exists_true(mock_run_git):
    """Test branch_exists returns True when branch exists."""
    mock_run_git.return_value = "ref: refs/heads/feature"
    assert branch_exists("feature") is True


@patch("stacking_pr.utils.git.run_git_command")
def test_branch_exists_false(mock_run_git):
    """Test branch_exists returns False when branch doesn't exist."""
    mock_run_git.return_value = None
    assert branch_exists("nonexistent") is False


@patch("stacking_pr.utils.git.run_git_command")
def test_create_branch_success(mock_run_git):
    """Test create_branch successfully creates a branch."""
    mock_run_git.return_value = "Switched to a new branch"

    result = create_branch("new-feature", "main")

    assert result is True
    mock_run_git.assert_called_with(["checkout", "-b", "new-feature", "main"])


@patch("stacking_pr.utils.git.run_git_command")
def test_create_branch_failure(mock_run_git):
    """Test create_branch returns False on failure."""
    mock_run_git.return_value = None

    result = create_branch("new-feature", "main")

    assert result is False


@patch("stacking_pr.utils.git.run_git_command")
def test_init_git_repo(mock_run_git):
    """Test init_git_repo initializes a repository."""
    mock_run_git.return_value = "Initialized empty Git repository"

    result = init_git_repo()

    assert result is True
    mock_run_git.assert_called_once_with(["init"])

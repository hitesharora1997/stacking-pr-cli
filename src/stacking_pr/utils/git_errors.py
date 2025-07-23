"""Git error handling utilities."""

import subprocess


class GitError(Exception):
    """Base exception for git-related errors."""

    pass


class NotInGitRepoError(GitError):
    """Raised when not in a git repository."""

    pass


class DetachedHeadError(GitError):
    """Raised when in detached HEAD state."""

    pass


class UncommittedChangesError(GitError):
    """Raised when there are uncommitted changes."""

    pass


class BranchNotFoundError(GitError):
    """Raised when a branch is not found."""

    pass


def check_git_state():
    """Check git repository state and raise appropriate errors."""
    # Check if in git repo
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"], capture_output=True, check=True
        )
    except subprocess.CalledProcessError:
        raise NotInGitRepoError(
            "Not in a git repository. Run 'stacking-pr init' first."
        )

    # Check for detached HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "-q", "HEAD"], capture_output=True, text=True
        )
        if result.returncode != 0:
            raise DetachedHeadError(
                "Currently in detached HEAD state. Please checkout a branch."
            )
    except subprocess.CalledProcessError:
        raise DetachedHeadError(
            "Currently in detached HEAD state. Please checkout a branch."
        )


def has_uncommitted_changes():
    """Check if there are uncommitted changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    return bool(result.stdout.strip())

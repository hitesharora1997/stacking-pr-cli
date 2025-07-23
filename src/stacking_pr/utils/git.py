"""Git operations utilities."""

import os
import subprocess


def run_git_command(cmd, check=True):
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            ["git"] + cmd, capture_output=True, text=True, check=check
        )
        if result.returncode != 0 and check:
            return None
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception:
        # Catch any other unexpected errors
        return None


def is_git_repo():
    """Check if the current directory is a git repository."""
    return os.path.exists(".git")


def init_git_repo():
    """Initialize a new git repository."""
    return run_git_command(["init"]) is not None


def get_current_branch():
    """Get the name of the current branch."""
    return run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])


def branch_exists(branch_name):
    """Check if a branch exists."""
    result = run_git_command(
        ["show-ref", "--verify", f"refs/heads/{branch_name}"], check=False
    )
    return result is not None


def create_branch(branch_name, base_branch):
    """Create a new branch from a base branch."""
    return run_git_command(["checkout", "-b", branch_name, base_branch]) is not None


def checkout_branch(branch_name):
    """Checkout an existing branch."""
    return run_git_command(["checkout", branch_name]) is not None


def push_branch(branch_name, force=False):
    """Push a branch to remote."""
    cmd = ["push", "origin", branch_name]
    if force:
        cmd.append("--force-with-lease")
    return run_git_command(cmd) is not None


def merge_branch(branch_name, into_branch="main"):
    """Merge a branch into another branch."""
    current = get_current_branch()
    if current != into_branch:
        if not checkout_branch(into_branch):
            return False

    success = run_git_command(["merge", branch_name]) is not None

    if current != into_branch:
        checkout_branch(current)

    return success


def get_commit_count(from_branch, to_branch):
    """Get the number of commits between two branches."""
    result = run_git_command(["rev-list", "--count", f"{from_branch}..{to_branch}"])
    return int(result) if result else 0


def get_commit_messages(from_branch, to_branch):
    """Get commit messages between two branches."""
    result = run_git_command(
        ["log", "--pretty=format:%s", f"{from_branch}..{to_branch}"]
    )
    return result.split("\n") if result else []


def get_remote_url():
    """Get the remote repository URL."""
    return run_git_command(["config", "--get", "remote.origin.url"])


def get_repo_info():
    """Get repository owner and name from remote URL."""
    url = get_remote_url()
    if not url:
        return None, None

    # Handle different URL formats
    if url.startswith("git@"):
        # SSH format: git@github.com:owner/repo.git
        parts = url.split(":")[-1].replace(".git", "").split("/")
    else:
        # HTTPS format: https://github.com/owner/repo.git
        parts = url.replace(".git", "").split("/")[-2:]

    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, None

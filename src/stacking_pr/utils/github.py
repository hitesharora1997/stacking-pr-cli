"""GitHub integration utilities using gh CLI."""

import json
import subprocess

from .git import get_commit_messages


def run_gh_command(cmd, check=True):
    """Run a gh CLI command and return the output."""
    try:
        result = subprocess.run(
            ["gh"] + cmd, capture_output=True, text=True, check=check
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        # gh CLI not installed
        return None


def is_gh_available():
    """Check if gh CLI is available and authenticated."""
    result = run_gh_command(["auth", "status"], check=False)
    return result is not None and "Logged in" in result


def create_or_update_pr(branch_name, base_branch=None, draft=False):
    """Create or update a pull request for a branch."""
    if not is_gh_available():
        return None

    # Check if PR already exists
    existing_pr = get_pr_info(branch_name)
    if existing_pr:
        # Update existing PR
        repo = existing_pr["repository"]["nameWithOwner"]
        pr_num = existing_pr["number"]
        return f"https://github.com/{repo}/pull/{pr_num}"

    # Create new PR
    cmd = ["pr", "create", "--head", branch_name]

    if base_branch:
        cmd.extend(["--base", base_branch])

    if draft:
        cmd.append("--draft")

    # Generate PR title from commit messages
    commits = get_commit_messages(base_branch or "main", branch_name)
    if commits:
        title = commits[0]  # Use first commit as title
        body = "\n".join(f"- {msg}" for msg in commits)
        cmd.extend(["--title", title, "--body", body])
    else:
        cmd.extend(["--title", f"Changes from {branch_name}"])

    result = run_gh_command(cmd)
    return result if result else None


def get_pr_info(branch_name):
    """Get pull request information for a branch."""
    if not is_gh_available():
        return None

    result = run_gh_command(
        ["pr", "view", branch_name, "--json", "number,state,title,url,repository"]
    )
    if result:
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return None
    return None


def get_pr_status(pr_number):
    """Get the status of a pull request."""
    if not is_gh_available():
        return "unknown"

    result = run_gh_command(
        ["pr", "view", str(pr_number), "--json", "state,mergeable,reviews"]
    )
    if result:
        try:
            data = json.loads(result)
            state = data.get("state", "unknown")
            mergeable = data.get("mergeable", "UNKNOWN")

            if state == "CLOSED":
                return "closed"
            elif state == "MERGED":
                return "merged"
            elif mergeable == "CONFLICTING":
                return "conflicts"
            elif data.get("reviews"):
                approved = any(r.get("state") == "APPROVED" for r in data["reviews"])
                if approved:
                    return "approved"
            return "open"
        except json.JSONDecodeError:
            return "unknown"
    return "unknown"


def merge_pr(pr_number):
    """Merge a pull request."""
    if not is_gh_available():
        return False

    result = run_gh_command(
        ["pr", "merge", str(pr_number), "--merge", "--delete-branch"]
    )
    return result is not None


def list_prs(state="open"):
    """List pull requests."""
    if not is_gh_available():
        return []

    result = run_gh_command(
        ["pr", "list", "--state", state, "--json", "number,title,headRefName"]
    )
    if result:
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return []
    return []

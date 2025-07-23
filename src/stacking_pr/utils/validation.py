"""Input validation utilities."""

import re


def is_valid_branch_name(branch_name):
    """
    Validate if a branch name is valid for git.

    Git branch names must:
    - Not contain whitespace
    - Not contain special characters like ~, ^, :, ?, *, [, \\, ..
    - Not end with a dot or slash
    - Not contain consecutive dots
    - Not be empty
    """
    if not branch_name or not branch_name.strip():
        return False

    # Check for invalid characters
    invalid_chars = r"[\s~^:?*\[\]\\]"
    if re.search(invalid_chars, branch_name):
        return False

    # Check for consecutive dots
    if ".." in branch_name:
        return False

    # Check if ends with dot or slash
    if branch_name.endswith(".") or branch_name.endswith("/"):
        return False

    # Check for other git-specific invalid patterns
    invalid_patterns = [
        r"^\.",  # starts with dot
        r"@\{",  # contains @{
        r"\.lock$",  # ends with .lock
    ]

    for pattern in invalid_patterns:
        if re.search(pattern, branch_name):
            return False

    return True


def sanitize_commit_message(message):
    """
    Sanitize commit message to prevent shell injection.

    Returns a safely escaped message.
    """
    if not message:
        return ""

    # Remove null bytes
    message = message.replace("\x00", "")

    # Escape single quotes by replacing them with '\''
    message = message.replace("'", "'\"'\"'")

    return message

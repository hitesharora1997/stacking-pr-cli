"""Create a new branch in the stack."""

import click

from ..utils.git import (
    branch_exists,
    checkout_branch,
    create_branch,
    get_current_branch,
)
from ..utils.git_errors import GitError, check_git_state
from ..utils.stack import add_to_stack, get_stack_info
from ..utils.validation import is_valid_branch_name


@click.command()
@click.argument("branch_name")
@click.option(
    "--base", "-b", help="Base branch for the new branch (defaults to current branch)"
)
@click.option(
    "--checkout/--no-checkout",
    default=True,
    help="Whether to checkout the new branch after creation",
)
def create(branch_name, base, checkout):
    """
    Create a new branch in the stack.

    BRANCH_NAME: Name for the new stacked branch
    """
    # Check git state
    try:
        check_git_state()
    except GitError as e:
        click.echo(f"Error: {e}", err=True)
        return

    # Validate branch name
    if not is_valid_branch_name(branch_name):
        click.echo(f"Error: Invalid branch name '{branch_name}'.", err=True)
        click.echo(
            r"Branch names cannot contain spaces, special characters "
            r"(~^:?*[\), consecutive dots, or end with a dot/slash.",
            err=True,
        )
        return

    if branch_exists(branch_name):
        click.echo(f"Error: Branch '{branch_name}' already exists.", err=True)
        return

    # Get base branch
    if not base:
        base = get_current_branch()
        if not base:
            click.echo("Error: Could not determine current branch.", err=True)
            return

    # Create the branch
    if not create_branch(branch_name, base):
        click.echo(f"Error: Failed to create branch '{branch_name}'.", err=True)
        return

    # Add to stack tracking
    add_to_stack(branch_name, base)

    # Checkout if requested
    if checkout:
        checkout_branch(branch_name)
        click.echo(
            f"✅ Created and checked out branch '{branch_name}' based on '{base}'"
        )
    else:
        click.echo(f"✅ Created branch '{branch_name}' based on '{base}'")

    # Show stack info
    stack_info = get_stack_info()
    if stack_info:
        click.echo(f"\nCurrent stack depth: {len(stack_info)} branches")

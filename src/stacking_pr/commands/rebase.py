"""Rebase command implementation."""

import click

from ..utils.git import (
    checkout_branch,
    get_current_branch,
    run_git_command,
)
from ..utils.stack import get_stack_info


@click.command()
@click.option(
    "--stack", "-s", help="Rebase entire stack (otherwise just current branch)"
)
@click.option(
    "--onto", help="Branch to rebase onto (defaults to base branch from config)"
)
@click.option("--interactive", "-i", is_flag=True, help="Interactive rebase")
def rebase(stack, onto, interactive):
    """
    Rebase current branch or entire stack.

    This command helps maintain a clean history by rebasing your branches
    onto their base branches, resolving any conflicts that arise.
    """
    current_branch = get_current_branch()
    if not current_branch:
        click.echo("Error: Not on a valid branch", err=True)
        return

    stack_info = get_stack_info()

    if stack:
        # Rebase entire stack
        click.echo("Rebasing entire stack...")
        branches_to_rebase = []

        # Build dependency order
        for branch, info in stack_info.items():
            branches_to_rebase.append((branch, info.get("base", "main")))

        # Sort by dependency
        branches_to_rebase.sort(key=lambda x: 0 if x[1] == "main" else 1)

        for branch, base in branches_to_rebase:
            click.echo(f"\nRebasing {branch} onto {base}...")
            if not checkout_branch(branch):
                click.echo(f"Error: Failed to checkout {branch}", err=True)
                return

            if not _perform_rebase(base, interactive):
                click.echo(f"Error: Rebase failed for {branch}", err=True)
                click.echo("Please resolve conflicts and run 'git rebase --continue'")
                return

        # Return to original branch
        checkout_branch(current_branch)
        click.echo("\n✅ Stack rebase complete!")

    else:
        # Rebase just current branch
        if current_branch not in stack_info:
            click.echo(
                f"Error: Branch '{current_branch}' is not part of a stack", err=True
            )
            return

        base = onto or stack_info[current_branch].get("base", "main")
        click.echo(f"Rebasing {current_branch} onto {base}...")

        if not _perform_rebase(base, interactive):
            click.echo("Error: Rebase failed", err=True)
            click.echo("Please resolve conflicts and run 'git rebase --continue'")
            return

        click.echo(f"✅ Rebased {current_branch} onto {base}")


def _perform_rebase(onto_branch, interactive=False):
    """Perform the actual rebase operation."""
    cmd = ["rebase"]
    if interactive:
        # Note: Interactive rebase won't work in non-interactive context
        click.echo("Warning: Interactive rebase requires manual interaction", err=True)
        return False

    cmd.append(onto_branch)
    result = run_git_command(cmd, check=False)

    return result is not None

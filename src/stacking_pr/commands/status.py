"""Show the status of the current stack."""

import click

from ..utils.git import get_commit_count, get_current_branch
from ..utils.github import get_pr_status
from ..utils.stack import get_stack_info, get_stack_tree


@click.command()
@click.option(
    "--verbose", "-v", is_flag=True, help="Show detailed information about each branch"
)
@click.option("--prs", is_flag=True, help="Show associated pull request information")
def status(verbose, prs):
    """
    Show the status of the current stack.

    This command displays the structure of your stacked branches
    and optionally shows associated pull requests.
    """
    current_branch = get_current_branch()
    if not current_branch:
        click.echo("Error: Not in a git repository.", err=True)
        return

    stack_info = get_stack_info()
    if not stack_info:
        click.echo("No stacked branches found in this repository.")
        click.echo("Run 'stacking-pr init' to get started.")
        return

    # Display stack tree
    click.echo("📚 Stack Overview:")
    click.echo("=" * 50)

    tree = get_stack_tree(stack_info)
    for line in tree:
        if current_branch in line:
            click.echo(click.style(line, fg="green", bold=True))
        else:
            click.echo(line)

    if verbose:
        click.echo("\n📊 Branch Details:")
        click.echo("-" * 50)
        for branch_name, info in stack_info.items():
            click.echo(f"\n{branch_name}:")
            click.echo(f"  Base: {info['base']}")
            commits = get_commit_count(info["base"], branch_name)
            click.echo(f"  Commits: {commits}")

            if prs and info.get("pr_number"):
                pr_status = get_pr_status(info["pr_number"])
                click.echo(f"  PR: #{info['pr_number']} ({pr_status})")

    click.echo("\n💡 Tips:")
    click.echo("  • Create new branch: stacking-pr create <name>")
    click.echo("  • Push stack: stacking-pr push")
    click.echo("  • Merge stack: stacking-pr merge")

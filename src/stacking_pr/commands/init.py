"""Initialize a repository for stacked PR workflow."""

import os

import click

from ..utils.config import create_config_file
from ..utils.git import init_git_repo, is_git_repo


@click.command()
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force initialization even if already initialized",
)
def init(force):
    """
    Initialize a repository for stacked PR workflow.

    This command sets up the necessary configuration and hooks
    for managing stacked pull requests in your repository.
    """
    # Check if we're in a git repository
    if not is_git_repo() and not init_git_repo():
        click.echo(
            "Error: Not in a git repository and failed to initialize one.", err=True
        )
        return

    # Check if already initialized
    config_path = ".stacking-pr.yml"
    if os.path.exists(config_path) and not force:
        click.echo("Repository already initialized for stacked PRs.")
        click.echo("Use --force to reinitialize.")
        return

    # Create configuration file
    create_config_file(config_path)

    click.echo("✅ Repository initialized for stacked PR workflow!")
    click.echo("\nNext steps:")
    click.echo(
        "  1. Create your first stacked branch: stacking-pr create <branch-name>"
    )
    click.echo("  2. Make your changes and commit them")
    click.echo("  3. Push your stack: stacking-pr push")

"""
Main CLI interface for stacking-pr tool.
"""

import click

from .commands import create, init, merge, push, rebase, status
from .version import get_version


@click.group()
@click.version_option(version=get_version(), prog_name="stacking-pr")
@click.pass_context
def cli(ctx):
    """
    stacking-pr: A tool for managing stacked pull requests.

    This tool helps you maintain a clean git history by managing
    stacked (dependent) pull requests, making it easier to create
    focused, reviewable changes.
    """
    ctx.ensure_object(dict)


# Add commands to the CLI group
cli.add_command(init.init)
cli.add_command(create.create)
cli.add_command(status.status)
cli.add_command(push.push)
cli.add_command(merge.merge)
cli.add_command(rebase.rebase)


if __name__ == "__main__":
    cli()

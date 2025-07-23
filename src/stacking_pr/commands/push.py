"""Push branches and create/update pull requests."""

import click

from ..utils.git import get_current_branch, push_branch
from ..utils.github import create_or_update_pr
from ..utils.stack import get_stack_info, get_stack_order


@click.command()
@click.option("--all", "-a", is_flag=True, help="Push all branches in the stack")
@click.option(
    "--create-prs", is_flag=True, help="Create pull requests for branches without them"
)
@click.option("--draft", is_flag=True, help="Create pull requests as drafts")
def push(all, create_prs, draft):
    """
    Push branches and optionally create pull requests.

    By default, pushes only the current branch. Use --all to push
    the entire stack in the correct order.
    """
    if all:
        # Get stack order for pushing
        stack_order = get_stack_order()
        if not stack_order:
            click.echo("No stacked branches to push.")
            return

        click.echo(f"Pushing {len(stack_order)} branches in stack order...")

        for i, branch in enumerate(stack_order, 1):
            click.echo(f"\n[{i}/{len(stack_order)}] Pushing {branch}...")
            if push_branch(branch):
                click.echo(f"✅ Pushed {branch}")

                if create_prs:
                    # Determine base branch from stack dependencies
                    stack_info = get_stack_info()
                    base = stack_info.get(branch, {}).get("base", "main")
                    pr_url = create_or_update_pr(branch, base, draft=draft)
                    if pr_url:
                        click.echo(f"📝 PR created/updated: {pr_url}")
            else:
                click.echo(f"❌ Failed to push {branch}", err=True)
                if click.confirm("Continue with remaining branches?"):
                    continue
                else:
                    break
    else:
        # Push only current branch
        current = get_current_branch()
        if not current:
            click.echo("Error: Could not determine current branch.", err=True)
            return

        click.echo(f"Pushing {current}...")
        if push_branch(current):
            click.echo(f"✅ Pushed {current}")

            if create_prs:
                # Determine base branch from stack config
                stack_info = get_stack_info()
                base = stack_info.get(current, {}).get("base", "main")
                pr_url = create_or_update_pr(current, base, draft=draft)
                if pr_url:
                    click.echo(f"📝 PR created/updated: {pr_url}")
        else:
            click.echo(f"❌ Failed to push {current}", err=True)

"""Merge stacked branches in order."""

import click

from ..utils.git import get_current_branch, merge_branch, run_git_command
from ..utils.github import get_pr_info, merge_pr
from ..utils.stack import get_stack_order, remove_from_stack


@click.command()
@click.option(
    "--branch", "-b", help="Specific branch to merge (defaults to current branch)"
)
@click.option(
    "--cascade",
    is_flag=True,
    help="Merge all branches up to and including the specified branch",
)
@click.option(
    "--delete-branches", is_flag=True, help="Delete branches after successful merge"
)
def merge(branch, cascade, delete_branches):
    """
    Merge stacked branches in the correct order.

    This command ensures that branches are merged in the proper
    sequence to maintain a clean history.
    """
    # Determine target branch
    target_branch = branch or get_current_branch()
    if not target_branch:
        click.echo("Error: Could not determine branch to merge.", err=True)
        return

    # Get branches to merge
    if cascade:
        stack_order = get_stack_order()
        try:
            target_index = stack_order.index(target_branch)
            branches_to_merge = stack_order[: target_index + 1]
        except ValueError:
            click.echo(f"Error: Branch '{target_branch}' not found in stack.", err=True)
            return
    else:
        branches_to_merge = [target_branch]

    click.echo(f"Merging {len(branches_to_merge)} branch(es)...")

    merged_branches = []
    for branch in branches_to_merge:
        click.echo(f"\nMerging {branch}...")

        # Check for associated PR
        pr_info = get_pr_info(branch)
        if pr_info and pr_info["state"] == "open":
            if click.confirm(f"Merge PR #{pr_info['number']} for {branch}?"):
                if merge_pr(pr_info["number"]):
                    click.echo(f"✅ Merged PR #{pr_info['number']}")
                    merged_branches.append(branch)
                else:
                    click.echo(f"❌ Failed to merge PR #{pr_info['number']}", err=True)
                    if not click.confirm("Continue with remaining branches?"):
                        break
        else:
            # Direct git merge
            if merge_branch(branch):
                click.echo(f"✅ Merged {branch}")
                merged_branches.append(branch)
            else:
                click.echo(f"❌ Failed to merge {branch}", err=True)
                if not click.confirm("Continue with remaining branches?"):
                    break

    # Clean up merged branches
    if delete_branches and merged_branches:
        if click.confirm(
            f"\nDelete {len(merged_branches)} merged branch(es) locally and remotely?"
        ):
            click.echo("\nCleaning up merged branches...")
            for branch in merged_branches:
                remove_from_stack(branch)
                # Delete local branch
                if run_git_command(["branch", "-d", branch], check=False):
                    click.echo(f"🗑️  Deleted local branch {branch}")
                # Delete remote branch
                if run_git_command(["push", "origin", "--delete", branch], check=False):
                    click.echo(f"🗑️  Deleted remote branch {branch}")
                else:
                    click.echo(
                        f"⚠️  Could not delete remote branch {branch} "
                        "(may already be deleted)"
                    )
        else:
            click.echo("Skipping branch deletion")

    click.echo(f"\n✅ Successfully merged {len(merged_branches)} branch(es)")

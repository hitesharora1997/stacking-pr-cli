"""Stack management utilities."""

from .config import load_config, save_config


def get_stack_info():
    """Get information about all branches in the stack."""
    config = load_config()
    return config.get("stack", {})


def add_to_stack(branch_name, base_branch):
    """Add a branch to the stack tracking."""
    config = load_config()
    if "stack" not in config:
        config["stack"] = {}

    config["stack"][branch_name] = {
        "base": base_branch,
        "pr_number": None,
        "created_at": None,  # TODO: Add timestamp
    }

    return save_config(config)


def remove_from_stack(branch_name):
    """Remove a branch from stack tracking."""
    config = load_config()
    if "stack" in config and branch_name in config["stack"]:
        del config["stack"][branch_name]
        return save_config(config)
    return False


def update_stack_info(branch_name, **kwargs):
    """Update information for a branch in the stack."""
    config = load_config()
    if "stack" in config and branch_name in config["stack"]:
        config["stack"][branch_name].update(kwargs)
        return save_config(config)
    return False


def get_stack_order():
    """Get branches in dependency order (base branches first)."""
    stack_info = get_stack_info()
    if not stack_info:
        return []

    # Build dependency graph
    dependencies = {}
    for branch, info in stack_info.items():
        dependencies[branch] = info["base"]

    # Topological sort
    ordered = []
    visited = set()

    def visit(branch):
        if branch in visited or branch not in dependencies:
            return
        visited.add(branch)
        base = dependencies[branch]
        if base in dependencies:
            visit(base)
        ordered.append(branch)

    for branch in dependencies:
        visit(branch)

    return ordered


def get_stack_tree(stack_info=None):
    """Generate a tree representation of the stack."""
    if stack_info is None:
        stack_info = get_stack_info()

    if not stack_info:
        return []

    # Build parent-to-children mapping
    children = {}
    roots = []

    for branch, info in stack_info.items():
        base = info["base"]
        if base not in stack_info:
            roots.append(branch)
        else:
            if base not in children:
                children[base] = []
            children[base].append(branch)

    # Generate tree lines
    lines = []

    def add_branch(branch, prefix="", is_last=True):
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{branch}")

        if branch in children:
            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(children[branch]):
                is_last_child = i == len(children[branch]) - 1
                add_branch(child, child_prefix, is_last_child)

    # Add base branches first
    base_branch = get_stack_info().get("settings", {}).get("base_branch", "main")
    lines.append(f"{base_branch} (base)")

    # Add root branches
    for i, root in enumerate(roots):
        is_last = i == len(roots) - 1
        add_branch(root, "", is_last)

    return lines


def get_branch_descendants(branch_name):
    """Get all branches that depend on the given branch."""
    stack_info = get_stack_info()
    descendants = []

    for other_branch, info in stack_info.items():
        if info["base"] == branch_name:
            descendants.append(other_branch)
            descendants.extend(get_branch_descendants(other_branch))

    return descendants

# stacking-pr

[![PyPI version](https://badge.fury.io/py/stacking-pr.svg)](https://badge.fury.io/py/stacking-pr)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A developer tool for managing clean commit history and modular PRs through a stacked workflow.

## Overview

`stacking-pr` helps developers maintain a clean git history by managing stacked (dependent) pull requests. This approach allows you to break down large features into smaller, focused, and easily reviewable changes while maintaining their dependencies.

## Features

- 🏗️ **Stacked Branches**: Create dependent branches that build on each other
- 🔄 **Smart Push**: Push entire stacks with proper dependency order
- 📝 **PR Management**: Automatically create and update pull requests using GitHub CLI
- 🎯 **Clean Merges**: Merge stacks in the correct order to maintain history
- 📊 **Visual Status**: See your entire stack structure at a glance
- 🔧 **Git Integration**: Works seamlessly with your existing git workflow

## How It Works

`stacking-pr` tracks your branch dependencies in a local `.stacking-pr.yml` file:

1. **Each branch knows its parent**: When you create a branch, it records what it's based on
2. **Commands respect hierarchy**: Operations happen in dependency order automatically
3. **Git stays in control**: We only run standard Git commands you could run manually
4. **PR descriptions are smart**: Automatically includes dependency information

Under the hood, `stacking-pr` runs standard Git commands:
- `git checkout -b` for branch creation  
- `git push --force-with-lease` for safe force pushes
- `gh pr create` for PR management

Your Git history remains clean and linear, just as if you managed it manually.

## Installation

### From PyPI

```bash
pip install stacking-pr
```

### From Source

```bash
git clone https://github.com/hitesharora1997/stacking-pr.git
cd stacking-pr
pip install -e .
```

### Prerequisites

- Python 3.9+
- Git
- GitHub CLI (`gh`) - optional but recommended for PR management

## Quick Start

1. **Initialize your repository**:
   ```bash
   stacking-pr init
   ```

2. **Create a new branch in your stack**:
   ```bash
   stacking-pr create feature/api-base
   ```

3. **Create dependent branches**:
   ```bash
   stacking-pr create feature/api-endpoints
   stacking-pr create feature/api-tests
   ```

4. **Check your stack status**:
   ```bash
   stacking-pr status
   ```

5. **Push your stack and create PRs**:
   ```bash
   stacking-pr push --all --create-prs
   ```

## Getting Started Tutorial

This tutorial walks you through using `stacking-pr` to implement a user authentication feature as a series of stacked pull requests.

### Scenario
You're adding authentication to your application. Instead of one massive PR, you'll create:
1. Base authentication interfaces and types
2. JWT token implementation
3. User login endpoints
4. Tests and documentation

### Step 1: Setup

First, ensure you have the prerequisites:

```bash
# Check Git is installed
git --version

# Check GitHub CLI is installed (optional but recommended)
gh --version

# Install stacking-pr
pip install stacking-pr
```

Navigate to your project and initialize stacking-pr:

```bash
cd my-project
stacking-pr init
```

This creates a `.stacking-pr.yml` file to track your stacks.

### Step 2: Create the Base Branch

Start with the foundation - authentication interfaces:

```bash
# Create the first branch in your stack
stacking-pr create feature/auth-interfaces

# You're automatically switched to the new branch
# Now add your base authentication code
mkdir -p src/auth
echo "# Authentication interfaces" > src/auth/__init__.py
```

Create your interface files:

```python
# src/auth/interfaces.py
from abc import ABC, abstractmethod
from typing import Optional, Dict

class AuthProvider(ABC):
    @abstractmethod
    def authenticate(self, credentials: Dict) -> Optional[str]:
        """Authenticate user and return token"""
        pass

class TokenValidator(ABC):
    @abstractmethod
    def validate(self, token: str) -> Optional[Dict]:
        """Validate token and return user info"""
        pass
```

Commit your changes:

```bash
git add src/auth/
git commit -m "feat: add authentication interfaces

- Add AuthProvider abstract base class
- Add TokenValidator abstract base class
- Set up auth module structure"
```

### Step 3: Stack the Implementation

Now create a branch for the JWT implementation that builds on top:

```bash
# This creates a new branch based on feature/auth-interfaces
stacking-pr create feature/jwt-implementation

# Add your JWT implementation
cat > src/auth/jwt_provider.py << 'EOF'
import jwt
from typing import Optional, Dict
from .interfaces import AuthProvider, TokenValidator

class JWTProvider(AuthProvider, TokenValidator):
    def __init__(self, secret: str):
        self.secret = secret
    
    def authenticate(self, credentials: Dict) -> Optional[str]:
        # Implementation here
        pass
    
    def validate(self, token: str) -> Optional[Dict]:
        # Implementation here
        pass
EOF
```

Commit the implementation:

```bash
git add src/auth/jwt_provider.py
git commit -m "feat: implement JWT authentication provider

- Add JWTProvider class implementing both interfaces
- Support token generation and validation
- Configure with secret key"
```

### Step 4: Add API Endpoints

Create another stacked branch for the API layer:

```bash
stacking-pr create feature/auth-endpoints

# Add login endpoint
mkdir -p src/api
cat > src/api/auth.py << 'EOF'
from fastapi import APIRouter, Depends
from src.auth.jwt_provider import JWTProvider

router = APIRouter(prefix="/auth")

@router.post("/login")
async def login(username: str, password: str):
    # Login implementation
    pass

@router.get("/verify")
async def verify(token: str):
    # Token verification
    pass
EOF
```

Commit:

```bash
git add src/api/
git commit -m "feat: add authentication API endpoints

- Add /auth/login endpoint
- Add /auth/verify endpoint
- Integrate with JWTProvider"
```

### Step 5: Check Your Stack Status

View your stack structure:

```bash
stacking-pr status --verbose
```

Output:
```
📚 Stack Overview:
==================================================
main (base)
└── feature/auth-interfaces
    └── feature/jwt-implementation
        └── feature/auth-endpoints

📊 Branch Details:
--------------------------------------------------

feature/auth-interfaces:
  Base: main
  Commits: 1

feature/jwt-implementation:
  Base: feature/auth-interfaces
  Commits: 1

feature/auth-endpoints:
  Base: feature/jwt-implementation
  Commits: 1

💡 Tips:
  • Create new branch: stacking-pr create <name>
  • Push stack: stacking-pr push
  • Merge stack: stacking-pr merge
```

### Step 6: Push and Create Pull Requests

Push your entire stack and create PRs:

```bash
# First, let's see what would happen (dry run)
stacking-pr push --all --create-prs --dry-run

# If everything looks good, push for real
stacking-pr push --all --create-prs
```

This will:
1. Push `feature/auth-interfaces` and create a PR against `main`
2. Push `feature/jwt-implementation` and create a PR against `feature/auth-interfaces`
3. Push `feature/auth-endpoints` and create a PR against `feature/jwt-implementation`

Each PR description will include:
- Commit messages from that branch
- Link to the base PR
- Clear dependency information

### Step 7: Handling Reviews and Updates

When reviewers request changes on the base PR:

```bash
# Switch to the branch that needs changes
git checkout feature/auth-interfaces

# Make the requested changes
echo "# Updated based on review" >> src/auth/interfaces.py
git add src/auth/interfaces.py
git commit -m "fix: address review comments on interfaces"

# Push just this branch
stacking-pr push

# The dependent branches may need rebasing
# stacking-pr will guide you through this
```

### Step 8: Adding Tests (New Branch in Stack)

Add tests as another layer:

```bash
# Make sure you're on the latest branch
git checkout feature/auth-endpoints

# Create test branch
stacking-pr create feature/auth-tests

# Add tests
mkdir -p tests/auth
cat > tests/auth/test_jwt.py << 'EOF'
def test_jwt_provider():
    # Test implementation
    pass
EOF

git add tests/
git commit -m "test: add authentication tests

- Test JWT token generation
- Test token validation
- Test API endpoints"

# Push the new branch
stacking-pr push --create-prs
```

### Step 9: Merging the Stack

Once all PRs are approved:

```bash
# Check PR status
stacking-pr status --prs

# Merge the entire stack in order
stacking-pr merge --cascade --delete-branches
```

This will:
1. Merge `feature/auth-interfaces` into `main`
2. Merge `feature/jwt-implementation` into `main`
3. Merge `feature/auth-endpoints` into `main`
4. Merge `feature/auth-tests` into `main`
5. Delete the feature branches (local and remote)

### Step 10: Stack Maintenance

If the main branch is updated while you're working:

```bash
# Update your local main
git checkout main
git pull

# Rebase your entire stack
stacking-pr rebase --all

# Force push all branches (safely with --force-with-lease)
stacking-pr push --all --force-with-lease
```

### Common Workflows

#### Split a Large Branch
```bash
# You realize feature/big-change is too large
git checkout feature/big-change
stacking-pr split --into 3
# Interactive prompt helps you organize commits
```

#### Insert a Branch in the Middle
```bash
# Need to add something between jwt-implementation and endpoints
git checkout feature/jwt-implementation
stacking-pr create feature/jwt-middleware
# Make changes
stacking-pr rebase --cascade  # Updates branches above
```

#### Emergency Fix
```bash
# Need to fix something in the base while stack is in review
stacking-pr fix feature/auth-interfaces
# Guides you through fixing and rebasing dependent branches
```

### Pro Tips

1. **Commit Messages Matter**: Your first commit message becomes the PR title
2. **Keep Branches Small**: 100-300 lines is ideal for reviews
3. **Use Draft PRs**: `stacking-pr push --draft` while work is in progress
4. **Visualize Before Push**: Always run `status --verbose` before pushing
5. **Name Branches Clearly**: Use a consistent naming scheme like `feature/component-aspect`

### What's Next?

- Read about [advanced workflows](docs/advanced.md)
- Learn about [team collaboration](docs/team.md)
- Configure [custom templates](docs/templates.md)
- Set up [CI/CD integration](docs/ci-cd.md)

## Commands

### `init`
Initialize a repository for stacked PR workflow.

```bash
stacking-pr init [--force]
```

Options:
- `--force, -f`: Force initialization even if already initialized

### `create`
Create a new branch in the stack.

```bash
stacking-pr create <branch-name> [OPTIONS]
```

Options:
- `--base, -b`: Base branch for the new branch (defaults to current branch)
- `--checkout/--no-checkout`: Whether to checkout the new branch after creation

### `status`
Show the status of the current stack.

```bash
stacking-pr status [OPTIONS]
```

Options:
- `--verbose, -v`: Show detailed information about each branch
- `--prs`: Show associated pull request information

Example output:
```
📚 Stack Overview:
==================================================
main (base)
└── feature/api-base
    ├── feature/api-endpoints
    └── feature/api-tests
```

### `push`
Push branches and optionally create/update pull requests.

```bash
stacking-pr push [OPTIONS]
```

Options:
- `--all, -a`: Push all branches in the stack
- `--create-prs`: Create pull requests for branches without them
- `--draft`: Create pull requests as drafts

### `rebase`
Rebase current branch or entire stack.

```bash
stacking-pr rebase [OPTIONS]
```

Options:
- `--stack, -s`: Rebase entire stack (otherwise just current branch)
- `--onto`: Branch to rebase onto (defaults to base branch from config)
- `--interactive, -i`: Interactive rebase (requires manual interaction)

### `merge`
Merge stacked branches in the correct order.

```bash
stacking-pr merge [OPTIONS]
```

Options:
- `--branch, -b`: Specific branch to merge (defaults to current branch)
- `--all`: Merge all branches in the stack
- `--delete-branches`: Delete branches after successful merge

## Workflow Example

Here's a typical workflow for implementing a new feature:

```bash
# Initialize the repo for stacked PRs
stacking-pr init

# Create base implementation
stacking-pr create feature/user-model
# ... make changes, commit ...

# Add API endpoints on top
stacking-pr create feature/user-api
# ... make changes, commit ...

# Add tests on top
stacking-pr create feature/user-tests
# ... make changes, commit ...

# View the stack
stacking-pr status --verbose

# Push everything and create PRs
stacking-pr push --all --create-prs

# After reviews, merge in order
stacking-pr merge --cascade --delete-branches
```

## Configuration

The tool creates a `.stacking-pr.yml` configuration file in your repository root. This file tracks:

- Stack structure and dependencies
- PR associations
- Default settings

Example configuration:
```yaml
version: "1.0"
stack:
  feature/api-base:
    base: main
    pr_number: 123
  feature/api-endpoints:
    base: feature/api-base
    pr_number: 124
settings:
  base_branch: main
  auto_create_prs: false
  delete_after_merge: false
```

## Best Practices

1. **Keep branches focused**: Each branch should represent one logical change
2. **Write descriptive commit messages**: They'll be used for PR descriptions
3. **Update regularly**: Rebase your stack when the base branch updates
4. **Review in order**: Review PRs from bottom to top of the stack
5. **Merge in order**: Always merge from the base up to maintain history

## Troubleshooting

### GitHub CLI not found
Install the GitHub CLI and authenticate:
```bash
# Install
brew install gh  # macOS
# or see: https://cli.github.com/

# Authenticate
gh auth login
```

### Conflicts during merge
1. Resolve conflicts in the bottom-most branch first
2. Rebase dependent branches after resolving
3. Push with `--force-with-lease`

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Created by Hitesh Arora

Inspired by tools like [git-branchless](https://github.com/arxanas/git-branchless) and GitHub's stacked PR workflow.
# Contributing to stacking-pr

Thank you for your interest in contributing to stacking-pr! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/hitesharora1997/stacking-pr.git
   cd stacking-pr
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   make setup
   ```

3. Make sure tests pass:
   ```bash
   make test
   ```

## Development Workflow

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and write tests

3. Format your code:
   ```bash
   make format
   ```

4. Run linting and tests:
   ```bash
   make lint
   make test-cov
   ```

5. Commit your changes with a descriptive message:
   ```bash
   git commit -m "feat: add support for X"
   ```

6. Push and create a pull request

## Code Style

- We use `black` for code formatting
- We use `isort` for import sorting
- We use `flake8` for linting
- All code must have type hints
- Write docstrings for all public functions and classes

## Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use pytest for all tests
- Mock external dependencies (git commands, gh CLI)

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `test`: Adding missing tests or correcting existing tests
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `chore`: Other changes that don't modify src or test files

### Examples
```
feat(cli): add support for interactive branch selection
fix(git): handle detached HEAD state correctly
docs: update README with new command options
```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Ensure all tests pass and coverage requirements are met
3. Update documentation for any new commands or options
4. Request review from maintainers

## Project Structure

```
stacking-pr/
├── src/
│   └── stacking_pr/
│       ├── __init__.py         # Package initialization
│       ├── cli.py              # Main CLI entry point
│       ├── version.py          # Version management
│       ├── commands/           # CLI command implementations
│       │   ├── init.py
│       │   ├── create.py
│       │   ├── status.py
│       │   ├── push.py
│       │   └── merge.py
│       └── utils/              # Utility modules
│           ├── git.py          # Git operations
│           ├── config.py       # Configuration management
│           ├── stack.py        # Stack tracking logic
│           └── github.py       # GitHub integration
├── tests/                      # Test suite
├── pyproject.toml             # Project configuration
├── Makefile                   # Development commands
├── README.md                  # Project documentation
└── CONTRIBUTING.md            # This file
```

## Adding New Commands

1. Create a new file in `src/stacking_pr/commands/`
2. Implement the command using Click decorators
3. Add the command to the CLI group in `cli.py`
4. Write tests for the new command
5. Update README with documentation

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include steps to reproduce for bugs
- Provide context and use cases for feature requests
- Include relevant system information (OS, Python version, git version)

## Questions?

Feel free to open an issue for any questions about contributing!
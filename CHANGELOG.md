# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-01-23

### Added
- Basic test suite with pytest for improved reliability
- Flake8 configuration and linting compliance
- Input validation for branch names to prevent security issues
- Error handling for git operations with custom exceptions
- Confirmation prompts for destructive operations
- GitHub CLI availability check during initialization
- `rebase` command for maintaining clean history

### Fixed
- CLI entry point configuration (now correctly points to `stacking_pr.cli:cli`)
- Security vulnerability in shell command execution (now uses proper argument lists)
- Incorrect PR base determination logic when pushing stacked branches
- Config file no longer automatically added to .gitignore (users choose whether to track it)

### Changed
- Improved error messages with better context
- Enhanced git state checking (detached HEAD detection)
- Better handling of edge cases in git operations

## [0.2.0] - 2025-01-22

### Added
- Enhanced CLI commands for stacked PR workflow
- Improved configuration management
- Better stack tracking functionality

## [0.1.0] - 2025-01-21

### Added
- Initial release of stacking-pr CLI tool
- Core commands: init, create, push, merge, status
- Stack-based branch management
- GitHub integration via gh CLI
- Configuration file support (.stacking-pr.yml)
- Basic git operations wrapper
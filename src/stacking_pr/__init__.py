"""
stacking-pr: A developer tool for managing clean commit history and modular PRs.

This package helps developers maintain a clean git workflow with stacked pull requests,
making it easier to create focused, reviewable changes.
"""

__version__ = "0.1.0"
__author__ = "Hitesh Arora"
__email__ = "hitesh.arora@example.com"

from .cli import cli

__all__ = ["cli"]

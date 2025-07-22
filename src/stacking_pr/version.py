"""Version information for stacking-pr."""

import importlib.metadata


def get_version():
    """Get the version of stacking-pr package."""
    try:
        return importlib.metadata.version("stacking-pr")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.0"  # Fallback version for development

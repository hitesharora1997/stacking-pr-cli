"""Configuration management utilities."""

from pathlib import Path

import yaml

DEFAULT_CONFIG = {
    "version": "1.0",
    "stack": {},
    "settings": {
        "base_branch": "main",
        "pr_template": None,
        "auto_create_prs": False,
        "delete_after_merge": False,
    },
}


def get_config_path():
    """Get the path to the configuration file."""
    return Path(".stacking-pr.yml")


def load_config():
    """Load configuration from file."""
    config_path = get_config_path()
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}
            # Merge with defaults to ensure all keys exist
            merged = DEFAULT_CONFIG.copy()
            merged.update(config)
            return merged
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file."""
    config_path = get_config_path()
    try:
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception:
        return False


def create_config_file(path=None):
    """Create a new configuration file with defaults."""
    if path is None:
        path = get_config_path()

    config = DEFAULT_CONFIG.copy()

    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    return True


def get_setting(key, default=None):
    """Get a setting value from configuration."""
    config = load_config()
    return config.get("settings", {}).get(key, default)


def set_setting(key, value):
    """Set a setting value in configuration."""
    config = load_config()
    if "settings" not in config:
        config["settings"] = {}
    config["settings"][key] = value
    return save_config(config)

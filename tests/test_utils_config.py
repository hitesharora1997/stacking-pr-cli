"""Tests for configuration utilities."""

import yaml

from stacking_pr.utils.config import (
    DEFAULT_CONFIG,
    get_config_path,
    load_config,
    save_config,
)


def test_default_config_structure():
    """Test that default config has expected structure."""
    assert "stack" in DEFAULT_CONFIG
    assert isinstance(DEFAULT_CONFIG["stack"], dict)
    assert "settings" in DEFAULT_CONFIG


def test_get_config_path():
    """Test config path returns expected filename."""
    config_path = get_config_path()
    assert config_path.name == ".stacking-pr.yml"


def test_load_config_returns_default(monkeypatch, tmp_path):
    """Test that load_config returns default config if file doesn't exist."""
    monkeypatch.chdir(tmp_path)

    config = load_config()

    assert config == DEFAULT_CONFIG


def test_load_config_reads_existing(monkeypatch, tmp_path):
    """Test that load_config reads existing config."""
    monkeypatch.chdir(tmp_path)

    # Create a custom config
    custom_config = {
        "version": "1.0",
        "stack": {
            "feature-1": {"branches": ["feature-1a", "feature-1b"], "base": "main"}
        },
        "settings": {"base_branch": "main"},
    }

    config_file = tmp_path / ".stacking-pr.yml"
    with open(config_file, "w") as f:
        yaml.dump(custom_config, f)

    loaded_config = load_config()
    assert loaded_config == custom_config


def test_save_config(monkeypatch, tmp_path):
    """Test saving configuration."""
    monkeypatch.chdir(tmp_path)

    config = {
        "version": "1.0",
        "stack": {"test-stack": {"branches": ["branch1", "branch2"], "base": "main"}},
    }

    save_config(config)

    # Read the saved file
    config_file = tmp_path / ".stacking-pr.yml"
    assert config_file.exists()

    with open(config_file) as f:
        saved_config = yaml.safe_load(f)

    assert saved_config == config

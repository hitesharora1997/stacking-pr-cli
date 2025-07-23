"""Tests for stack management utilities."""

from unittest.mock import patch

from stacking_pr.utils.stack import (
    add_to_stack,
    get_stack_info,
    remove_from_stack,
    update_stack_info,
)


@patch("stacking_pr.utils.stack.load_config")
def test_get_stack_info_empty(mock_load_config):
    """Test get_stack_info with empty config."""
    mock_load_config.return_value = {"stack": {}}

    info = get_stack_info()
    assert info == {}


@patch("stacking_pr.utils.stack.load_config")
def test_get_stack_info_with_branches(mock_load_config):
    """Test get_stack_info with existing branches."""
    stack_data = {
        "feature-1": {
            "base": "main",
            "pr_number": None,
        },
        "feature-2": {
            "base": "feature-1",
            "pr_number": 123,
        },
    }
    mock_load_config.return_value = {"stack": stack_data}

    info = get_stack_info()
    assert info == stack_data


@patch("stacking_pr.utils.stack.save_config")
@patch("stacking_pr.utils.stack.load_config")
def test_add_to_stack(mock_load_config, mock_save_config):
    """Test adding branch to stack."""
    mock_load_config.return_value = {"stack": {}}
    mock_save_config.return_value = True

    result = add_to_stack("feature-1", "main")

    assert result is True
    expected_config = {
        "stack": {
            "feature-1": {
                "base": "main",
                "pr_number": None,
                "created_at": None,
            }
        }
    }
    mock_save_config.assert_called_once_with(expected_config)


@patch("stacking_pr.utils.stack.save_config")
@patch("stacking_pr.utils.stack.load_config")
def test_update_stack_info(mock_load_config, mock_save_config):
    """Test updating stack info for a branch."""
    mock_load_config.return_value = {
        "stack": {
            "feature-1": {
                "base": "main",
                "pr_number": None,
            }
        }
    }
    mock_save_config.return_value = True

    result = update_stack_info("feature-1", pr_number=123)

    assert result is True
    expected_config = {
        "stack": {
            "feature-1": {
                "base": "main",
                "pr_number": 123,
            }
        }
    }
    mock_save_config.assert_called_once_with(expected_config)


@patch("stacking_pr.utils.stack.save_config")
@patch("stacking_pr.utils.stack.load_config")
def test_remove_from_stack(mock_load_config, mock_save_config):
    """Test removing branch from stack."""
    mock_load_config.return_value = {
        "stack": {
            "feature-1": {"base": "main"},
            "feature-2": {"base": "feature-1"},
        }
    }
    mock_save_config.return_value = True

    result = remove_from_stack("feature-1")

    assert result is True
    expected_config = {
        "stack": {
            "feature-2": {"base": "feature-1"},
        }
    }
    mock_save_config.assert_called_once_with(expected_config)


@patch("stacking_pr.utils.stack.save_config")
@patch("stacking_pr.utils.stack.load_config")
def test_remove_from_stack_not_found(mock_load_config, mock_save_config):
    """Test removing non-existent branch returns False."""
    mock_load_config.return_value = {
        "stack": {
            "feature-1": {"base": "main"},
        }
    }

    result = remove_from_stack("nonexistent")

    assert result is False
    mock_save_config.assert_not_called()

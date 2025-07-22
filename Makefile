.PHONY: help setup install dev test test-cov lint format clean

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup:  ## Create virtual environment and install dependencies
	python -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -e ".[dev,test]"

install:  ## Install the package in development mode
	pip install -e .

dev:  ## Install development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=stacking_pr --cov-report=html --cov-report=term

lint:  ## Run linting checks
	flake8 src/stacking_pr
	black --check src/stacking_pr
	isort --check-only src/stacking_pr

format:  ## Format code with black and isort
	black src/stacking_pr
	isort src/stacking_pr

clean:  ## Clean up temporary files and directories
	rm -rf venv/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
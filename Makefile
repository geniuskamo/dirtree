.PHONY: install clean lint test build develop dev-install setup

# Development installation
develop:
	pip install -e .

# Install development dependencies
dev-install:
	pip install -r requirements-dev.txt

# Development setup (combine develop and dev-install)
setup: develop dev-install

# Production installation
install:
	pip install .

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '__pycache__' -delete
	find . -name '.pytest_cache' -delete

# Run linting
lint:
	flake8 src/
	black --check src/
	isort --check-only src/

# Format code
format:
	black src/
	isort src/

# Run tests
test:
	python -m pytest tests/

# Build distribution
build: clean
	python setup.py sdist bdist_wheel

# Build binary
binary:
	python build_binary.py

# Full distribution (includes both package and binary)
dist: clean build binary

# Default target
all: clean lint test dist

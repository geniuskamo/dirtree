# Directory Tree Generator

A Python tool that generates tree-like representations of directory structures, supporting both console and markdown outputs.

## Project Structure
```
dirtree/
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── formatters.py
│   └── tree_generator.py
│   └── README.md
└── setup.py
```

## Features
- Console and Markdown output formats
- Customizable formatting through formatter classes
- Permission error handling
- Sorted directory listings
- Command-line interface

## Installation

### From Source
```bash
pip install .
```

### Binary Distribution
Pre-built binaries are available for Windows, macOS, and Linux platforms. Download the appropriate binary for your system from the releases page.

To build the binary yourself:
```bash
# Install development dependencies first
pip install -r requirements-dev.txt

# Build binary
make binary

# Binary will be available in dist/<platform>/
```

### For Developers
```bash
git clone https://github.com/yourusername/dirtree.git
cd dirtree
make setup  # Installs package in editable mode and dev dependencies
```

## Usage

```bash
# Basic usage - current directory
dirtree

# Specify directory
dirtree /path/to/directory

# Generate markdown
dirtree /path/to/directory --format markdown

# Save to file
dirtree /path/to/directory --format markdown -o tree.md
```

## Example Outputs

### Console Output
```
.
├── src
│   ├── __init__.py
│   ├── cli.py
│   ├── formatters.py
│   └── tree_generator.py
└── setup.py
```

### Markdown Output
The markdown output includes proper HTML entities for spacing and renders well in markdown documents:
```
.
├── src
&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py
&nbsp;&nbsp;&nbsp;&nbsp;├── cli.py
&nbsp;&nbsp;&nbsp;&nbsp;├── formatters.py
&nbsp;&nbsp;&nbsp;&nbsp;└── tree_generator.py
└── setup.py
```

## Development

### Project Structure
```
dirtree/
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── formatters.py
│   └── tree_generator.py
├── requirements-dev.txt
├── Makefile
└── setup.py
```

### Available Make Commands
- `make setup` - Set up development environment
- `make lint` - Run code linting (flake8, black, isort)
- `make format` - Format code using black and isort
- `make test` - Run tests
- `make clean` - Clean build artifacts
- `make build` - Build distribution packages
- `make binary` - Build standalone executable

### Development Dependencies
Development dependencies are managed in `requirements-dev.txt` and include:
- pytest - Testing framework
- flake8 - Code linting
- black - Code formatting
- isort - Import sorting
- build/wheel - Package building

### Building Distributions
- `make build` - Build Python package distribution
- `make binary` - Build standalone executable
- `make dist` - Build both package and binary distributions

### Binary Distribution
The project uses PyInstaller to create standalone executables:
- Binaries are created for the current platform
- Output is placed in `dist/<platform>/`
- Single file executables include all dependencies

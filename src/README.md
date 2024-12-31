# Directory Tree Generator

A Python tool that generates tree-like representations of directory structures, supporting both console and markdown outputs.

## Project Structure
```
dirtree/
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── formatters.py
│   ├── tree_generator.py
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

### For Users
```bash
pip install .
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

### Development Dependencies
Development dependencies are managed in `requirements-dev.txt` and include:
- pytest - Testing framework
- flake8 - Code linting
- black - Code formatting
- isort - Import sorting
- build/wheel - Package building

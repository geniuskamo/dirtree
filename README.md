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
- Console, Markdown, and JSON output formats
- Customizable formatting through formatter classes
- Permission error handling
- Sorted directory listings
- Command-line interface
- Exclude specific directories from the output

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
git clone https://github.com/geniuskamo/dirtree.git
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
dirtree /path/to/directory --format markdown -f md

# Save to file
dirtree /path/to/directory --format markdown -o tree.md

# Exclude specific directories
dirtree /path/to/directory --exclude dir1,dir2 -e dir1,dir2

# Generate JSON
dirtree /path/to/directory --format json

# Disable progress bar
dirtree /path/to/directory --no-progress
```

## Configuration

The tool supports configuration files in YAML format. Create a file named `dirtree.yml`:

```yaml
# Default output format
format: console

# Directories to exclude
exclude:
  - node_modules
  - .git
  - __pycache__

# Enable verbose logging
verbose: false

# Output file path
output: tree.txt

# Log file location
log_file: dirtree.log

# Disable progress bar
no_progress: false
```

Use the configuration file:
```bash
dirtree /path/to/directory -c dirtree.yml
```

Command line arguments override configuration file settings.

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
    ├── __init__.py
    ├── cli.py
    ├── formatters.py
    └── tree_generator.py
└── setup.py
```

### JSON Output
The JSON output provides a structured representation of the directory:
```json
{
    "src": {
        "__init__.py": null,
        "cli.py": null,
        "formatters.py": null,
        "tree_generator.py": null
    },
    "setup.py": null
}
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

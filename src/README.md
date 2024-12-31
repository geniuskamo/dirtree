# Directory Tree Generator

A simple command-line tool to generate a tree-like representation of directory structures.

## Installation

```bash
pip install .
```

## Usage

```bash
# Generate tree for current directory in console
dirtree

# Generate tree for specific directory in console
dirtree /path/to/directory

# Generate tree in Markdown format and save to file
dirtree /path/to/directory --format markdown -o output.md

# Generate tree in Markdown format and display in console
dirtree /path/to/directory --format markdown
```

## Example Outputs

### Console Output
```
├── README.md
├── setup.py
├── dirtree
│   ├── __init__.py
│   ├── cli.py
│   └── tree_generator.py
```

### Markdown Output
The markdown output will be similar but formatted for better rendering in markdown documents.

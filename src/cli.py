import argparse
from src.tree_generator import DirectoryTree  # Update import
from src.formatters import ConsoleFormatter, MarkdownFormatter  # Update import


def main():
    parser = argparse.ArgumentParser(
        description="Generate a tree-like structure of directory contents"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to generate tree from (default: current directory)"
    )
    parser.add_argument(
        "--format",
        choices=["console", "markdown"],
        default="console",
        help="Output format (default: console)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file (only used with markdown format)"
    )
    parser.add_argument(
        "--exclude",
        help="Comma-separated list of directories to exclude"
    )

    args = parser.parse_args()

    exclude = args.exclude.split(",") if args.exclude else []
    formatter = MarkdownFormatter() if args.format == "markdown" else ConsoleFormatter()
    tree = DirectoryTree(args.directory, formatter, exclude)
    output = "\n".join(tree.generate())

    if args.format == "markdown" and args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()

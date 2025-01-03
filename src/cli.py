import argparse
import logging
import sys
from pathlib import Path
from src.tree_generator import DirectoryTree  # Update import
from src.formatters import ConsoleFormatter, MarkdownFormatter, JSONFormatter  # Update import

def setup_logging(verbose: bool):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # File handler for all levels
    log_file = Path('dirtree.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    if verbose:
        # Console handler for debug and above
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    logger = logging.getLogger(__name__)
    logger.debug("Logging setup completed")
    logger.debug(f"Log file location: {log_file.absolute()}")
    if verbose:
        logger.info("Verbose logging enabled")

def main():
    logger = logging.getLogger(__name__)
    
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
        "-f", "--format",
        choices=["console", "markdown", "json"],
        default="console",
        help="Output format (default: console)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file (only used with markdown or json format)"
    )
    parser.add_argument(
        "-e", "--exclude",
        help="Comma-separated list of directories to exclude"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging to console"
    )

    args = parser.parse_args()
    
    try:
        setup_logging(args.verbose)
        logger.debug("Command line arguments parsed successfully")
        logger.debug(f"Directory: {args.directory}")
        logger.debug(f"Format: {args.format}")
        logger.debug(f"Output: {args.output}")
        logger.debug(f"Exclude: {args.exclude}")

        exclude = args.exclude.split(",") if args.exclude else []
        formatter = {
            "console": ConsoleFormatter,
            "markdown": MarkdownFormatter,
            "json": JSONFormatter
        }[args.format]()
        
        logger.info(f"Starting tree generation for directory: {args.directory}")
        tree = DirectoryTree(args.directory, formatter, exclude)
        output = "\n".join(tree.generate())

        if args.output:
            logger.info(f"Writing output to file: {args.output}")
            try:
                with open(args.output, "w") as f:
                    f.write(output)
                logger.info("File written successfully")
            except IOError as e:
                logger.error(f"Failed to write to output file: {e}")
                sys.exit(1)
        else:
            print(output)
        
        logger.info("Tree generation completed successfully")
        
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

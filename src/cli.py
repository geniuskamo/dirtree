import argparse
import logging
import sys
from pathlib import Path
from src.tree_generator import DirectoryTree  # Update import
from src.formatters import ConsoleFormatter, MarkdownFormatter, JSONFormatter  # Update import
from src.config import load_config
from tqdm import tqdm

def setup_logging(verbose: bool, log_file: str = 'dirtree.log'):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # File handler for all levels
    log_file = Path(log_file)
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
        help="Output format (default: console)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path"
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
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable progress bar"
    )

    args = parser.parse_args()
    
    try:
        # Load config file first
        config = load_config(args.config)
        
        # Override config with command line arguments
        if args.format:
            config['format'] = args.format
        if args.output:
            config['output'] = args.output
        if args.exclude:
            config['exclude'] = args.exclude.split(',')
        if args.verbose:
            config['verbose'] = True

        if args.no_progress:
            tqdm.disable = True

        setup_logging(config['verbose'], config['log_file'])
        logger = logging.getLogger(__name__)
        
        logger.debug("Configuration loaded successfully")
        logger.debug(f"Active configuration: {config}")

        formatter = {
            "console": ConsoleFormatter,
            "markdown": MarkdownFormatter,
            "json": JSONFormatter
        }[config['format']]()
        
        logger.info(f"Starting tree generation for directory: {args.directory}")
        tree = DirectoryTree(args.directory, formatter, config['exclude'])
        output = "\n".join(tree.generate())

        if config['output']:
            logger.info(f"Writing output to file: {config['output']}")
            try:
                with open(config['output'], "w") as f:
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

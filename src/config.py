import yaml
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "format": "console",
    "exclude": [],
    "verbose": False,
    "output": None,
    "log_file": "dirtree.log"
}

def load_config(config_file: str = None) -> Dict[str, Any]:
    """Load configuration from file and merge with defaults."""
    config = DEFAULT_CONFIG.copy()
    
    if config_file and os.path.exists(config_file):
        try:
            logger.debug(f"Loading config from {config_file}")
            with open(config_file, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    config.update(user_config)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
    
    return config

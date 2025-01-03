import pytest
import yaml
import os
from src.config import load_config, DEFAULT_CONFIG

@pytest.fixture
def config_file(tmp_path):
    config = {
        "format": "markdown",
        "exclude": ["node_modules", ".git"],
        "verbose": True,
        "output": "test.md",
        "log_file": "test.log"
    }
    config_path = tmp_path / "test_config.yml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    return str(config_path)

def test_load_default_config():
    config = load_config()
    assert config == DEFAULT_CONFIG

def test_load_config_file(config_file):
    config = load_config(config_file)
    assert config["format"] == "markdown"
    assert "node_modules" in config["exclude"]
    assert config["verbose"] is True
    assert config["output"] == "test.md"

def test_load_invalid_config():
    config = load_config("nonexistent.yml")
    assert config == DEFAULT_CONFIG

def test_load_malformed_config(tmp_path):
    bad_config = tmp_path / "bad_config.yml"
    bad_config.write_text("invalid: yaml: content")
    config = load_config(str(bad_config))
    assert config == DEFAULT_CONFIG

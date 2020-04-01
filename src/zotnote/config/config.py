# -*- coding: utf-8 -*-
"""A module that manages all things config."""

import click
from tomlkit import dumps
from tomlkit import loads
from zotnote import ROOT
from zotnote import config_dir


class Configuration:
    """A helper class to manage configuration."""

    exmpl_cfg_file = ROOT / "config/config.toml.example"
    config_file = config_dir / "config.toml"

    @classmethod
    def validate(cls):
        """Validate local configuration & create missing folders and files."""
        # Make sure the config file is placed in XDG_CONFIG_HOME
        if not cls.config_file.exists():
            click.echo("Missing configuration file. Proceeding to create a new one.")
            cls.__create_dir(config_dir)
            cls.create_config()

    @classmethod
    def load_config(cls):
        """Load configuration file."""
        return loads(cls.config_file.read_text())

    @classmethod
    def create_config(cls):
        """Create new configuration."""
        if cls.config_file.exists():
            ow = click.confirm(
                "Do you really want to create a new config? "
                "This will overwrite your existing config."
            )
            if ow:
                config = cls.__new_config()
        else:
            config = cls.__new_config()
        cls.config_file.write_text(dumps(config))

    @classmethod
    def update_config(cls, key, value):
        """Update a single value in the config."""
        config = loads(cls.config_file.read_text())
        config[key] = value
        cls.config_file.write_text(dumps(config))

    @classmethod
    def __new_config(cls):
        """Load example configuration and populate interactively."""
        exmpl_config = loads(cls.exmpl_cfg_file.read_text())
        config = exmpl_config

        config["name"] = click.prompt("Enter your name")
        config["email"] = click.prompt("Enter your email")

        config["editor"] = click.prompt("The command to execute your editor of choice")

        config["notes"] = click.prompt("Enter location for your notes")
        return config

    @staticmethod
    def __create_dir(dir):
        """Create directory if missing."""
        if not dir.exists():
            dir.mkdir(parents=True)

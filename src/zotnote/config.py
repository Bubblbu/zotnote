# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

import click
from tomlkit import dumps, loads

from zotnote import config_dir, data_dir, base_dir


class Configuration:
    """A helper class to manage configurations"""
    example_config = base_dir / "config.toml.example"
    config_file = config_dir / "config.toml"

    pkg_templates_dir = base_dir / "notes/templates"
    templates_dir = data_dir / "templates"


    @classmethod
    def validate(cls):
        """Validate local configuration & create missing folders and files."""
        if not cls.config_file.exists():
            click.echo("Missing configuration file. Proceeding to create a new one.")
            cls.__create_dir(config_dir)
            cls.create_config()

        if not cls.templates_dir.exists():
            click.echo("App data missing. Proceeding to copy templates.")
            cls.__create_dir(cls.templates_dir)
            cls.__copy_templates()

        pkg_templates = len(list(cls.pkg_templates_dir.glob("*.j2")))
        lc_templates = len(list(cls.templates_dir.glob("*.j2")))

        if lc_templates < pkg_templates:
            click.echo("Template files are missing in app data. Copying...")
            cls.__copy_templates()

    @classmethod
    def load_config(cls):
        """Load configuration file."""

        return loads(cls.config_file.read_text())

    @classmethod
    def create_config(cls):
        """Creates new configuration."""
        if cls.config_file.exists():
            ow = click.confirm("Do you really want to create a new config? "
                               "This will overwrite your existing config.")
            if ow:
                config = cls.__new_config()
        else:
            config = cls.__new_config()
        cls.config_file.write_text(dumps(config))

    @classmethod
    def update_config(cls, key, value):
        config = loads(cls.config_file.read_text())
        config[key] = value
        cls.config_file.write_text(dumps(config))

    @staticmethod
    def __new_config():
        """Load example configuration and populate interactively"""
        exmpl_file = base_dir / "config.toml.example"
        exmpl_config = loads(exmpl_file.read_text())
        config = exmpl_config

        config['name'] = click.prompt("Enter your name")
        config['email'] = click.prompt("Enter your email")

        config["editor"] = click.prompt("The command to execute your editor of choice")

        config["zotero"] = click.prompt("Enter path to your Zotero directory")
        config["notes"] = click.prompt("Enter location for your notes")
        return config

    @staticmethod
    def __create_dir(dir):
        """Create directory if missing."""
        if not dir.exists():
            dir.mkdir(parents=True)

    @classmethod
    def __copy_templates(cls):
        """Copy template files to the data directory."""
        for f in cls.pkg_templates_dir.glob("*.j2"):
            shutil.copyfile(f, cls.templates_dir / f.name)

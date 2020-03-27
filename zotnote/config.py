# -*- coding: utf-8 -*-
import shutil
from distutils.util import strtobool
from pathlib import Path

import click
from tomlkit import comment, document, dumps, loads, nl

from zotnote import config_dir, data_dir


class Configuration:
    """
    Factory class to setup the project
    """
    config_file = config_dir / "config.toml"
    templates_dir = data_dir / "templates"

    def __init__(self):
        # check if config file exists
        if not self.config_file.exists():
            click.echo("Missing configuration file. Proceeding to create a new one.")
            self.create_config_dir()
            self.create_config()

        if not self.templates_dir.exists():
            click.echo("App data missing. Proceeding to copy templates.")
            self.create_datadir()
            self.copy_templates()

    @classmethod
    def load_config(cls):
        """
        Load configuration
        """

        return loads(cls.config_file.read_text())

    @classmethod
    def create_config_dir(cls):
        if not config_dir.exists():
            config_dir.mkdir(parents=True)

    @classmethod
    def create_config(cls):
        """
        Loads or creates new configuration.
        """
        if cls.config_file.exists():
            ow = click.prompt(
                "A configuration already exists. Do you want to create a new one? [y/n]")
            if strtobool(ow):
                config = cls.__new_config()
                cls.config_file.write_text(dumps(config))
            else:
                config = loads(cls.config_file.read_text())
        else:
            config = cls.__new_config()
            cls.config_file.write_text(dumps(config))
        return config

    @classmethod
    def create_datadir(cls):
        """
        Creates data directory for zotnote and copies all templates to the folder
        """
        if not cls.templates_dir.exists():
            cls.templates_dir.mkdir(parents=True)

    @classmethod
    def copy_templates(cls):
        template_dir_dist = Path(".").parent / "templates"
        for f in template_dir_dist.glob("*.j2"):
            shutil.copyfile(f, cls.templates_dir / f.name)

    @staticmethod
    def locate(cwd):
        candidates = [Path(cwd)]
        candidates.extend(Path(cwd).parents)

        for path in candidates:
            poetry_file = path / "pyproject.toml"

            if poetry_file.exists():
                return poetry_file

        else:
            raise RuntimeError(
                "Poetry could not find a pyproject.toml file in {} or its parents".format(
                    cwd
                )
            )

    @staticmethod
    def __new_config():
        config = document()
        config.add(comment("Profile"))
        config.add("name", click.prompt("Enter your name"))
        config.add(nl())

        config.add(comment("Settings"))
        config.add(nl())

        config.add(comment("Directories"))
        config.add("zotero", click.prompt("Path to your Zotero installation"))
        config.add("notes", click.prompt("Where do you want to store your notes"))

        return config

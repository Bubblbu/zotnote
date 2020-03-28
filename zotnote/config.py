# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

import click
from tomlkit import comment, document, dumps, loads, nl

from zotnote import config_dir, data_dir, project_dir


class Configuration:
    """
    Factory class to setup the project
    """
    config_file = config_dir / "config.toml"
    templates_dir = data_dir / "templates"
    pkg_templates_dir = project_dir / "templates"

    @classmethod
    def check_files(cls):
        if not cls.config_file.exists():
            click.echo("Missing configuration file. Proceeding to create a new one.")
            cls.create_config_dir()
            cls.create_config()

        if not cls.templates_dir.exists():
            click.echo("App data missing. Proceeding to copy templates.")
            cls.create_datadir()
            cls.copy_templates()

        pkg_templates = len(list(cls.pkg_templates_dir.glob("*.j2")))
        lc_templates = len(list(cls.templates_dir.glob("*.j2")))
        if lc_templates < pkg_templates:
            click.echo("Template files are missing in app data. Copying...")
            cls.copy_templates()

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
            ow = click.confirm("A configuration already exists. "
                               "Do you want to create a new one?")
            if ow:
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
        for f in cls.pkg_templates_dir.glob("*.j2"):
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
        config.add("email", click.prompt("Enter your email"))
        config.add(nl())

        config.add(comment("Settings"))
        config.add("editor", click.prompt(
            "The command to execute your editor of choice."
            "(e.g., gedit, code, or vi/m)"))
        config.add(nl())

        config.add(comment("Directories"))
        config.add("zotero", click.prompt(
            "Enter path to your Zotero directory (usually \"~/Zotero\""))
        config.add("notes", click.prompt(
            "Enter location to your notes (e.g., \"~/Documents/notes/\""))

        return config

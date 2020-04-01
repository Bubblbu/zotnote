# -*- coding: utf-8 -*-
"""This module is the main entry point for the app."""
from .cli import add
from .cli import cli
from .cli import config
from .cli import edit
from .cli import remove
from .cli import templates
from .config.config import Configuration


def main():
    """Load config and launch CLI."""
    # Check if all configuration files are in place
    Configuration.validate()

    # Add commands to CLI
    cli.add_command(add)
    cli.add_command(config)
    cli.add_command(edit)
    cli.add_command(remove)
    cli.add_command(templates)
    # cli.add_command(report)

    # Launch CLI
    cli(prog_name="zotnote")

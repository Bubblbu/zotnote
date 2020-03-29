#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from zotnote.cli import cli
from zotnote.cli import config, add, report, edit, remove
from .config import Configuration


def main():
    # Check if all configuration files are in place
    Configuration.validate()

    # Add commands to CLI
    cli.add_command(add)
    cli.add_command(config)
    cli.add_command(edit)
    cli.add_command(remove)
    # cli.add_command(report)

    # Launch CLI
    cli(prog_name='zotnote')


if __name__ == "__main__":
    main()

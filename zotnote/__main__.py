#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from zotnote.cli import cli, config, new, update_templates, report, edit, remove
from .config import Configuration


def main():
    Configuration().check_files()

    cli.add_command(new)
    cli.add_command(report)
    cli.add_command(config)
    cli.add_command(update_templates)
    cli.add_command(edit)
    cli.add_command(remove)
    cli(prog_name='zotnote')


if __name__ == "__main__":
    main()

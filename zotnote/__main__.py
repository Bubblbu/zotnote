#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from zotnote.cli import cli, config, new, report

if __name__ == "__main__":
    cli.add_command(new)
    cli.add_command(report)
    cli.add_command(config)
    cli()

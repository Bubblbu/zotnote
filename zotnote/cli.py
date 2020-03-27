#!/usr/bin/env python
# # -*- coding: utf-8 -*-
import sys
from distutils.util import strtobool

import click

from zotnote.templates import MarkdownTemplate
from zotnote.zotero import BetterBibtexException, ZoteroDBConnector

from zotnote import AUTHOR, notes_dir, zotero_dir, templates_dir


@click.command()
@click.argument('citekey')
def new(citekey):
    """Create reading note for CITEKEY in your Zotero library."""
    # Retrieve Information from Zotero
    zotero = ZoteroDBConnector(citekey)

    try:
        zotero.citekey_lookup()
    except BetterBibtexException as e:
        print(e)
        sys.exit()

    fieldValues = zotero.get_field_values()

    print(f"Found entry for {citekey}:\n\n"
          f"\tTitle: {fieldValues['title']}\n"
          f"\tCreator: {fieldValues['creator']}\n"
          f"\tDate: {fieldValues['date']}\n")

    choice = click.prompt("Continue? [y/n]")
    if strtobool(choice):
        pass
    else:
        print("Cya!")
        sys.exit()

    # Fill template
    md = MarkdownTemplate(citekey, fieldValues)

    # Write output file
    outfile = notes_dir / f"{citekey}.md"

    if outfile.exists():
        choice = click.prompt('This file already exists. Overwrite (and lose content)? [y/n]')
        if strtobool(choice):
            print(f"Overwriting {str(outfile)}")
            outfile.write_text(str(md))
        else:
            print("I have not created a new reading note.")
    else:
        print(f"Writing {str(outfile)}")
        outfile.write_text(str(md))


@click.command(help="Configure Zotnote from the command line")
def config():
    click.echo("Not implemented yet.")


@click.command(help="Create a small, basic report based on the notes")
def report():
    click.echo("Not implemented yet.")


@click.group()
def cli():
    """Zotnote is a CLI-tool to streamline reading notes with Zotero
    """
    pass


# if __name__ == "__main__":
#     # Load variables from .env
#     load_dotenv(find_dotenv())

#     project_dir = Path(__file__).resolve().parents[1]
#     templates_dir = project_dir / "templates"

#     notes_dir = Path(os.getenv("NOTES_DIR"))
#     zotero_dir = Path(os.getenv("ZOTERO_DIR"))

#     AUTHOR = os.getenv("AUTHOR")

#     cli.add_command(new)
#     cli.add_command(report)
#     cli.add_command(config)
#     cli()

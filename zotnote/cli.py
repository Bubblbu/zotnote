# # -*- coding: utf-8 -*-
import sys
from pathlib import Path

import click

from zotnote.connectors.bbp import BetterBibtex

from .config import Configuration
from .templates import MarkdownNote


@click.command()
@click.argument('citekey')
def new(citekey):
    """Create reading note for CITEKEY in your Zotero library."""
    config = Configuration().load_config()

    candidates = BetterBibtex.search_citekey_in_bbp(citekey)
    if not candidates:
        click.echo("No results found for " + citekey)
        sys.exit()
    else:
        if len(candidates) != 1:
            click.echo("More potential matching articles. More options to be implemented soon.")
            sys.exit()
        else:
            candidate = candidates[0]

    fieldValues = BetterBibtex.extract_fields(candidate)

    click.echo(f"Found entry for {citekey}:\n\n"
               f"\tTitle: {fieldValues['title']}\n"
               f"\tCreator: {fieldValues['author']}\n"
               f"\tDate: {fieldValues['issued']}\n")

    choice = click.confirm("Continue?")
    if choice:
        pass
    else:
        click.echo("Cya!")
        sys.exit()

    # Fill template
    md = MarkdownNote(citekey, fieldValues, config)

    # Write output file
    notes_dir = Path(config['notes'])
    outfile = notes_dir / f"{citekey}.md"

    if outfile.exists():
        choice = click.confirm('This file already exists. Overwrite (and lose content)?')
        if choice:
            click.echo(f"Overwriting {str(outfile)}")
            outfile.write_text(str(md))
        else:
            click.echo("I have not created a new reading note.")
    else:
        click.echo(f"Writing {str(outfile)}")
        outfile.write_text(str(md))


@click.command(help="Configure Zotnote from the command line")
def config():
    Configuration.create_config()


@click.command(help="Update templates in local app data storage")
def update_templates():
    Configuration.copy_templates()


@click.command(help="Create a small, basic report based on the notes. (TBD")
def report():
    click.echo("Not implemented yet.")


@click.group()
def cli():
    """Zotnote is a CLI-tool to streamline reading notes with Zotero
    """

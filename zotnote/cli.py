# # -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

import click

from zotnote.connectors.bbp import BetterBibtex

from .config import Configuration
from .templates import MarkdownNote


def create_note(citekey):
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

    choice = click.confirm("Is this the correct document?")
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
        choice = click.confirm('This file already exists. Edit instead?')
        if choice:
            click.echo(f"Overwriting {str(outfile)}")
            outfile.write_text(str(md))
        else:
            click.echo("I have not created a new reading note.")
    else:
        click.echo(f"Writing {str(outfile)}")
        outfile.write_text(str(md))


@click.command(help="Create a new note")
@click.argument('citekey')
def new(citekey):
    create_note(citekey)


@click.command(help="Open note in your editor")
@click.argument('citekey')
def edit(citekey):
    config = Configuration().load_config()

    # Write output file
    notes_dir = Path(config['notes'])
    outfile = notes_dir / f"{citekey}.md"

    if outfile.exists():
        os.system(f"{config['editor']} {str(outfile)}")
    else:
        choice = click.confirm("File does not exist yet. Create now?")
        if choice:
            create_note(citekey)
        else:
            sys.exit()


@click.command(help="Remove a note")
@click.argument('citekey')
def remove(citekey):
    config = Configuration().load_config()

    # Write output file
    notes_dir = Path(config['notes'])
    outfile = notes_dir / f"{citekey}.md"

    if outfile.exists():
        choice = click.confirm("Are you sure you want to delete this note?")
        if choice:
            outfile.unlink()
        else:
            sys.exit()
    else:
        click.echo("This note does not exist.")


@click.command(help="Configure Zotnote from the command line")
def config():
    Configuration.create_config()


@click.command(help="Update templates in local app data storage")
def update_templates():
    Configuration.copy_templates()


@click.command(help="Create a small, basic report based on the notes.")
def report():
    click.echo("Not implemented yet.")


@click.group()
def cli():
    """Automatize and manage your reading notes with Zotero & Better Bibtex Plugin (BBT)
    """

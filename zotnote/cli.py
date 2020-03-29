# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

import click

from zotnote.connectors.bbt import (BetterBibtex, BetterBibtexException,
                                    BetterBibtexNotRunning)

from .config import Configuration
from .templates import MarkdownNote
from .utils import citekey_regex


def create_note(citekey, config, bbt, force):
    """Create reading note for CITEKEY in your Zotero library."""
    candidates = bbt.search_citekey_in_bbp(citekey)
    if not candidates:
        click.echo("No results found for " + citekey)
        sys.exit()
    elif len(candidates) != 1:
        click.echo("Something wrong happened here. We have too many candidates...")
        sys.exit()
    else:
        candidate = candidates[0]
        fieldValues = bbt.extract_fields(candidate)

        # Fill template
    md = MarkdownNote(citekey, fieldValues, config)

    # Write output file
    notes_dir = Path(config['notes'])
    outfile = notes_dir / f"{citekey}.md"

    if outfile.exists():
        if force:
            click.echo(f"Overwriting {str(outfile)}")
            outfile.write_text(str(md))
        else:
            choice = click.confirm(
                'This file already exists. Edit instead?" Use --force to overwrite files.')
            if choice:
                os.system(f"{config['editor']} {str(outfile)}")
    else:
        click.echo(f"Writing {str(outfile)}")
        outfile.write_text(str(md))


@click.command(help="Create a new note. If no citekey is provided the Zotero picker is launched.")
@click.argument('citekey', required=False)
@click.option("-f", "--force", is_flag=True, help="Overwrite existing notes")
def add(citekey, force):
    config = Configuration.load_config()

    try:
        bbt = BetterBibtex(config)
    except BetterBibtexNotRunning as e:
        click.echo(e)
        sys.exit()

    if citekey:
        match = citekey_regex.match(citekey)
        if match is None:
            click.echo("The citekey provided is not valid")
            sys.exit()
    else:
        citekey = bbt.citation_picker()
        if citekey is None:
            click.echo("No citation key provided.")
            sys.exit()

    create_note(citekey, config, bbt, force)


@click.command(help="Open note in your editor")
@click.argument('citekey')
def edit(citekey):
    config = Configuration.load_config()

    try:
        bbt = BetterBibtex(config)
    except BetterBibtexNotRunning as e:
        click.echo(e)
        sys.exit()

    if citekey:
        match = citekey_regex.match(citekey)
        if match is None:
            click.echo("The citekey provided is not valid")
            sys.exit()
    else:
        citekey = bbt.citation_picker()
        if citekey is None:
            sys.exit()

    # Write output file
    notes_dir = Path(config['notes'])
    outfile = notes_dir / f"{citekey}.md"

    if outfile.exists():
        os.system(f"{config['editor']} {str(outfile)}")
    else:
        choice = click.confirm("File does not exist yet. Create now?")
        if choice:
            create_note(citekey, config)
        else:
            sys.exit()


@click.command(help="Remove a note")
@click.argument('citekey')
def remove(citekey):
    config = Configuration.load_config()

    try:
        bbt = BetterBibtex(config)
    except BetterBibtexNotRunning as e:
        click.echo(e)
        sys.exit()

    if citekey:
        match = citekey_regex.match(citekey)
        if match is None:
            click.echo("The citekey provided is not valid")
            sys.exit()
    else:
        citekey = bbt.citation_picker()
        if citekey is None:
            sys.exit()

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

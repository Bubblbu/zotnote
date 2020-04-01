# -*- coding: utf-8 -*-
"""The main CLI module."""
import os
import sys
from pathlib import Path

import click
from click_option_group import RequiredMutuallyExclusiveOptionGroup
from click_option_group import optgroup

from .config.config import Configuration
from .connectors.bbt import BetterBibtex
from .connectors.bbt import BetterBibtexNotRunning
from .notes.note import BadTemplateName
from .notes.note import Note
from .utils.helpers import citekey_regex


def create_note(citekey, config, bbt, force, template):
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
    try:
        note = Note(citekey, fieldValues, config, template)
    except BadTemplateName as e:
        click.echo(e)
        sys.exit()

    # Write output file
    notes_dir = Path(config["notes"])
    outfile = notes_dir / f"{citekey}.md"

    if outfile.exists():
        if force:
            click.echo(f"Overwriting {str(outfile)}")
        else:
            choice = click.confirm(
                "This file already exists. Edit instead?"
                "Use --force to overwrite files."
            )
            if choice:
                os.system(f"{config['editor']} {str(outfile)}")
    else:
        click.echo(f"Writing {str(outfile)}")

    # Write note
    outfile.write_text(note.render())


@click.command()
@click.argument("citekey", required=False)
@click.option(
    "-t",
    "--template",
    default="simple",
    help="Template for note layout",
    metavar="TEMPLATE",
)
@click.option("-f", "--force", is_flag=True, help="Overwrite existing notes")
def add(citekey, force, template):
    """
    Create a new note. If no citekey is provided the Zotero picker is launched.

    CITEKEY is the cite key created by Better Bibtex.
    TEMPLATE is the type of the note created.

    See `templates` command for more details.
    """
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

    create_note(citekey, config, bbt, force, template)


@click.command()
@click.argument("citekey", required=False)
def edit(citekey):
    """
    Open a note in your editor of choice.

    CITEKEY is the cite key created by BBT.
    """
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
    notes_dir = Path(config["notes"])
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
@click.argument("citekey", required=False)
def remove(citekey):
    """Remove a note.

    CITEKEY is the cite key created by BBT.
    """
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
    notes_dir = Path(config["notes"])
    outfile = notes_dir / f"{citekey}.md"

    if outfile.exists():
        choice = click.confirm("Are you sure you want to delete this note?")
        if choice:
            outfile.unlink()
        else:
            sys.exit()
    else:
        click.echo("This note does not exist.")


@click.command()
def templates():
    """List all available templates for notes."""
    config = Configuration.load_config()

    templates = Note.list_all_templates(config)

    for t in templates:
        if t == "simple":
            click.echo(f"{t} (default)")
        else:
            click.echo(t)


@click.command()
@optgroup(
    "Edit configuration",
    cls=RequiredMutuallyExclusiveOptionGroup,
    help="Interact with the configuration",
)
@optgroup.option(
    "-l", "--list", is_flag=True, help="List all config key/value pairs",
)
@optgroup.option("-r", "--reset", is_flag=True, help="Reset config.")
@optgroup.option(
    "-u",
    "--update-entry",
    metavar="ENTRY",
    help="Update an ENTRY in the config file.",
    type=str,
)
def config(list, reset, update_entry):
    """Configure Zotnote from the command line."""
    config = Configuration.load_config()

    if list:
        for k, v in config.items():
            click.echo(f"{k}: {v}")
    elif reset:
        Configuration.create_config()
    elif update_entry is not None:
        if update_entry in config:
            click.echo(f"Old value: {config[update_entry]}")
            value = click.prompt("New value")
            Configuration.update_config(update_entry, value)
        else:
            click.echo(f"{update_entry} is not a valid entry in the config.")


@click.command()
def report():
    """Create a small, basic report based on the notes."""
    NotImplemented


@click.group()
def cli():
    """CLI for ZotNote."""
    pass

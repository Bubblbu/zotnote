# ZotNote

> A helper tool that automatises your reading notes with Zotero.

Vision: A literature review suite that connects to Zotero/Better-Bibtex. Writing and accessing reading notes plus some basic qualitative text analytics based on the written notes.

## Current features

- Very simple installation via pip
- Clean (very basic) CLI
- Connects to local Zotero and Better Bibtex databases to retrieve metadata
- Supports custom [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates for reading notes

*Planned features*

- Annotation of reading notes with special tags/keywords
  - Analytics based on these tags and keywords + content
- Retrieval of tags/keywords from Zotero
  - Enrich the reading notes with more metadata from Zotero
- Simple reports about progress of literature review 
- (*dreaming*) Automatically export collection of notes as an annotated bibliography.

## Getting started

### Requirements

I have currently only used the script on my own Linux machine.

- Python 3.6 (I am currently using f-strings)
- [Zotero Standalone](https://www.zotero.org/)
- [Better Bibtex plugin](https://github.com/retorquere/zotero-better-bibtex)

### Installation

The recommended way to install ZotNote is using [pipx](https://pipxproject.github.io/pipx/).

```bash
pipx install zotnote
```

Pipx cleanly install the package in an isolated environment (clean uninstalls!) and automagically exposes the cli-endpoints globally on your system.

However, you can also simply use pip.

```bash
pip install zotnote
```

## Usage

### Configuration

After installation you should be able to simply run `zotnote` and be prompted to a quick interactive configuration.

ZotNote currently asks you for:

- A name which is used in all reading notes.
- Path to your Zotero installation
- A folder to store your reading notes

### Creating your own notes

`zotnote new [citekey]` should be all you need to start creating your notes. The script will retrieve all required metadata from Zotero and populate the template stored in your notes folder and create a new reading note.

## Developers

The project is being developed with [Poetry](https://python-poetry.org/) as a dependency manager.

More instructions will follow soon!

## Authors

Written by Asura Enkhbayar while he was quarantined.
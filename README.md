# ZotNote

> Automatize and manage your reading notes with Zotero & Better Bibtex Plugin (BBT). **Note: ZotNote is still in early development and not production ready**

[![PyPI version](https://img.shields.io/pypi/v/zotnote.svg)](https://pypi.python.org/pypi/zotnote/)

---

*Current features*

- Very simple installation via pip
- Clean (very basic) CLI
- Connects to local Zotero & BBT databases to retrieve metadata
- Supports custom [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates for reading notes

*Planned features*

- Annotation of reading notes with special tags/keywords
  - Analytics based on these tags and keywords + content
- Retrieval of tags/keywords from Zotero
  - Enrich the reading notes with more metadata from Zotero
- Simple reports about progress of literature review 
- (*dreaming*) Automatically export collection of notes as an annotated bibliography.

*Long-term vision*

A literature review suite that connects to Zotero & BBT. Management of reading notes, reading/writing analytics, and basic qualitative text analysis (export reports as HTML via Jupyter notebooks). Export of reading notes in different formats (e.g., annotated bibliography).

## Installation

### Requirements

- [Python](https://www.python.org/downloads/) 3.6 or higher
- [Zotero Standalone](https://www.zotero.org/) with [Better Bibtex plugin](https://github.com/retorquere/zotero-better-bibtex)

### Recommended: Install via pipx

The recommended way to install ZotNote is using [pipx](https://pipxproject.github.io/pipx/). Pipx cleanly install the package in an isolated environment (clean uninstalls!) and automagically exposes the CLI-endpoints globally on your system.

```bash
pipx install zotnote

```


### Option 2: Install via pip

However, you can also simply use pip. Please be aware of the Python version and environments you are using.

```bash
pip install zotnote
```

### Option 3: Download from GitHub

Download the latest release from Github and unzip. Put the folder containing the scripts into your `PATH`. 

Alternatively, run

```bash
[sudo] python3 setup.py install
```

or

```bash
python3 setup.py install --user
```

### Option 4: Git clone (for developers)

```bash
git clone git@github.com:Bubblbu/zotnote.git
```

The project is being developed with [Poetry](https://python-poetry.org/) as a dependency manager.

More instructions will follow soon!

## Getting started

```
Usage: zotnote [OPTIONS] COMMAND [ARGS]...

  Automatize and manage your reading notes with Zotero & Better Bibtex
  Plugin (BBT)

Options:
  --help  Show this message and exit.

Commands:
  config            Configure Zotnote from the command line
  edit              Open note in your editor
  new               Create a new note
  remove            Remove a note
  report            Create a small, basic report based on the notes.
  update-templates  Update templates in local app data storage
```

### Configuration

After installation you should be able to simply run `zotnote` and be prompted to a quick interactive configuration.

ZotNote currently asks you for:

- A name which is used in all reading notes.
- Path to your Zotero installation
- A folder to store your reading notes

### Usage

`zotnote new [citekey]` should be all you need to start creating your notes. The script will retrieve all required metadata from Zotero and populate the template stored in your notes folder and create a new reading note.

## Authors

Written by [Asura Enkhbayar](https://twitter.com/bubblbu_) while he was quarantined.

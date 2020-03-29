# ZotNote

Automatize and manage your reading notes with Zotero & Better Bibtex Plugin (BBT). **Note: ZotNote is still in early development and not production ready**

[![PyPI version](https://img.shields.io/pypi/v/zotnote.svg)](https://pypi.python.org/pypi/zotnote/)

![ZotNote demo](assets/demo.gif)

---

*Current features*

- Simple installation via pipx/pip
- Full command-line interface to create, edit, and remove notes
- Easy selection of entries with interactive Zotero citation picker
- Templating for the reading notes ([Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)) 

*Planned features*

- Annotation of reading notes and individual quotes using tags/keywords
  - Retrieval of relevant quotes based on these tags and keywords
  - Analytics based on these tags and keywords
- Enrich reading notes with more metadata from Zotero
- Simple reports about progress of literature review 
- (*dreaming*) Automatically export collection of notes as an annotated bibliography.

*Long-term vision*

A literature review suite that connects to Zotero & BBT. Management of reading notes, reading/writing analytics, and basic qualitative text analysis (export reports as HTML via Jupyter notebooks). Export of reading notes in different formats (e.g., annotated bibliography).

You can find a roadmap for ZotNote [here](https://github.com/Bubblbu/zotnote/projects/1).

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

```shell
Usage: zotnote [OPTIONS] COMMAND [ARGS]...

  Automatize and manage your reading notes with Zotero & Better Bibtex
  Plugin (BBT)

Options:
  --help  Show this message and exit.

Commands:
  add     Create a new note.
  config  Configure Zotnote from the command line.
  edit    Open a note in your editor of choice.
  remove  Remove a note
```

### Configuration

After installation you should be able to simply run `zotnote` and be prompted to a quick command-line configuration.

ZotNote currently asks you for:

- A name which is used in all reading notes.
- An email address
- Path to your Zotero installation (not required anymore. To be removed soon)
- A folder to store your reading notes

### Usage

`zotnote add [citekey]` should be all you need to start creating your notes. If you don't provide a citekey ZotNote will launch the Zotero picker for you.

## Authors

Written by [Asura Enkhbayar](https://twitter.com/bubblbu_) while he was quarantined.

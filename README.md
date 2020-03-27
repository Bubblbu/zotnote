# ZotNote

A helper tool that automatises reading note management with Zotero.

## Features

- Connects to local Zotero and Better Bibtex databases to retrieve metadata
- Supports custom templates for reading notes
- CLI interface to populate templates and create reading note skeletons

*Planned features*

- Basic annotations
- Retrieval of tags/keywords from Zotero
- Text analysis of reading notes
- Export as annotated bibliography

## Getting started

### Requirements

I have currently only used the script on my own Linux machine.

- Python 3.6 (I am currently using f-strings)
- [Zotero Standalone](https://www.zotero.org/)
- [Better Bibtex plugin](https://github.com/retorquere/zotero-better-bibtex)

### Installation

Just copy the script found in `src` to a folder on your machine. Make sure to add the folder to your PATH and make the file executable.

## Usage

### Configuration

The script contains a few variables that you have to rename to according to your own file system.

```bash
NOTES = "/path/to/reading/notes"
ZOTERO = "/path/to/zotero"

AUTHOR = "Your Name"
```

Make sure to copy `templates/template.txt` to your NOTES folder.

## Creating your own notes

`new_zotnote.py citekey` should be all you need to start creating your notes. The script will retrieve all required metadata from Zotero and populate the template stored in your notes folder and create a new reading note.
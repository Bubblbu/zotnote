# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 31-03-2019

- Major redesign of how configuration, notes, and templates are managed
    - XDG_DATA_HOME is no longer used to store templates. User templates will be loaded from notes folder
    - Implemented a Note class to manage notes/templates related methods
- Changes to CLI:
    - Added `templates` function to list all available templates
    - Added `-t/--template` option to `zotnote add` to choose between various formats
- Improved python project management
    - Added bump2version to project
    - Added pre-commit running various hooks

## [0.2.0] - 27-03-2019

- Completely removed requirements to access local SQLite database. Now using the BBP search interface.
   - Will probably remove all sqlite3 dependencies in the future.
- Modified "create" command to no longer overwrite files.
- Added "edit" command to open notes in an editor
- Added "remove" command to delete note

## [0.1.0] - 26-03-2019

Initial version released.

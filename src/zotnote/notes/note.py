# -*- coding: utf-8 -*-
"""
This module manages notes.

- Read and write notes
- Manage templates
- Export notes to different formats
"""

import datetime
from pathlib import Path

from jinja2 import Template
from zotnote import ROOT


class BadTemplateName(Exception):
    """This exception is thrown when a BadTemplate is loaded."""

    pass


class Note:
    """The Note class."""

    templates_dir = ROOT / "notes/templates"
    content_dir = templates_dir / "content"

    # Load the master template
    master_file = templates_dir / "master.j2"

    def __init__(self, citekey, fieldValues, config, note_type):
        """Construct note with citekey and retrieved values."""
        self.citekey = citekey
        self.fieldValues = fieldValues

        self.ts = datetime.datetime.now()
        self.ts_iso = self.ts.isoformat(timespec="seconds")
        self.ts_day = self.ts.strftime("%m.%d.%y")

        self.author = config["name"]
        self.email = config["email"]

        notes_dir = Path(config["notes"])
        self.user_templates = notes_dir / "templates"

        # Ensure that content type is set and valid
        self.content_template = None

        # Check if user template is present in notes folder
        files = self.user_templates.glob("*.j2")
        for f in files:
            if note_type + ".j2" == f.name:
                self.content_template = f

        # If not found, check in system templates
        if self.content_template is None:
            files = self.content_dir.glob("*.j2")
            for f in files:
                if note_type + ".j2" == f.name:
                    self.content_template = f

        # If content_template is still not found:
        if self.content_template is None:
            raise BadTemplateName("Invalid template name.")

    def render(self):
        """Render note with template and save to disk."""
        master = Template(self.master_file.read_text())
        content = Template(self.content_template.read_text())

        # Render content
        d = {
            "citekey": self.citekey,
            "author": self.author,
            "ts": self.ts_iso,
            "ts_day": self.ts_day,
            "title": self.fieldValues["title"],
            "creator": self.fieldValues["author"],
            "date": self.fieldValues["issued"],
            "doi": self.fieldValues["DOI"],
            "type": self.fieldValues["type"],
        }
        rendered = master.render(d) + "\n\n" + content.render()

        return rendered

    @classmethod
    def list_all_templates(cls, config):
        notes_dir = Path(config["notes"])
        user_templates = notes_dir / "templates"

        templates = []
        # Check if user template is present in notes folder
        files = user_templates.glob("*.j2")
        templates.extend([f.name.split(".")[0] for f in files])

        files = cls.content_dir.glob("*.j2")
        templates.extend([f.name.split(".")[0] for f in files])

        return set(templates)

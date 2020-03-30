# -*- coding: utf-8 -*-
"""
This module manages notes.

- Read and write notes
- Manage templates
- Export notes to different formats
"""

import datetime

from jinja2 import Template

from zotnote import data_dir


class Note:
    """The Note class."""

    def __init__(self, citekey, fieldValues, config):
        """Construct note with citekey and retrieved values."""
        self.citekey = citekey
        self.fieldValues = fieldValues

        self.ts = datetime.datetime.now()
        self.ts_iso = self.ts.isoformat(timespec="seconds")
        self.ts_day = self.ts.strftime("%m.%d.%y")

        self.author = config["name"]

        filein = data_dir / "templates/template.j2"
        self.__template = Template(filein.read_text())

    def render_note(self, template=None):
        """Render note with template and save to disk."""
        if template is None:
            template = self.__template
        else:
            NotImplemented

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
        return template.render(d)

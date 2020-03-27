#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import datetime

from jinja2 import Template

from zotnote import AUTHOR, notes_dir


class MarkdownTemplate():
    def __init__(self, citekey, fieldValues):
        self.citekey = citekey
        self.fieldValues = fieldValues

        self.ts = datetime.datetime.now()
        self.ts_iso = self.ts.isoformat(timespec="seconds")
        self.ts_day = self.ts.strftime("%m.%d.%y")

        self.author = AUTHOR
        filein = notes_dir / "template.j2"
        self.__template = Template(filein.read_text())

    def __str__(self):
        d = {
            'citekey': self.citekey,
            'author': self.author,
            'ts': self.ts_iso,
            'ts_day': self.ts_day,
            'title': self.fieldValues['title'],
            'creator': self.fieldValues['creator'],
            'date': self.fieldValues['date'],
            'doi': self.fieldValues['DOI'],
            'type': self.fieldValues['type']
        }
        return self.__template.render(d)

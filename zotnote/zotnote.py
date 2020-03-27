#!/usr/bin/env python
# # -*- coding: utf-8 -*-
import click
import datetime
import json
import sqlite3
import sys
from distutils.util import strtobool
from pathlib import Path
import click

ZOTERO = Path("/home/asura/Zotero/")
NOTES = Path("/home/asura/Documents/notes/")

AUTHOR = "Asura Enkhbayar"


class BetterBibtexException(Exception):
    pass


class MarkdownTemplate():
    def __init__(self, citekey, fieldValues):
        self.citekey = citekey
        self.fieldValues = fieldValues
        self.ts = datetime.datetime.now()
        self.ts_iso = self.ts.isoformat(timespec="seconds")
        self.ts_day = self.ts.strftime("%m.%d.%y")

        self.author = AUTHOR

        filein = NOTES / "template.txt"
        self.__template = Template(filein.read_text())

    def __str__(self):
        d = {
            'citekey': self.citekey,
            'author': AUTHOR,
            'ts': self.ts_iso,
            'ts_day': self.ts_day,
            'title': self.fieldValues['title'],
            'creator': self.fieldValues['creator'],
            'date': self.fieldValues['date'],
            'doi': self.fieldValues['DOI'],
            'type': self.fieldValues['type']
        }
        return self.__template.substitute(d)


class ZoteroDBConnector():
    """This class manages the connections to both Zotero's and
    Better Bibtex's local SQLite databases.
    """

    def __init__(self, citekey):
        self.__citekey = citekey
        self.__itemID = None

        self.__fieldIDs = {
            'title': 110,
            'DOI': 26,
            'date': 14
        }

        self.__zotero = None

        self.fieldValues = {
            'title': "",
            'type': "",
            'DOI': "",
            'date': "",
            'creator': ""
        }

    def __get_value_id(self):
        results = self.__zotero.execute(
            f"SELECT fieldID, valueID from itemData where itemID=\"{self.itemID}\"")
        return {f: v for (f, v) in results.fetchall()}

    def __get_value_labels(self, valueID):
        result = self.__zotero.execute(
            f"SELECT value from itemDataValues where valueID=\"{valueID}\"")
        return result.fetchone()[0]

    def __get_type_name(self):
        result = self.__zotero.execute(
            f"SELECT itemTypeID from items where itemID=\"{self.itemID}\"")
        itemTypeID = result.fetchone()[0]
        result = self.__zotero.execute(
            f"SELECT typeName from itemTypes where itemTypeID=\"{itemTypeID}\"")
        return result.fetchone()[0]

    def __get_creator_name(self):
        result = self.__zotero.execute(
            f"SELECT creatorID from itemCreators where itemID=\"{self.itemID}\"")
        creators = result.fetchall()
        creatorIDs = [_[0] for _ in creators]

        creators = []
        for creatorID in creatorIDs:
            result = self.__zotero.execute(
                f"SELECT firstName, lastName from creators where creatorID=\"{creatorID}\"")
            name = result.fetchone()
            creators.append(f"{name[1]}, {name[0]}")
        return "; ".join(creators)

    def citekey_lookup(self):
        better_bibtex = sqlite3.connect(str(ZOTERO / "better-bibtex.sqlite.bak"))
        keys_string = better_bibtex.execute(
            'SELECT data FROM "better-bibtex" WHERE name="better-bibtex.citekey"')
        keys_dict = json.loads(keys_string.fetchone()[0])
        better_bibtex.close()

        k = {v['citekey']: v['itemID'] for v in keys_dict['data']}

        if self.__citekey in k:
            self.itemID = k[self.__citekey]
        else:
            raise BetterBibtexException(f"Couldn't find \"{self.__citekey}\" in"
                                        " your Zotero library")

    def get_field_values(self):
        self.__zotero = sqlite3.connect(str(ZOTERO / "zotero.sqlite.bak"))

        valueIDs = self.__get_value_id()
        for l, fID in self.__fieldIDs.items():
            try:
                self.fieldValues[l] = self.__get_value_labels(valueIDs[fID])
            except Exception:
                pass

        if self.fieldValues['date'] != "":
            self.fieldValues['date'] = self.fieldValues['date'].split(" ")[-1]

        # creator string
        self.fieldValues['creator'] = self.__get_creator_name()

        # item type
        self.fieldValues['type'] = self.__get_type_name()

        # Close the connection
        self.__zotero.close()
        return self.fieldValues


if __name__ == "__main__":
    """This is ZotNote.
    """
    # Initialize argument parser
    parser = argparse.ArgumentParser(
        prog="ZotNote",
        description='This is a script that fetches data from local Zotero'
                    'databases and creates a template for reading notes.')
    
    new_group = parser.add_argument_group()
    report_group = parser.add_mutually_exclusive_group(required=True)
    parser.add
    # Add arguments
    parser.add_argument("command", action="store", type=str,
                        choices=["new", "report"], metavar="COMMAND",
                        help="Actions that you can run")
    new_group.add_argument("citekey", action="store", type=str, metavar="CITEKEY",
                        help="The citekey for selected entry as managed by"
                        "better-bibtex-plugin")

    # Parse arguments from command line
    args = parser.parse_args()

    command = args.command
    citekey = args.citekey

    # Mode
    if command == "new":
        # Retrieve Information from Zotero
        zotero = ZoteroDBConnector(citekey)

        try:
            zotero.citekey_lookup()
        except BetterBibtexException as e:
            print(e)
            sys.exit()

        fieldValues = zotero.get_field_values()

        print(f"Found entry for {citekey}:\n\n"
              f"\tTitle: {fieldValues['title']}\n"
              f"\tCreator: {fieldValues['creator']}\n"
              f"\tDate: {fieldValues['date']}\n")

        choice = input("Continue? [y/n]\n").lower()
        if strtobool(choice):
            pass
        else:
            print("Cya!")
            sys.exit()

        # Fill template
        md = MarkdownTemplate(citekey, fieldValues)

        # Write output file
        file = NOTES / f"{citekey}.md"

        if file.exists():
            choice = input(
                "This file already exists. Overwrite (and lose content)? [y/n]\n").lower()
            if strtobool(choice):
                print(f"Overwriting {str(file)}")
                file.write_text(str(md))
            else:
                print("I have not created a new reading note.")
        else:
            print(f"Writing {str(file)}")
            file.write_text(str(md))
    elif command == "report":
        print("Not implemented yet")

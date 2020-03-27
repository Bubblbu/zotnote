#!/usr/bin/env python
# # -*- coding: utf-8 -*-
import json
import sqlite3
from pathlib import Path


class BetterBibtexException(Exception):
    pass


class ZoteroDBConnector():
    """This class manages the connections to both Zotero's and
    Better Bibtex's local SQLite databases.
    """

    def __init__(self, citekey, config):
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

        self.zotero_dir = Path(config['zotero'])

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
        better_bibtex = sqlite3.connect(str(self.zotero_dir / "better-bibtex.sqlite.bak"))
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
        self.__zotero = sqlite3.connect(str(self.zotero_dir / "zotero.sqlite.bak"))

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

# # -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path


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

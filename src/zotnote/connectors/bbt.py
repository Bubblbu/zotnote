# -*- coding: utf-8 -*-
"""This module contains code to interface with Better Bibtex."""
import json

import requests
from zotnote.utils.helpers import prune_author_str

SEARCH = "items.search"
BIBLIOGRAPHY = "items.bibliography"
NOTES = "items.notes"
ATTACHEMENTS = "items.attachements"


class BetterBibtexNotRunning(Exception):
    """This error is thrown when BBT is not running."""

    pass


class BetterBibtexSearchError(Exception):
    """This error is thrown when something fails during the request."""

    pass


class BetterBibtexBadRequest(Exception):
    """This error is thrown when BBT detects a bad request."""

    pass


class BetterBibtex:
    """Wrapper class to access and manage BetterBibtex."""

    BASE_URL = "http://localhost:23119/better-bibtex/"
    SEARCH_URL = BASE_URL + "json-rpc"
    CAYW_URL = BASE_URL + "cayw"

    def __init__(self, config):
        """Initialise BBT.

        Sets up the requests for the JSON-RPC endpoints and check is BBT is running
        """
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.payload = {"jsonrpc": "2.0", "method": None, "params": None}

        if not self.probe_bbt():
            raise BetterBibtexNotRunning(
                "Better Bibtex is not running. Please make sure to launch Zotero BBT"
            )

    def probe_bbt(self):
        """Check if Zotero & BBT are running."""
        r = requests.get(BetterBibtex.CAYW_URL + "?probe=probe")
        if r.text == "ready":
            return True
        else:
            return False

    def citation_picker(self):
        """Launch the Zotero citation picker and return result."""
        r = requests.get(BetterBibtex.CAYW_URL)
        return r.text

    # JSON-RPC API endpoints
    def search(self, citekey):
        """Search the endpoint with a citekey. Returns all candidates."""
        payload = self.payload
        payload["method"] = "item.search"
        payload["params"] = [f"{citekey}"]
        payload = json.dumps([payload])

        try:
            r = requests.post(
                BetterBibtex.SEARCH_URL, data=payload, headers=self.headers
            )
        except ConnectionError:
            raise BetterBibtexNotRunning("Are you sure that Zotero is running?")

        if r.status_code == 200:
            r = r.json()[0]
            if "error" in r:
                raise BetterBibtexBadRequest(r["error"])
            else:
                return r["result"]
        else:
            raise BetterBibtexSearchError(
                "Request returned with status code: " + r.status_code
            )

    def bibliography(self, citekey):
        """Retrieve bibliographic entry for citekey."""
        payload = self.payload
        payload["metod"] = "item.bibliography"
        payload["params"] = [f"{citekey}"]
        payload = json.dumps([payload])

    def notes(self, citekey):
        """Retrieve bibliographic entry for citekey."""
        payload = self.payload
        payload["metod"] = "item.notes"
        payload["params"] = [f"{citekey}"]
        payload = json.dumps([payload])

    @staticmethod
    def select_candidate(candidates):
        NotImplemented

    @staticmethod
    def extract_fields(candidate, selected_fields):
        """
        Pretty simple function that retrieves the article information.

        Returns a dict defined by selected fields.

        This one should probably be exported to its own class representing
        articles in an intermediate stage.
        """
        selected_fields = ["title", "DOI", "type", "issued", "author"]
        author_str_len = 60

        article = {f: None for f in selected_fields}

        for f in selected_fields:
            if f in candidate:
                if f == "author":
                    author_str = []
                    for name in candidate[f]:
                        name_str = f"{name['family']}, {name['given']}"
                        author_str.append(name_str)
                    author_str = "; ".join(author_str)
                    if len(author_str) >= author_str_len:
                        author_str = prune_author_str(author_str, author_str_len)
                    article[f] = author_str
                elif f == "issued":
                    year = candidate[f]["date-parts"][0][0]
                    article[f] = year
                else:
                    article[f] = candidate[f]
        return article

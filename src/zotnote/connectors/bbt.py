# -*- coding: utf-8 -*-
"""This module contains code to interface with Better Bibtex."""
import json

import requests
from zotnote.utils.helpers import prune_author_str


class BetterBibtexNotRunning(Exception):
    """This error is thrown when BBT is not running."""

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
        self.payload = [{"jsonrpc": "2.0", "method": "item.search", "params": None}]

        self.selected_fields = ["title", "DOI", "type", "issued", "author"]

        self.author_str_len = 60

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

    def search_citekey_in_bbp(self, citekey):
        """Search the endpoint with a citekey. Returns all candidates."""
        payload = self.payload
        payload[0]["params"] = [f"{citekey}"]
        payload = json.dumps(payload)

        r = requests.post(BetterBibtex.SEARCH_URL, data=payload, headers=self.headers)
        if r.status_code == 200:
            candidates = r.json()[0]["result"]
            return candidates
        else:
            return None

    def extract_fields(self, candidate):
        """
        Pretty simple function that retrieves the article information.

        Returns a dict defined by selected fields.
        """
        article = {f: None for f in self.selected_fields}

        for f in self.selected_fields:
            if f in candidate:
                if f == "author":
                    author_str = []
                    for name in candidate[f]:
                        name_str = f"{name['family']}, {name['given']}"
                        author_str.append(name_str)
                    author_str = "; ".join(author_str)
                    if len(author_str) >= self.author_str_len:
                        author_str = prune_author_str(author_str, self.author_str_len)
                    article[f] = author_str
                elif f == "issued":
                    year = candidate[f]["date-parts"][0][0]
                    article[f] = year
                else:
                    article[f] = candidate[f]
        return article

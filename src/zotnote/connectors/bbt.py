# -*- coding: utf-8 -*-
"""This module contains code to interface with Better Bibtex."""
import json
from textwrap import fill
from textwrap import indent

import click
import requests
from zotnote.utils.helpers import prune_author_str


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

    # URLs and endpoints
    BASE_URL = "http://localhost:23119/better-bibtex/"
    JSON_RPC = BASE_URL + "json-rpc"
    CAYW_URL = BASE_URL + "cayw"

    # JSON-RPC methods
    SEARCH = "items.search"
    BIBLIOGRAPHY = "items.bibliography"
    NOTES = "items.notes"
    ATTACHEMENTS = "items.attachements"

    def __init__(self, citation_style="apa"):
        """Initialise BBT.

        Sets up the requests for the JSON-RPC endpoints and check is BBT is running
        """
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.payload = {"jsonrpc": "2.0", "method": None, "params": None}
        self.citation_style = citation_style

        if not self.__probe_bbt():
            raise BetterBibtexNotRunning(
                "Better Bibtex is not running. Please make sure to launch Zotero BBT"
            )

    @classmethod
    def __probe_bbt(cls):
        """Check if Zotero & BBT are running."""
        r = requests.get(cls.CAYW_URL + "?probe=probe")
        if r.text == "ready":
            return True
        else:
            return False

    @classmethod
    def citation_picker(cls):
        """Launch the Zotero citation picker and return result."""
        r = requests.get(cls.CAYW_URL)
        return r.text

    # JSON-RPC API endpoints
    def search(self, citekey):
        """
        Search the endpoint with a citekey.

        Returns a single candidate or None.
        """
        payload = self.payload
        payload["method"] = "item.search"
        payload["params"] = [citekey]
        payload = json.dumps([payload])

        try:
            candidates = self.__request(payload, self.headers)
        except BetterBibtexNotRunning:
            raise
        except BetterBibtexSearchError:
            raise
        except BetterBibtexBadRequest:
            raise

        if not candidates:
            candidate = None
        elif len(candidates) == 1:
            candidate = candidates[0]
        elif len(candidates) > 1:
            candidate = self.select_candidate(candidates)

        return candidate

    def select_candidate(self, candidates):
        """Interactively select item from candidates."""
        items = {}
        for ix, c in enumerate(candidates):
            citekey = c["citekey"]
            zot_id = c["id"].split("/")[-1]
            citation = self.bibliography(citekey)

            items[ix] = {"citekey": citekey, "zot_id": zot_id, "citation": citation}

        click.echo("")
        for i in range(len(candidates)):
            item = items[i]
            click.echo(f"[{i+1}] {item['citekey']}")
            click.echo("\t")
            click.echo(indent(fill(f">> {item['citation']}"), "\t"))
            click.echo("")

        selection = click.prompt(
            "Choose the correct item from ",
            prompt_suffix=f"[1-{len(candidates)}] | Enter anything else to abort.",
        )
        try:
            sel = int(selection) - 1
        except Exception:
            click.echo("Input is not a number.")
            return None

        if sel <= len(candidates):
            return candidates[sel]
        else:
            click.echo("Input is not a valid choice.")
            return None

    def bibliography(self, citekey):
        """Retrieve bibliographic entry for citekey."""
        payload = self.payload
        payload["method"] = "item.bibliography"
        payload["params"] = [[citekey], {"id": self.citation_style}]
        payload = json.dumps([payload])

        try:
            bib = self.__request(payload, self.headers)
        except BetterBibtexNotRunning:
            raise
        except BetterBibtexSearchError:
            raise
        except BetterBibtexBadRequest:
            raise

        return bib

    def notes(self, citekey):
        """Retrieve bibliographic entry for citekey."""
        payload = self.payload
        payload["method"] = "item.notes"
        payload["params"] = [f"{citekey}"]
        payload = json.dumps([payload])

    @classmethod
    def __request(cls, payload, headers):
        """Process all requests to BBT."""
        try:
            r = requests.post(cls.JSON_RPC, data=payload, headers=headers)
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

    @staticmethod
    def extract_fields(candidate):
        """
        Pretty simple function that retrieves the article information.

        Returns a dict defined by selected fields.

        This one should probably be exported to its own class representing
        articles in an intermediate stage.
        """
        selected_fields = ["title", "DOI", "type", "issued", "author", "citekey", "id"]
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

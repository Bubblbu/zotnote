#!/usr/bin/env python
"""
API wrapper for Better Bibtex
"""
import requests
import json


class BetterBibtexException(Exception):
    pass


class BetterBibtex:
    """
    Wrapper to accces the Better Bibtex search endpoints. Ensure that Zotero is running.
    """
    url = "http://localhost:23119/better-bibtex/json-rpc"
    headers = {'Content-Type': "application/json", 'Accept': "application/json"}
    payload = [{"jsonrpc": "2.0", "method": "item.search", "params": None}]

    selected_fields = ["title", "DOI", "type", "issued", "author"]
    author_str_len = 60

    @classmethod
    def search_citekey_in_bbp(cls, citekey):
        """
        Searches the endpoint with the given search term (citekey).

        Returns all candidates.
        """
        payload = cls.payload
        payload[0]['params'] = [f"{citekey}"]
        payload = json.dumps(payload)

        r = requests.post(cls.url, data=payload, headers=cls.headers)
        if r.status_code == 200:
            candidates = r.json()[0]['result']
            return candidates
        else:
            return None

    @classmethod
    def extract_fields(cls, candidate):
        """
        Pretty simple function that retrieves the article information

        Returns a dict defined by selected fields.
        """
        article = {f: None for f in cls.selected_fields}

        for f in cls.selected_fields:
            if f in candidate:
                if f == "author":
                    author_str = []
                    for name in candidate[f]:
                        name_str = f"{name['family']}, {name['given']}"
                        author_str.append(name_str)
                    author_str = "; ".join(author_str)
                    if len(author_str) >= cls.author_str_len:
                        author_str = cls.prune_author_str(author_str,
                                                          cls.author_str_len)
                    article[f] = author_str
                elif f == "issued":
                    year = candidate[f]['date-parts'][0][0]
                    article[f] = year
                else:
                    article[f] = candidate[f]
        return article

    @staticmethod
    def prune_author_str(string, maxlen):
        strings = string.split("; ")
        string = "; ".join(strings[0:-1])[0:maxlen]
        string = string + "...; " + strings[-1]
        return string

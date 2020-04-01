# -*- coding: utf-8 -*-
"""Various utility functions."""

import re

citekey_regex = re.compile(r"^[a-z0-9]+_[a-z0-9]+_[a-z0-9]+$")


def prune_author_str(author_str, maxlen):
    """Shorten author string.

    If len(AUTHOR_STR) > MAXLEN the authors are shortened
    using an ellipsis while retaining the last author.
    """
    strings = author_str.split("; ")
    string = "; ".join(strings[0:-1])[0:maxlen]
    string = string + "...; " + strings[-1]
    return string

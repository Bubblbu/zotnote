# -*- coding: utf-8 -*-
import re

citekey_regex = re.compile(r"^[a-z0-9]+_[a-z0-9]+_[a-z0-9]+$")


def prune_author_str(string, maxlen):
    """Shorten author string to a certain character length.
    The last author is still shown while middle authors are
    at one point shortened ...
    """
    strings = string.split("; ")
    string = "; ".join(strings[0:-1])[0:maxlen]
    string = string + "...; " + strings[-1]
    return string

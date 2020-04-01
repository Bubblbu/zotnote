# -*- coding: utf-8 -*-
"""Some definitions for the whole package."""
from pathlib import Path

from xdg import XDG_CONFIG_HOME, XDG_DATA_HOME

base_dir = Path(__file__).resolve().parent
config_dir = Path(XDG_CONFIG_HOME) / "zotnote"
data_dir = Path(XDG_DATA_HOME) / "zotnote"

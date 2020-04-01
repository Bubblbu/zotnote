# -*- coding: utf-8 -*-
"""Some definitions for the whole package."""
from pathlib import Path

from xdg import XDG_CONFIG_HOME

ROOT = Path(__file__).resolve().parent
config_dir = Path(XDG_CONFIG_HOME) / "zotnote"

# -*- coding: utf-8 -*-
from pathlib import Path

from xdg import XDG_CONFIG_HOME, XDG_DATA_HOME

config_dir = Path(XDG_CONFIG_HOME) / "zotnote"
data_dir = Path(XDG_DATA_HOME) / "zotnote"

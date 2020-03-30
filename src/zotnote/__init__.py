# -*- coding: utf-8 -*-
from pathlib import Path

from xdg import XDG_CONFIG_HOME, XDG_DATA_HOME

project_dir = Path(__file__).parents[1]
config_dir = Path(XDG_CONFIG_HOME) / "zotnote"
data_dir = Path(XDG_DATA_HOME) / "zotnote"

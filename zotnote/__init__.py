# -*- coding: utf-8 -*-
from dotenv import find_dotenv, load_dotenv
import os
from pathlib import Path

# Load variables from .env
load_dotenv(find_dotenv())

project_dir = Path(__file__).resolve().parents[1]
templates_dir = project_dir / "templates"

notes_dir = Path(os.getenv("NOTES_DIR"))
zotero_dir = Path(os.getenv("ZOTERO_DIR"))

AUTHOR = os.getenv("AUTHOR")
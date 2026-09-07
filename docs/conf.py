from __future__ import annotations

import os
from datetime import datetime, timezone

project = "MLO CLASSI Spectrograph"
author = "Caden Gobat (SDSU)"
copyright = f"{datetime.now(timezone.utc).year}, San Diego State University"

extensions = []

source_suffix = {
    ".rst": "restructuredtext",
}

master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

nitpicky = True

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "MLO CLASSI Spectrograph"
html_show_sourcelink = True

html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "sticky_navigation": True,
    "titles_only": False,
}

repository = os.environ.get("GITHUB_REPOSITORY", "")
if "/" in repository:
    github_user, github_repo = repository.split("/", 1)
    html_context = {
        "display_github": True,
        "github_user": github_user,
        "github_repo": github_repo,
        "github_version": "main",
        "conf_py_path": "/docs/",
    }
else:
    html_context = {}

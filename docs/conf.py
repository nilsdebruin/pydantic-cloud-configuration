"""Sphinx configuration."""
project = "Pydantic Cloud Settings"
author = "Nils de Bruin"
copyright = "2022, Nils de Bruin"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"

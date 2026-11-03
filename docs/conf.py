# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. The freepygame package lives at the
# repository root, one level above this conf.py.
sys.path.insert(0, os.path.abspath(".."))

# -- Project information ------------------------------------------------------

project = "freepygame"
copyright = "2026, freebird"
author = "freebird"
release = "0.1.0"
version = "0.1"

# -- General configuration ----------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",      # generate API docs from docstrings
    "sphinx.ext.napoleon",     # support Google / NumPy style docstrings
    "sphinx.ext.viewcode",     # link to source code
    "sphinx.ext.intersphinx",  # link to external projects (pygame)
]

# Napoleon: accept both Google- and NumPy-style docstrings (the codebase uses a
# mixed Chinese/Google style).
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False

# Intersphinx mapping so `:py:class:`pygame.Surface`` etc. can be cross-linked
# when the pygame docs are reachable; failures are silently ignored.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pygame": ("https://www.pygame.org/docs", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output --------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]
html_title = "freepygame 文档"

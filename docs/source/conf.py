# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))
sys.path.append(os.path.abspath('exts'))

# -- Project information -----------------------------------------------------

project = 'InstaTweet'
copyright = '2022, Adam Korn'
author = 'Adam Korn'

# The full version, including alpha/beta/rc tags
release = '2.0.0b0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# InterSphinx to add Python and Tweepy references
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'tweepy': ('https://docs.tweepy.org/en/stable/', None),
    'sqlalchemy': ('https://docs.sqlalchemy.org/en/14/', None)
}

# I don't think i need this but..
master_doc = 'index'

# ---- Autodoc Settings ------------------------------------------------------
#
# Order based on source
autodoc_member_order = 'bysource'
#
# Remove typehints from method signatures and put in description instead
autodoc_typehints = 'description'
#
# Only add typehints for documented parameters (and all return types);
# this prevents parameters being documented twice for both the class and __init__
# which was driving me INSANE bc literally for what??? like who.. WHO wants that
autodoc_typehints_description_target = 'documented_params'

# ---- MyST Parser Settings ------------------------------------------------------
#
source_suffix = ['.rst', '.md']


# ---- Skip and Setup Method -------------------------------------------------
def skip(app, what, name, obj, would_skip, options):
    """Include __init__ as a documented method"""
    if name in ('__init__',):
        return False
    return would_skip


def setup(app):
    app.connect('autodoc-skip-member', skip)
    app.add_css_file("property.css")  # To prevent horizontal stacking in RTD

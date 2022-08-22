# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# List of Options from RTD:
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
#
# No sys.path.insert bc it breaks everything <3


# ================================== Imports ==================================

import os
import sys
import inspect
import subprocess
import pkg_resources


# ============================== Build Environment ==============================
# Build behaviour is dependent on environment
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# If building locally, configure path so I don't need to run setup.py install first
if not on_rtd:
    sys.path.insert(0, os.path.abspath('../../'))

# Add path for custom Pygments style
sys.path.append(os.path.abspath('.'))
pygments_style = 'tdk_style.TDKStyle'

# Add path for snippets folder
sys.path.append(os.path.abspath('_snippets'))

# on_rtd = True  # Uncomment for testing RTD builds locally


# ============================ Project information ============================

project = 'InstaTweet'
copyright = '2022, Adam Korn'
author = 'Adam Korn'

# The full version, including alpha/beta/rc tags
# Simplify things by using the version from setup.py
version = pkg_resources.require("insta-tweet")[0].version
release = version


# ======================== General configuration ============================

# Doc with root toctree
master_doc = 'index'  # .rst

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# ============================ Extensions ====================================

# Add any Sphinx extension module names here, as strings
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'myst_parser',
]

if on_rtd:
    # Building on RTD -> Add linkcode links (in addition to viewcode links)
    # This links to the class/method/function on GitHub (with lines highlighted)
    # as another option for viewing source code
    extensions.append('_ext.linkcode')


# ====================== Extra Settings for Extensions ========================

# ~~~~ InterSphinx ~~~~
# Add references to Python, Tweepy, SQLAlchemy docs
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'tweepy': ('https://docs.tweepy.org/en/stable/', None),
    'sqlalchemy': ('https://docs.sqlalchemy.org/en/14/', None)
}

# ~~~~ AutoSectionLabel ~~~~
# Make sure the target is unique
autosectionlabel_prefix_document = True


# ~~~~ Autodoc ~~~~
# Order based on source
autodoc_member_order = 'bysource'
#
# Remove typehints from method signatures and put in description instead
autodoc_typehints = 'description'
#
# Only add typehints for documented parameters (and all return types)
#  ->  Prevents parameters being documented twice for both the class and __init__
#  ->  It does mean everything with a typehint actually needs a docstring tho :/
autodoc_typehints_description_target = 'documented_params'


# ~~~~ MyST Parser ~~~~
# Add narkdown as source -> to include README.md instead of making a README.rst
source_suffix = ['.rst', '.md']


# ============================ HTML Output Settings ============================

# HTML Context
# Add the "Edit on GitHub" link at the top
html_context = {
    'display_github': True,
    'github_user': 'TDKorn',
    'github_repo': 'insta-tweet',
    'github_version': 'docs/docs/source/'
}

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Theme Options
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html#theme-options
#
html_theme_options = {
    # Add the [+] signs to nav
    'collapse_navigation': False,
    # Prev/Next buttons also placed at the top bc it'd be cruel not to
    'prev_next_buttons_location': 'both',
}


# ============================ Linkcode Extension Settings ============================
#
# Keeping linkcode separate from other extension settings since it's only for RTD builds (and long af)
# To be clear: if on_rtd == False, this whole section is skipped and only viewcode is used
#
#
#                  Adapted from https://github.com/nlgranger/SeqTools (ily)
#
#
if on_rtd:
    # Get the blob to link to on GitHub
    linkcode_revision = "master"

    try:
        # lock to commit number
        cmd = "git log -n1 --pretty=%H"
        head = subprocess.check_output(cmd.split()).strip().decode('utf-8')
        linkcode_revision = head

        # if we are on master's HEAD, use master as reference
        cmd = "git log --first-parent master -n1 --pretty=%H"
        master = subprocess.check_output(cmd.split()).strip().decode('utf-8')
        if head == master:
            linkcode_revision = "master"

        # if we have a tag, use tag as reference
        cmd = "git describe --exact-match --tags " + head
        tag = subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')
        linkcode_revision = tag

    except subprocess.CalledProcessError:
        pass

    # Source URL template; formatted + returned by linkcode_resolve
    linkcode_url = "https://github.com/tdkorn/insta-tweet/blob/" \
                   + linkcode_revision + "/{filepath}#L{linestart}-L{linestop}"

    # Hardcoded Top Level Module Path // since InstaTweet isn't PyPi release name :(  it could be tho...
    modpath = pkg_resources.require('insta-tweet')[0].location

    def linkcode_resolve(domain, info):
        """Returns a link to the source code on GitHub, with appropriate lines highlighted

        Adapted from https://github.com/nlgranger (ily)
        """
        if domain != 'py' or not info['module']:
            return None

        modname = info['module']
        fullname = info['fullname']

        submod = sys.modules.get(modname)
        if submod is None:
            print(f'No submodule found for {fullname}')
            return None

        obj = submod
        for part in fullname.split('.'):
            try:
                obj = getattr(obj, part)
                print(obj)
            except Exception:
                print(f'error getting part? obj = {obj}, part = {part})')
                return None

        try:
            filepath = os.path.relpath(inspect.getsourcefile(obj), modpath)
            if filepath is None:
                print(f'No filepath found for {obj} in module {modpath}...?')
                return
        except Exception as e:
            return print(  # ie. None
                f'Exception raised while trying to retrieve module path for {obj}:',
                e, sep='\n'
            )

        try:
            source, lineno = inspect.getsourcelines(obj)
        except OSError:
            print(f'failed to get source lines for {obj}')
            return None
        else:
            linestart, linestop = lineno, lineno + len(source) - 1

        final_link = linkcode_url.format(
            filepath='/'.join(filepath.split('\\')),
            linestart=linestart,
            linestop=linestop
        )
        print(f"Final Link for {fullname}: {final_link}")
        return final_link


# ---- Skip and Setup Method -------------------------------------------------

def skip(app, what, name, obj, would_skip, options):
    """Include __init__ as a documented method"""
    if name in ('__init__',):
        return False
    return would_skip


def setup(app):
    app.connect('autodoc-skip-member', skip)
    app.add_css_file("custom.css")

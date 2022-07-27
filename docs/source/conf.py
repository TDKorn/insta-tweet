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
import pkg_resources

# sys.path.insert(0, os.path.abspath('../../'))
# sys.path.append(os.path.abspath('exts'))

# -- Project information -----------------------------------------------------

project = 'InstaTweet'
copyright = '2022, Adam Korn'
author = 'Adam Korn'

# The full version, including alpha/beta/rc tags
# release = pkg_resources.require("insta-tweet")[0].version
release = "2.0.0b12"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    # 'sphinx.ext.viewcode',
    'sphinx.ext.linkcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'myst_parser',
]
# Make sure the target is unique
autosectionlabel_prefix_document = True

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
html_theme_options = {
    'collapse_navigation': False,  # Add the [+] signs to nav
    'prev_next_buttons_location': 'both',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_context = {
    'display_github': True,
    'github_user': 'TDKorn',
    'github_repo': 'insta-tweet',
    'github_version': 'docs/docs/source/'
}

# html_show_sourcelink = True


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

# ---- MyST Parser Settings ---------------------------------------------------
#
source_suffix = ['.rst', '.md']

# ---- Linkcode Extension Settings ---------------------------------------------------
#

import subprocess
import inspect


# linkcode_revision = "master"

# try:
#     # lock to commit number
#     cmd = "git log -n1 --pretty=%H"
#     head = subprocess.check_output(cmd.split()).strip().decode('utf-8')
#     linkcode_revision = head
#
#     # if we are on master's HEAD, use master as reference
#     cmd = "git log --first-parent master -n1 --pretty=%H"
#     master = subprocess.check_output(cmd.split()).strip().decode('utf-8')
#     if head == master:
#         linkcode_revision = "master"
#
#     # if we have a tag, use tag as reference
#     cmd = "git describe --exact-match --tags " + head
#     tag = subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')
#     linkcode_revision = tag
#
# except subprocess.CalledProcessError:
#     pass



linkcode_revision = 'docs'
linkcode_url = "https://github.com/tdkorn/insta-tweet/blob/" \
               + linkcode_revision + "/{filepath}#L{linestart}-L{linestop}"

# print(m := pkg_resources.require('insta-tweet')[0].location)
# x = InstaTweet.TweetClient.upload_media
# print(filepath := os.path.relpath(inspect.getsourcefile(x), m))

# modpath = pkg_resources.require(topmodulename)[0].location
modpath = pkg_resources.require('insta-tweet')[0].location  # Since InstaTweet is pkg name not folder name? idk...


def linkcode_resolve(domain, info):
    if domain != 'py' or not info['module']:
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        print("submod is none")
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
            print(f'No Filepath? modpath = {modpath}')
            return
    except Exception:
        print(f'No filepath?? obj -> {obj} modpath -> {modpath}')
        return None

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
    print(f"Final Link for {info['fullname']}:", final_link)
    return final_link


# ---- Skip and Setup Method -------------------------------------------------
def skip(app, what, name, obj, would_skip, options):
    """Include __init__ as a documented method"""
    if name in ('__init__',):
        return False
    return would_skip


def setup(app):
    app.connect('autodoc-skip-member', skip)
    app.add_css_file("property.css")  # To prevent horizontal stacking in RTD

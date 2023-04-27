# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# List of Options from RTD:
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
#

# ================================== Imports ==================================

import os
import re
import sys
import pkg_resources
import sphinx_github_style

# ============================== Build Environment ==============================
# Build behaviour is dependent on environment
on_rtd = os.environ.get('READTHEDOCS') == 'True'

if not on_rtd:
    sys.path.insert(0, os.path.abspath('../../'))

sys.path.append(os.path.abspath('.'))

# Use default Pygments style if not HTML
if 'html' not in sys.argv:
    pygments_style = 'sphinx'

# on_rtd = True  # Uncomment for testing RTD builds locally


# ============================ Project information ============================

project = 'InstaTweet'
copyright = '2022, Adam Korn'
author = 'Adam Korn'
repo = "insta-tweet"

# Simplify things by using the installed version
pkg = pkg_resources.require(repo)[0]
version = pkg.version
release = version


# ======================== General configuration ============================

# Doc with root toctree
master_doc = 'contents'  # .rst

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

# Source File type
source_suffix = '.rst'

# LaTeX settings
latex_elements = {          # Less yucky looking font
    'preamble': r'''
\usepackage[utf8]{inputenc}
\usepackage{charter}
\usepackage[defaultsans]{lato}
\usepackage{inconsolata}
''',  # Change Background of Code Blocks
   # 'sphinxsetup': """
# VerbatimColor={RGB}{13,17,23},
# """,
}

# ============================ Extensions ====================================

# Add any Sphinx extension module names here, as strings
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'sphinx_github_style',
    'sphinx_sitemap',
]


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


# ~~~~~~~~ My Own Thing (replace_autodoc_refs_with_linkcode) ~~~~~~~~~
#
# Directory to save temp .rst file to while docs building
#
if on_rtd:
    rst_build_dir = os.path.abspath('../_build/')
else:
    rst_build_dir = os.path.abspath('../build/')
#
#
# Source file to convert for GitHub README/PyPi description
#
rst_src = os.path.abspath('_readme/about-instatweet.rst')
#
# File to save the final converted output to
#
rst_out = os.path.abspath('../../README.rst')  # Root of the repository
#
# [Optional] dict of {'ref': 'external_link'} to replace relative links
# like :ref:`ref` with an `ref <external_link>`_ (ex. for PyPi)
#
rst_replace_refs = {
    'mandatory-settings': 'https://instatweet.readthedocs.io/en/latest/_readme/getting-started.html#mandatory-settings',
}


# ============================ HTML Theme Settings ============================

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

# Set the "Edit on GitHub" link to use the current commit
html_context = {
    'display_github': True,
    'github_user': 'TDKorn',
    'github_repo': repo,
}

if not on_rtd:
    site_url = "https://tdkorn.github.io/insta-tweet/"

html_baseurl = "https://instatweet.readthedocs.io/en/latest/"

sitemap_url_scheme = "{link}"


# ~~~~ Sphinx GitHub Style ~~~~
#
# Top level package name
top_level = pkg.get_metadata("top_level.txt").strip()

# Blob to use when linking to GitHub source code
if on_rtd:
    linkcode_blob = 'last_tag'
else:
    # For gh-pages use master
    linkcode_blob = 'master'

# Text to use for the linkcode link
linkcode_link_text = "View on GitHub"

# Source URL template; formatted + returned by linkcode_resolve
linkcode_url = sphinx_github_style.get_linkcode_url(linkcode_blob, html_context)


# Use default linkcode_resolve function to generate links for rst ref replacements
linkcode_func = sphinx_github_style.get_linkcode_resolve(linkcode_url)


def linkcode_resolve(domain, info):
    final_link = linkcode_func(domain, info)
    replace_autodoc_refs_with_linkcode(
        info=info,
        link=final_link,
        rst_src=rst_src,
    )
    return final_link


def replace_autodoc_refs_with_linkcode(info: dict, link: str, rst_src: str):
    """Replaces Sphinx autodoc cross-references in a .rst file with linkcode links to highlighted GitHub source code

    Essentially turns your GitHub README into Sphinx-like documentation contained fully within the repository


    =================================  By https://github.com/TDKorn  =====================================


    For example, :meth:`~.InstaClient.get_user` would be rendered in HTML as an outlined "get_user()" link
    that contains an internal reference to the corresponding documentation entry (assuming it exists)

    We love it, it's great. Fr. But it's ugly and useless on GitHub and PyPi. Literally so gross.

    This function replaces cross-references in the ``rst_src`` file with the links generated by linkcode,
    which take you to the source file and highlight the full definition of the class/method/function/target

    .. note:: links are of the format https://github.com/user/repo/blob/branch/package/file.py#L30-L35

        For example,
        `get_user() <https://github.com/TDKorn/insta-tweet/blob/docs/InstaTweet/instaclient.py#L42-L64>`_


    :param info: the info dict from linkcode_resolve
    :param link: link to the highlighted GitHub source code, generated by linkcode
    :param rst_src: the .rst file to use as the initial source of content
    """
    if not rst_src.endswith('.rst'):
        raise TypeError

    # On the first function call that actually replaces a cross-reference with a link,
    # the content from ``rst_src`` is copied and saved to a temporary rst file in ``rst_build_dir``
    #
    # All function calls afterwards will use this temp file as the source and output file
    # When the build completes, it will be moved to the specified ``rst_out`` location
    #
    rst_temp = os.path.join(rst_build_dir, os.path.basename(rst_src))

    # If the temp output file already exists, use it as the source, since
    # the content from ``rst_src`` is already copied to it (and possibly edited)
    if os.path.exists(rst_temp):
        rst_src = rst_temp

    else:
        # If not, it's the first function call. It needs to be created
        rst_src = os.path.abspath(rst_src)

        # And if the rst build directory doesn't exist, create it too
        if not os.path.exists(rst_build_dir):
            os.mkdir(rst_build_dir)

    # Read in the rst
    rst = read(rst_src)

    # Use the linkcode data that was provided to see what the reference target is
    # Ex:  Class.[method] // module.[function] // [function]
    ref_name = info['fullname'].split('.')[-1]

    # The rst could have :meth:`~.method` or :meth:`~.Class.method` or :class:`~.Class` or...
    # Regardless, there's :directive:`~[].target` where [] is optional
    pattern = rf":\w+:`~\.?\w?\.{ref_name}`"

    # See if there's any reference in the rst, and figure out what it is
    if match := re.findall(pattern, rst):
        directive = match[0].split(':')[1]
    else:
        print('No references found for', ref_name)
        return None

    # Format the name of methods
    if directive == 'meth':
        ref_name += "()"

    # Format the link -> `method() <https://www.github.com/.../file.py#L10-L19`_
    rst_link = f"`{ref_name} <{link}>`_"

    # Then take the link and sub that hoe in!!
    subbed_rst = re.sub(pattern, rst_link, rst)

    # Save to the temp build rst file
    with open(rst_temp, 'w', encoding='utf-8') as f:
        f.write(subbed_rst)

    print(f'Added reST links for {ref_name}: {rst_link}')
    return {'info': info, 'rst_link': rst_link}


# ---- Methods for "build-finished" Core Event ----------------------

def read(file):
    with open(file, 'r', encoding='utf-8') as f:
        return u'{}'.format(f.read())


def replace_rst_refs(rst: str, refs: dict) -> str:
    """Post-processes the generated rst, replacing :ref: with external links (ex. for PyPi)

    :param rst: the text of the .rst file
    :param refs: dict of {'reference': 'external_link'}
    :return: the processed rst text
    """
    for ref, external_link in refs.items():
        rst = re.sub(
            pattern=rf":ref:`{ref}`",
            repl=f"`{ref} <{external_link}>`_",
            string=rst
        )
    return rst


def replace_rst_images(rst: str) -> str:
    """Post-processes the generated rst, replacing relative image paths with external RTD links

    Probably temporary until I write a proper function that adjusts the paths when moving to ``rst_out``

    :param rst: the text of the .rst file
    :return: the processed rst text
    """
    return re.sub(
        # .. image:: {..}/_static/(filename.ext)
        pattern=r".. image:: \S+_static/(\w+\.\w{3,4})",
        repl=r".. image:: https://instatweet.readthedocs.io/en/latest/_images/\1",
        string=rst
    )


def move_generated_rst_file(app, exception):
    """Moves the generated rst file from ``rst_temp`` to ``rst_out``"""
    built_rst = os.path.join(
        rst_build_dir, os.path.basename(rst_src)
    )
    if os.path.exists(built_rst):
        rst = replace_rst_images(
            rst=read(built_rst)
        )
        if rst_replace_refs:
            rst = replace_rst_refs(
                rst, refs=rst_replace_refs
            )
        with open(rst_out, 'w', encoding='utf-8') as f:
            f.write(rst)

        return print(
            f'Moved generated .rst file from {built_rst} to {rst_out}'
        )
    if exception:
        return print(
            "Build .rst file not found in build dir, exception raised:",
            exception, sep='\n'
        )
    return print('.rst file not generated, no exception was raised')


# ---- Skip and Setup Method -------------------------------------------------

def skip(app, what, name, obj, would_skip, options):
    """Include __init__ as a documented method but allow InstaClient to override it"""
    if name in ('__init__',):
        if not obj.__qualname__.startswith("InstaClient"):
            return False
    return would_skip


def setup(app):
    app.connect('autodoc-skip-member', skip)
    app.connect('build-finished', move_generated_rst_file)
    app.add_css_file("custom.css")

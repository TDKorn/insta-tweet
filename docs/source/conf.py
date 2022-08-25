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
import shutil
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

# For replace_rst_py_directives_with_linkcode
rst_src = os.path.abspath('_readme/about-instatweet.rst')
rst_out = os.path.abspath('../../README.rst')

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
        replace_rst_py_directives_with_linkcode(
            info, final_link, rst_src, rst_out
        )
        return final_link


    def replace_rst_py_directives_with_linkcode(info: dict, link: str, rst_src: str, rst_out: str):
        """Uses linkcode to replace Python domain Sphinx directives with linkcode links to GitHub source code

        This can turn your GitHub README into documentation that's "self-contained" within your GitHub repo


        =================================  By https://github.com/TDKorn  =====================================


        :param info: dict from linkcode_resolve
        :param rst_src: the .rst file to use as the initial source of content
        :param rst_out: the .rst file to write the output to

        .. admonition:: Example

            In HTML, :meth:`~.InstaClient.get_user` would render as an outlined "get_user()" link,
            which takes you to the corresponding documentation entry (assuming it exists)

            We love it, it's great. But it's ugly and useless in the rst file on GitHub.

            This function replaces the Python domain Sphinx directives with a similar
            appearing link, but it takes you to the file on GitHub and highlights the
            full class/method/function definition, thanks to linkcode :)


        .. note:: links are of the format https://github.com/user/repo/blob/branch/package/file.py#L30-L35

            For example,
            `get_user() <https://github.com/TDKorn/insta-tweet/blob/docs/InstaTweet/instaclient.py#L42-L64>`_

        """
        if not rst_src.endswith('.rst'):
            raise TypeError

        # On the first function call that actually replaces a directive with a link,
        # the content from rst_src is copied and saved to a temporary rst file in build/rst

        # All function calls afterwards will use this temp file as the source and output file
        # When the build completes, it will be moved to the specified rst_out location

        build_dir = os.path.abspath('../build/rst')
        rst_temp = os.path.join(build_dir, os.path.basename(rst_src))

        # If the temp output file already exists, use it as the source, since
        # the content from rst_src is already copied to it (and possibly edited)
        if os.path.exists(rst_temp):
            rst_src = rst_temp

        else:
            # If not, it's the first function call. It needs to be created
            rst_src = os.path.abspath(rst_src)

            # And if the rst build directory doesn't exist, create it too
            if not os.path.exists(build_dir):
                os.mkdir(build_dir)

        # Read in the rst
        with open(rst_src, 'r') as rst_file:
            rst = rst_file.read()

        # Use the linkcode data that was provided to see what the reference target is
        # Ex:  Class.[method] // module.[function] // [function]
        ref_name = info['fullname'].split('.')[-1]

        # The rst could have :meth:`~.method` or :meth:`~.Class.method` or :class:`~.Class` or...
        # Regardless, there's :directive:`~[].target` where [] is optional
        pattern = f":.+:`~.*\\.{ref_name}`"

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
        with open(rst_temp, 'w') as f:
            f.write(subbed_rst)

        print(f'Added reST links for {ref_name}: {rst_link}')
        return True


# ---- Skip and Setup Method -------------------------------------------------

def skip(app, what, name, obj, would_skip, options):
    """Include __init__ as a documented method"""
    if name in ('__init__',):
        return False
    return would_skip


def move_readme(app, exception):
    build_dir = os.path.abspath('../build/rst')
    rst_build = os.path.join(build_dir, os.path.basename(rst_src))

    if os.path.exists(rst_build):
        shutil.move(rst_build, rst_out)
        return print(
            'Moved README from ', rst_build, 'to', rst_out
        )
    if exception:
        return print(
            "README not found in build dir... exception:",
            exception, sep='\n'
        )
    return print('Failed to build README, but no exception was raised...')


def setup(app):
    app.connect('autodoc-skip-member', skip)
    app.connect('build-finished', move_readme)
    app.add_css_file("custom.css")

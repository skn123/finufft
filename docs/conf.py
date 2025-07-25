# -*- coding: utf-8 -*-
#
# finufft documentation build configuration file, created by
# sphinx-quickstart on Wed Nov  1 16:19:13 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import sphinx.ext.autodoc

# autodoc py module stuff...

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../python/finufft'))
sys.path.insert(0, os.path.abspath('../python/cufinufft'))

# quash sphinx's inevitable failure of C++ lib extension to import...
autodoc_mock_imports = ['finufft._finufft', 'numpy', 'pycuda', 'cufinufft._cufinufft']
# The above is not enough for nested import -- forcibly mock them out ahead of time:
#for name in autodoc_mock_imports:
#    sys.modules[name] = sphinx.ext.autodoc._MockModule(name, None)
# (removed the above since broke in sphinx 1.6 -> 1.7.4). Thanks Dylan.


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.6'   # dylan
needs_sphinx = '1.3'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
#    'sphinx.ext.autosectionlabel',   # needs v 1.4; can :ref: other files w/o this; removed 7/29/18
    'texext',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = {'.rst': 'restructuredtext'}

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'finufft'
copyright = u'2017-2025 The Simons Foundation, Inc. - All Rights Reserved'
author = u'Alex Barnett, Ludvig af Klinteberg, Joakim Andén, Libin Lu, Jeremy Magland, Andrea Malleo, Yu-Hsuan Shih, Marco Barbone, Robert Blackwell, and others.'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'2.4'
# The full version, including alpha/beta/rc tags.
release = u'2.4.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# Prevent readthedocs from highlighting :: blocks as py:
# https://stackoverflow.com/questions/44376893/selectively-disable-readthedocs-syntax-highlighting
highlight_language = 'none'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files (.rst only)
exclude_patterns = ['_build', 'overview_meat']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'alabaster'
html_theme = 'classic'
#html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}
#html_theme_options = {"codebgcolor":"rgb(240,240,240)"}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = 'logo-small.png'

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# web browser icon. see SO: https://stackoverflow.com/questions/54639192/change-the-favicon-of-the-sphinx-read-the-docs-theme
html_favicon = 'logo-32x32.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {'**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'] }

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = False

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'finufftdoc'

# To fix location of equation numbering. Barnett tried 6/19/18
# see https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/
def setup(app):
    app.add_css_file('theme_overrides.css')
# it doesn't fail if this file not found in _static  :(




# -- Options for LaTeX output ---------------------------------------------

# My problem with chapters wrongly numbered:
# https://stackoverflow.com/questions/60877841/how-can-i-force-sphinx-to-end-a-chapter-when-making-a-pdf
# .. ?

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
'pointsize': '10pt',

# removes blank pages:
'classoptions': ',openany,oneside',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
'preamble': r'''
  \usepackage{hyperref}
  \setcounter{tocdepth}{3}
''',

# Latex figure (float) alignment
#'figure_align': 'htbp',

# prevent any index from being made (Komiya):
# https://groups.google.com/g/sphinx-users/c/Pn3uHevtR28
'makeindex': '',
'printindex': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('latexindex', 'finufft.tex', u'FINUFFT Documentation',
     'Alex Barnett and the FINUFFT team', 'manual',False),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = 'logo.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
latex_domain_indices = False

# this doens't stop a latex index... :(
latex_use_modindex = False




# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'finufft', u'FINUFFT Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'finufft', u'FINUFFT Documentation',
     author, 'FINUFFT nonuniform FFT', 'Nonuniform FFT of types 1,2,3 in dimensions 1,2,3',
     'Numerical methods'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False

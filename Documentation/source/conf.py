# -*- coding: utf-8 -*-
#
# The Garden Group Genetic Algorithm for Clusters documentation build configuration file, created by
# sphinx-quickstart on Mon Oct  1 08:10:30 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
print('You are in '+str(os.getcwd()))

#PACKAGE_PARENT = '../../GA'
#SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
#sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
#import pdb; pdb.set_trace()
#sys.path.insert(0, os.path.abspath('../../GA'))
#original_path = os.getcwd()
#os.chdir('../../GA')
#import pdb; pdb.set_trace()

#import GA.Diversity_Schemes.CNA_Diversity_Scheme
#import GA.Diversity_Schemes.Energy_Diversity_Scheme

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
from os.path import expanduser
home = expanduser("~")
print('home = '+str(home))
#plantuml = 'java -jar '+str(home)+'/plantuml/plantuml.1.2018.11.jar'
extensions = ['sphinx.ext.autodoc','sphinx.ext.githubpages','sphinx.ext.napoleon','sphinx.ext.mathjax','sphinx.ext.graphviz','sphinx_tabs.tabs','sphinxcontrib.plantuml'] #,'sphinxcontrib.plantuml','sphinxtogithub'] #,'sphinx.ext.imgmath']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['GA_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
from Organisms import __author__
project = u'Organisms: A Genetic Algorithm for Nanoclusters'
copyright = u'2021, '+__author__
author = u''+__author__

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
from Organisms import __version__
def get_version_number():
    version = __version__
    return version
version = get_version_number()
if '.' in version:
    release = version.split('.', 1)[0]
else:
    release = '0'

#release = '2' #path.split('/')[-4].replace('OGA_v','')
# The full version, including alpha/beta/rc tags.
#version = '3.4' # '.'.join(release.split('.')[0:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Viewing page source link
#html_show_sourcelink = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = 'Images/Gnome_House.jpg'
#html_theme_path = ["themes"]
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': False,
    #'vcs_pageview_mode': 'blob',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}
# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'Images/gnome.png'

"""
html_theme = "classic"
html_theme_options = {
    "rightsidebar": "false",
    "relbarbgcolor": "black"
}
"""

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['GA_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#

# -- Options for Theme output ---------------------------------------------

import re

def process_docstring(app, what, name, obj, options, lines):
    spaces_pat = re.compile(r"( {8})")
    ll = []
    for l in lines:
        ll.append(spaces_pat.sub("    ",l))
    lines[:] = ll

#try:
#    from docutils.parsers.rst import directives
#    from source.youtube_video import Youtube
#    youtube_method_imported_successfully = True
#except:
#    #from youtube_video import Youtube
#    extensions.append('sphinxcontrib.youtube')
#    youtube_method_imported_successfully = True
def setup(app):
    app.add_css_file('my_theme.css')
    #if youtube_method_imported_successfully:
    #    directives.register_directive('youtube', Youtube)
    #app.add_stylesheet('my_theme.css')
    #app.connect('autodoc-process-docstring', process_docstring)
    #from sphinx.highlighting import lexers
    #from pygments.lexers import PythonLexer
    #lexers['python'] = PythonLexer(tabsize=2)
    #from sphinx.highlighting import lexers 
    #from pygments.lexers.compiled import PythonLexer 
    #from pygments.filters import VisibleWhitespaceFilter 
    #myLexer = PythonLexer() 
    #myLexer.add_filter(VisibleWhitespaceFilter(spaces='!')); 
    #app.add_lexer('python', myLexer);

#html_style = 'GA_static/my_theme.css' 

html_show_copyright = True

html_show_sphinx = True
'''
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}
'''


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Organismsdocs'

# -- Options for LaTeX output ---------------------------------------------

# inside conf.py
latex_engine = 'pdflatex'
latex_elements = {
    'fontpkg': r'''
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
''',
    'preamble': r'''
\usepackage[titles]{tocloft}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
''',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
    'printindex': r'\footnotesize\raggedright\printindex',
}
latex_show_urls = 'footnote'

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Organisms.tex', u'The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity Documentation',
     u'Geoffrey Weal', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'Organisms', u'The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Organisms', u'The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity Documentation',
     author, 'Organisms', 'This program is designed to perform the genetic algorithm in search of the global minimum nanocluster.',
     'Research'),
]




# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

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

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

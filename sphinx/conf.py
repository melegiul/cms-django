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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os
import sys
import django
sys.path.insert(0, os.path.abspath('../src/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()

# -- Project information -----------------------------------------------------

project = 'integreat-cms'
copyright = '2020, Integreat'
author = 'Integreat'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.coverage',
        'sphinxcontrib_django',
        'sphinx_rtd_theme',
        ]

intersphinx_mapping = {
        'http://docs.python.org/': None,
        'https://docs.djangoproject.com/en/stable': 'https://docs.djangoproject.com/en/stable/_objects',
}
# Add any paths that contain templates here, relative to this directory.
# templates_path = ['templates']
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = []

# Do not include source in build
html_show_sourcelink = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
        'logo_only': True
}

html_favicon = '../src/cms/static/images/favicon.ico'
html_logo = '../src/cms/static/images/integreat-logo-white.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['static']

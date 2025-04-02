# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "py-cidr"
copyright = '2024-present, Gene C'
author = 'Gene C'
release = '2.8.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'autoapi.extension']

autoapi_dirs = ['../src/py_cidr']
autoapi_options = ['members', 'show-module-summary']
autoapi_keep_files = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

def skip_submodules(app, what, name, obj, skip, options):
    skip = True
    if name == 'py_cidr' or \
        name.startswith('py_cidr.Cidr') or name.startswith('py_cidr.CidrMap') or \
        name.startswith('py_cidr.CidrFile') or name.startswith('py_cidr.CidrCache') :
        skip = False

    if what == 'method' and name.endswith('__init__'):
        skip = True

    if what == 'attribute':
        skip = True

    #print(f'skip={skip} what={what} name={name}')
    return skip

def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_submodules)


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

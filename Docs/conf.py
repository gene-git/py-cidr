# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "py-cidr"
copyright = '2024-present, Gene C'
author = 'Gene C'
release = '3.5.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'autoapi.extension']

autoapi_dirs = ['../src/py_cidr']
autoapi_ignore = ['_*']
autoapi_options = ['members']
autoapi_member_order = 'alphabetical'
autoapi_python_use_implicit_namespaces = True
add_module_names = False
autoapi_keep_files = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '_*']

def skip_submodules(app, what, name, obj, skip, options):
    #skip = True
    if 'cidr_types' in name:
        skip = False
    return skip

def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_submodules)


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
#html_static_path = ['_static']

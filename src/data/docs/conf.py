#
# Docs/conf.py
#
import os
import sys

#
# The source code
#
sys.path.insert(0, os.path.abspath("../.."))

#
# package version
#
def read_version() -> str:
    """
    Get package version from version.txt file
    """
    file = '../../version.txt'
    if os.path.exists(file):
        with open(file, 'r') as fob:
            proj_vers = fob.readlines()[0]
    else:
        proj_vers = '0.1.0-unknown'
    return proj_vers


project = "py-cidr"
copyright = '2024-present, Gene C'
author = 'Gene C'
release = read_version()

extensions = [
        'sphinx.ext.autodoc', # 'autoapi.extension'
        'sphinx.ext.napoleon',
        'sphinx.ext.imgconverter',
        ]

# handle google style until we switch to standard sphinx 
# napoleon_google_docstring = True
# napoleon_numpy_docstring = False

latex_engine = 'xelatex'
latex_use_xindy = True

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '11pt',

    #
    # Font settings
    # Adjust the font size of code blocks.
    #
    'fvset': r'\fvset{fontsize=\scriptsize}',

    'fontpkg': r'''
        \usepackage{fontspec}

        %
        % Fonts for : body (sans), headers (sans) and mono
        %
        \setmainfont{Source Sans 3}[Ligatures=TeX]
        \setsansfont{Source Sans 3}[Ligatures=TeX]
        \setmonofont{Source Code Pro}
    ''',


    'preamble': r'''
    \usepackage{parskip}

    %
    % Fix the 11pt headheight layout warnings
    %
    \setlength{\headheight}{14pt}
    \addtolength{\topmargin}{-2pt}


    %
    % List items vertical spacing
    %
    \usepackage{enumitem}
    \setlist[itemize]{
        noitemsep,
        topsep=6pt,             % \parskip,       % 0pt,
        parsep=0pt,
        partopsep=0pt,
        after=\vspace{0pt}
        }
    \setlist[enumerate]{
        noitemsep,
        topsep=6pt,             % 0pt,
        parsep=0pt,
        partopsep=0pt,
        after=\vspace{0pt}
        }

    \usepackage{newunicodechar}
    %\newunicodechar{␣}{\space}
    \newunicodechar{␣}{\textvisiblespace}
    \tracinglostchars=0

    ''',
}


latex_documents = [
    (
        'index',
        'py-cidr.tex',
        'py-cidr Reference Documentation',
        'Gene C',
        'manual'
    ),
]

# ===============================
# HTML Configuration & Stylesheets
# ===============================
html_theme = 'sphinx_rtd_theme'  # Works exactly the same if using 'furo' or 'alabaster'
html_static_path = ['_static']
html_css_files = [ 'custom.css',]


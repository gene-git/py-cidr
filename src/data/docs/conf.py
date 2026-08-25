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
napoleon_google_docstring = True
napoleon_numpy_docstring = False

latex_engine = 'xelatex'
latex_use_xindy = True

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',

    # Protrusion only to prevent XeLaTeX font expansion crashes
    'passoptionstopackages': r'\PassOptionsToPackage{protrusion=true}{microtype}',


    #'fontpkg': ''
    #'fontvars': '',

    'preamble': r'''
    \usepackage{microtype}
    \usepackage{parskip}
    \usepackage{fontspec}


    \usepackage{newunicodechar}
    %\newunicodechar{␣}{\space}
    \newunicodechar{␣}{\textvisiblespace}
    \tracinglostchars=0

    % Body Serif (Libertine)
    \setmainfont{Libertinus Serif}[
        Ligatures=TeX,
        Numbers=OldStyle
    ]

    % Section Headers (Sans-Serif libertine)
    \setsansfont{Libertinus Sans}[
        Ligatures=TeX
    ]

    % Verbatim/Inline (Monospace libertine)
    % Explicitly mapping it as the primary system typewriter engine (\ttdefault)
    \setmonofont{Libertinus Mono}[
        Scale=0.92,
        AutoFakeSlant=0.2
    ]

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

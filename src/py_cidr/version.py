# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Project py-cidr
This file is auto updated by git-release
"""
__version__ = "2.6.0"
__date__ = "2025-01-18"
__reldev__ = "release"
__githash__ = 'none'

def version() -> str:
    """ report version and release date """
    vers = f'py-cidr: version {__version__} ({__date__} commit {__githash__})'
    return vers

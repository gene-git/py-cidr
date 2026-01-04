# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
Project py-cidr
This file is auto updated by git-release
"""
__version__ = "3.10.0"
__date__ = "2025-09-01"
__reldev__ = "release"


def version() -> str:
    """ report version and release date """
    vers = f'py-cidr: version {__version__} ({__date__})'
    return vers

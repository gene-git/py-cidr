# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
Project py-cidr
This file is auto updated by git-release
"""
__version__ = "5.0.0"
__date__ = "2026-08-25"
__reldev__ = "release"


def version() -> str:
    """ report version and release date """
    vers = f'py-cidr: version {__version__} ({__date__})'
    return vers

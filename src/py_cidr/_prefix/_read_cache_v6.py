# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Convert old to new cache
"""
import pickle
from pickle import PickleError
from pytricia import PyTricia

class Version6:
    def __init__(self):
        self.ipv6: bool = False
        self.prefixlen = 32
        self.pyt: PyTricia = PyTricia(128)
        self.vers: str = 'v6'
        self.compact: bool = False

def read_cache_v6(file: str) -> PyTricia | None:
    """
    Read cache filr from version 6
    """
    old: Version6 | None = None

    try:
        with open(file, 'rb') as fob:
            old = pickle.load(fob)

    except (OSError, PickleError) as err:
        print(f' Error reading cidr cache: {err}')
        return False

    except (ModuleNotFoundError) as err:
        print(f' Unsupported cache - please make new cache: {err}')
        return False

    if old is None or old.pyt is None:
        return None

    return old.pyt

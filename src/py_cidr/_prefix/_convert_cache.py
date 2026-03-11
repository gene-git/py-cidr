# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Convert old to new cache
"""
from typing import Any

from pytricia import PyTricia

from py_cidr import ip_version 
from py_cidr import PrefixVal 
from py_cidr import IPvxNetwork



class OldElem:
    """ Original cache element """
    def __init__(self):
        self.net: IPvxNetwork
        self.val: Any


class Cachev3:
    """ v2 cache class """
    def __init__(self):
        self.vers: str = 'v3'
        self.compact: bool = False
        self.elems: list[OldElem] = []


def convert_cache_v2(old_elems: list[OldElem]) -> PyTricia:
    """
    Old cache is a list of elemnts
    Each element instance contains:
    - elem.net
    - elem.val
    New cache is a list of tuple(net, val)
    Sort to be sure order is correct after coverting.
    """
    cidr_vals: list[PrefixVal] = []
    cidr_vals = [(str(elem.net), elem.val) for elem in old_elems]

    v6: bool = bool(ip_version(old_elems[0].net) == 6)
    prefixlen = 128 if v6 else 32

    pyt: PyTricia = PyTricia(prefixlen)

    for (cidr, val) in cidr_vals:
        pyt[cidr] = val

    return pyt


def convert_cache_v3(cache_v3: Cachev3) -> PyTricia:
    """
    Old v3 cache is a class with a list of v2 elements
    Each element instance contains:
    - elem.net
    - elem.val
    same as v2. Only difference is v3 has the class instance 
    - vers
    - compact
    - elems
    """
    return convert_cache_v2(cache_v3.elems)

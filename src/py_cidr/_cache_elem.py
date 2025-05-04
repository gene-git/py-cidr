# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2024-present  Gene C <arch@sapience.com>
"""
Each element in cache holds the key value pair.

key = network
value = whatever is associated with the key.
"""
# pylint: disable=too-few-public-methods
from typing import (Any, Self)
from .cidr_types import (IPvxNetwork)


class CidrCacheElem:
    """
    Cache Element has (net, val).
    net is a network represented as IPvxNetwork
    and val can be Any
    """
    def __init__(self):
        self.net: IPvxNetwork
        self.val: Any

    def print(self):
        """ print values """
        net_str = str(self.net)
        val_str = str(self.val)
        print(f'{net_str:>20s}: {val_str}')

    def is_equal(self, elem: Self):
        """
        Args:
            elem (CidrCacheElem)

        Returns:
            bool:
            True if elem has same net/val
        """
        is_same = self.net == elem.net and self.val == elem.val
        return is_same

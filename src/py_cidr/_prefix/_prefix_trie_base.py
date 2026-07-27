# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Base Class for CidrCacheData
- uses patricia trie tree vai PyTricia module.
"""
from typing import Any
import os
import io
import pickle
from pickle import (PickleError)

from patricia26 import Patricia26
from pytricia import PyTricia

from py_cidr._utils import write_file_atomic
from ._read_cache_v6 import read_cache_v6


class PrefixTrieBase:
    """
    A Patricia Trie maps prefixes to values 
    i.e. it holds (prefix, val) pairs. The prefix lives as tree node
    and the value is stored in the node.

    By default the trie is full - all prefixes are kept.

    If initialized with 'compact' set to True, then we keep
    the trie as compact as possible. If (prefix, val) exists
    in trie either exactly or if the parent prefix has the same val,
    then it is not inserted.  Similarly, if a newly added prefix, val
    has children for which prefix is a supernet and has the same "val", 
    those children are then removed from the trie.
    """
    def __init__(self, compact: bool = False, ipv6: bool = False):
        """
        Data, "pyt" is a prefix trie (PATRICIA trie) where
        each prefix holds some value.
        Can think of it as a collection of (prefix: str, val: Any) pairs.
          prefix is string: ip-address / prefixlen
          val is Any

        The prefix len in trie is 32 for ipv4 and 128 for ipv6.

        dirty tracks if changes made - used by prefix_map::save_cache_file()
        write_cache_file always writes the file.
        """
        self.ipv6: bool = ipv6
        self.prefixlen: int = 128 if ipv6 else 32
        self.pyt: Patricia26 = Patricia26()
        self.vers: str = 'v7'
        self.compact: bool = compact

    def freeze(self):
        """
        When using patricia trie to only do lookups (read only)
        It is faster if frozen. See thaw().
        """
        self.pyt.freeze()

    def thaw(self):
        """
        When modifying the patricia trie it must be thawed.
        See freeze()
        """
        self.pyt.thaw()

    def read_cache_file(self, file: str) -> bool:
        """
        Read data from cache file.
        We package our own data together with the tree
        This approach makes it very siumple if ever need to
        change cache version as we have a dictionary payload.
        """
        if not (file and os.path.exists(file)):
            # nothing to do not an error
            return True

        with open(file, 'rb') as fob:
            payload = pickle.load(fob)

        if not isinstance(payload, dict):
            # try reading version v6 pytricia file and convert
            if not self._read_cache_file_v6(file):
                return False
            return True

        # Our data
        self.ipv6 = payload.get('ipv6', self.ipv6)
        self.prefixlen = payload.get('prefixlen', self.prefixlen)
        self.vers = payload.get('vers', self.vers)
        self.compact = payload.get('compact', self.compact)

        # Now the tree
        tree_bytes = payload.get('pyt')
        if tree_bytes:
            with io.BytesIO(tree_bytes) as fob:
                 self.pyt.load_from_file(fob)

        return True

    def write_cache_file(self, file: str) -> bool:
        """
        Write pickled cache file.
        Args:
            file (str):
            File to write to

        Returns:
            bool:
            Success or failure.
        """
        self.pyt.freeze()
        with io.BytesIO() as fob:
            self.pyt.dump_to_file(fob)
            tree_bytes = fob.getvalue()

        # build the payload dictionary
        payload = {
            'ipv6': self.ipv6,
            'prefixlen': self.prefixlen,
            'vers': self.vers,
            'compact': self.compact,
            'pyt': tree_bytes
        }

        with open(file, 'wb') as fob:
            pickle.dump(payload, fob, protocol=pickle.HIGHEST_PROTOCOL)

        self.pyt.thaw()
        return True

    def _read_cache_file_v6(self, file: str) -> bool:
        """
        Attempt to read older cache
        """
        tree = read_cache_v6(file)
        if tree is None:
            return False
        #
        # Conver to new
        #
        for pfx in list(tree):
            self.pyt[pfx] = tree.get(pfx)

        return True
 

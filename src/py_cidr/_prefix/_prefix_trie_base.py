# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Base Class for CidrCacheData
- uses patricia trie tree vai PyTricia module.
"""
import os
from typing import Any
import pickle
from pickle import (PickleError)

from pytricia import PyTricia

from py_cidr._utils import write_file_atomic

from ._convert_cache import (convert_cache_v3, convert_cache_v2)


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
        self.pyt: PyTricia = PyTricia(self.prefixlen)
        self.vers: str = 'v6'
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
        Caller responsible for locks etc
        """
        if not (file and os.path.exists(file)):
            # nothing to do not an error
            return True

        #
        # Version pickle files:
        # v2 Saves list of elem instances
        # v3 Saves CidrCacheDataBase instance
        # v4 - abandoned too slow used sortedcontainers
        # v6 - This version using patricia trie.
        #
        # Assume its prefix_trie unless we discover
        # it is older version below - then converted.
        #
        prefix_trie: PrefixTrieBase | None = None

        try:
            with open(file, 'rb') as fob:
                data = fob.read()
                if data:
                    prefix_trie = pickle.loads(data)

        except (OSError, PickleError) as err:
            print(f' Error reading cidr cache: {err}')
            return False

        except (ModuleNotFoundError) as err:
            print(f' Unsupported cache - please make new cache: {err}')
            return False

        if prefix_trie is None:
            return False

        if isinstance(prefix_trie, PrefixTrieBase):
            #
            # no need to check version here since only have one (v6).
            # NB we do not inherit cache version or cache compact
            #    we keep those as initialized in constructor.
            #
            self.pyt = prefix_trie.pyt
            self.pyt.thaw()

        elif prefix_trie.vers == 'v3':
            print(f'Converting old v3 cache version {file}\n')
            self.compact = prefix_trie.compact
            self.pyt = convert_cache_v3(prefix_trie)
            self.pyt.thaw()

            file_bak = file + '.bak'
            print(f'  Saving old version {file_bak}\n')
            os.rename(file, file_bak)
            self.write_cache_file(file)

        elif isinstance(prefix_trie, list):
            """
            older map
            - list["CidrCacheElem"]
            """
            print(f'Converting old (v2) cache version {file}\n')
            self.compact = True
            if prefix_trie:
                self.pyt = convert_cache_v2(prefix_trie)
                self.pyt.thaw()

            file_bak = file + '.bak'
            print(f'  Saving old version {file_bak}\n')
            os.rename(file, file_bak)
            self.write_cache_file(file)

        else:
            # wrong data in file (ignore un-released v3 cache)
            print(f'Unknown cache type {file}\n')
            return False

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
        try:
            self.pyt.freeze()
            data = pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL)
            self.pyt.thaw()

        except PickleError as exc:
            print(f' Error saving prefix cache: {exc}')
            return False

        (okay, err) = write_file_atomic(data, file)
        if not okay:
            print(f' Error saving prefix cache: {err}')
            return False
        return True

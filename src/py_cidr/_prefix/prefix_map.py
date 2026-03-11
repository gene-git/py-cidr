# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Cached (network, value) pairs: value is string.
network is either ipv4 or ipv6 ipaddress network (not mixed)
lookup of a cidr returns its associated value.
cidr matches cache.cidr if cidr is subnet of cidr.
Cache is an ordered list by net.
See Also:

    CidrMap which uses CidrCache and with a
    separate cache for ipv4 and ipv6

Requires:

    ipaddress: for cidr/network manipulations
    lockmgr: for ensuring cache can be safely read/written
"""
# pylint: disable=too-many-instance-attributes
from typing import (Any, Iterable, Iterator, Mapping, Self)
import os

from lockmgr import LockMgr

from ._prefix_trie import PrefixTrie
from ._choose_lockfile import choose_lock_file

class PrefixMap(PrefixTrie):
    """
    Derived from PrefixTrie = PrefixTrie + manages file caching.
    Each trie can be ipv4 or ipv6 (not both)>

    PrefixTrie can load/store from a file. This manages that process, chooses where
    things get cached and uses file locking to ensure things are done correctly.

    This is the primary class to use for either IPv4 or IPv6.
    All network data is an ipaddress network.
    To work with CIDR strings, see class CidrNetCache
    (will replace CidrCache once we're done.)
    And the public interface is PrefixTrie to replace CidrMap

    Args:
        cache_dir (str | None):
            Optional directory where cache files are saved.

        ipv6 (bool):
            If true this is used for IPv6 only, otherwise IPv4 which is the default.

        compact (bool):     
            If true,  then prefixes are compacted when possible.
            Example if adding a (prefix, val) and prefix is same as 
            or a subnet of existing prefix that has the same "val", then
            it is redundant and not added. Similarly, adding a prefix, val
            may lead to child prefixes with same value being removed.

    Possible Enhancement: Add cleanup() method to remove lockfile
    """
    def __init__(self, cache_dir: str = '', compact: bool = True, ipv6: bool = False):
        """
        Add cache related details to PrefixMap.
        """

        super().__init__(compact=compact, ipv6=ipv6)
        #
        # Cache info
        #
        self.ipv6: bool = ipv6
        self.cache_dir: str = cache_dir
        self.cache_file: str = ''
        self.cache_time: float = -1.0

        if cache_dir:
            ipt = 'ipv6' if ipv6 else 'ipv4'
            ext = f'{ipt}.pkl'

            self.cache_file = os.path.join(self.cache_dir, ext)
            lockfile = choose_lock_file(self.cache_dir, ipv6, self.vers)
            self.lock_timeout = 120
            self.lockmgr = LockMgr(lockfile)

    def load_cache(self):
        """
        Read cache from file
        """
        if not self.cache_file:
            return

        lockmgr = self.lockmgr
        timeout = self.lock_timeout
        if lockmgr.acquire_lock(wait=True, timeout=timeout):
            if os.path.exists(self.cache_file):
                if self.read_cache_file(self.cache_file):
                    self.cache_time = os.path.getmtime(self.cache_file)
                # else:
                #     print(f'PrefixMap failed to load file: {self.cache_file}')
            self.lockmgr.release_lock()
        else:
            print(f' Prefix cache read failed to get lock after {timeout}')
            print('  ** Failed to read cache')

    def save_cache(self):
        """
        Write cache to file if cache_dir was set up.
        Use locking to ensure no file contention.
        """
        if not self.cache_file:
            return

        if self.dirty:
            lockmgr = self.lockmgr
            timeout = self.lock_timeout
            if lockmgr.acquire_lock(wait=True, timeout=timeout):
                if self.cache_time > 0:
                    # cache changed since we read it in
                    cache_time_now = os.path.getmtime(self.cache_file)
                    if cache_time_now > self.cache_time:
                        print(' Prefix Cache changed - updating cache file')
                        temp_map = PrefixMap(compact=self.compact)
                        if temp_map.read_cache_file(self.cache_file):
                            #
                            # merge our data into the cached file data
                            #
                            if self.vers == temp_map.vers and self.ipv6 == temp_map.ipv6:
                                temp_map.merge_pyt(self.pyt)
                                self.pyt = temp_map.pyt
                            else:
                                print(f'Existing cache file is wrong vers/type')
                                print('  saving our data and ignoring current file')

                # Save the new data
                self.write_cache_file(self.cache_file)
                lockmgr.release_lock()
            else:
                print(f' Prefix cache write failed to get lock after {timeout}')
                print('  ** skipping writing cache')

            self.dirty = False

    def merge_other(self, other: Self) -> bool:
        """
        Merge another CidrCache into self.

        Args:
            new_cache (CidrCache)
            Data must be installed .add() to ensure the cache data is
            network sorted.
            Data from new_cache is combined / merged into the instance data.

            NB requirements:
            - the network types must match or will be ignored.
            - the compact types must match (we could simple make the
              combined map non-compact but we choose to make this error.
        """
        if not other:
            return True

        if other.ipv6 != self.ipv6:
            print('Network Type mismatch - cannot combine:')
            print(f' ipv6: {other.ipv6} added to {self.ipv6}')
            return False

        if other.compact != self.compact:
            print('Compact cache type mismatch - cannot combine:')
            print(' compact and {non-compact maps')
            return False


        if not self.merge_pyt(other.pyt):
            return False
        self.dirty = True
        return True

# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2024-present  Gene C <arch@sapience.com>
"""
Map cidr/ips to a (str) value.
Requires CidrCache

Keep separate caches for ipv4 and ipv6
cidr matches cache.cidr cidr when cidr is subnet of cache.cidr.

Requires CidrCache for the actual cache management
"""
from typing import (Any)

from ._cidr_cache import (CidrCache)
from ._cidr_nets import (cidr_to_net)
from ._cidr_valid import (is_valid_ip4, is_valid_ip6)


class _NetCache:
    """ holds both ipv4 and ipv6 cache """
    def __init__(self, cache_dir: str):
        self.ipv4: CidrCache = CidrCache('ipv4', cache_dir=cache_dir)
        self.ipv6: CidrCache = CidrCache('ipv6', cache_dir=cache_dir)

        if cache_dir:
            self.ipv4.load_cache()
            self.ipv6.load_cache()

    def get(self, ipt: str):
        """
        Returns the cache for ipv4 or ipv6

        Args:
            ipt (str):
            One of 'ipv4' or 'ipv6'
        Returns:
            Cache for the requested network type
        """
        cache = getattr(self, ipt)
        return cache

    def set(self, ipt: str, cache: CidrCache):
        """
        Assigns the cache for ipv4 or ipv6

        Args:
            ipt (str):
            One of 'ipv4' or 'ipv6'
        Returns:
            Cache for the requested network type
        """
        setattr(self, ipt, cache)
        return cache

    def get_cache(self, iptype: str) -> CidrCache:
        """
        Extract the cache for the provided iptype

        Args:
            ipt (str):
            One of 'ipv4' or 'ipv6'

        Returns:
            CidrCache:
            Cache for "iptype"
        """
        match iptype:
            case 'ipv4':
                return self.ipv4

            case 'ipv6':
                return self.ipv6

            case _:
                raise ValueError('iptype must be one of "ipv4" or "ipv6"')


class CidrMap:
    """
    Class provides map(cidr) -> some value.

     - ipv4 and ipv6 are cached separately
     - built on CidrCache and Cidr classes

    Args:
        cache_dir (str):
        Optional directory to save cache file
    """
    def __init__(self, cache_dir: str | None = None):
        """
        Instantiate CidrMap instance.
        """
        self._cache_dir: str = ''

        if cache_dir:
            self._cache_dir = cache_dir

        self._cache: _NetCache = _NetCache(cache_dir=self._cache_dir)

    def _iptype(self, cidr: str) -> str:
        """
        Identify whether cidr is a valid "ipv4" or "ipv6".

        Args:
            cidr (str):
            Input cidr string

        Returns:
            str:
            'ipv4' of 'ipv6' based on cidr or None if invalid cidr string.
            Return empty string '' if unknown.
        """
        net = cidr_to_net(cidr)
        if not net:
            return ''

        if is_valid_ip4(net):
            return 'ipv4'

        if is_valid_ip6(net):
            return 'ipv6'

        return ''

    def save_cache(self):
        """
        Write cache to files
        """
        self._cache.ipv4.write()
        self._cache.ipv6.write()

    def lookup(self, cidr: str) -> Any | None:
        """
        Check if cidr is in map.

        Args:
            cidr (str):
            Cidr value to lookup.

        Returns:
            Any | None:
            Result = map(cidr) if found else None.
        """
        ipt = self._iptype(cidr)
        if not ipt:
            return None

        result = None
        cache = self._cache.get_cache(ipt)
        result = cache.lookup_cidr(cidr)
        return result

    @staticmethod
    def create_private_cache() -> _NetCache:
        """
        Create and Return private cache object to use with add_cidr().

        This cache has no cache_dir set - memory only.
        Required if one CidrMap instance is used in multiple processes/threads
        Give each process/thread a private data cache and they can be merged
        into the CidrMap instance after they have all completed.

        Returns:
            (private):
            private_cache_data object.
        """
        private_cache = _NetCache(cache_dir='')
        return private_cache

    def add_cidr(self, cidr: str, result: str, priv_cache: _NetCache | None = None):
        """
        Add cidr to cache.

        Args:
            cidr (str):
            Add this cidr string and its associated result value to the map.

            result (str):
            The result value to be associated with this cidr.
            i.e. map(cidr) = result

            priv_data (private):

            If using multiple processes/threads then provide this object
            where changes are kept instead of in the instance cache.
            This way the same instance (and its cache) can be used
            across multiple processes/threads.

            Use CidrMap.create_private_cache() to create private_data

        """
        ipt = self._iptype(cidr)
        if not ipt:
            return

        if priv_cache:
            cache = priv_cache.get_cache(ipt)
        else:
            cache = self._cache.get_cache(ipt)

        cache.add_cidr(cidr, result)

    def merge(self, priv_cache: _NetCache | None):
        """
        Merge private cache into our internal cache.

        Args:
            priv_data (_PrivCache):
            The "private data" to add (cidr, result) to the map, then
            this merges content of priv_data into the current data.
            priv_data must be created by CidrMap.create_private_cache()
        """
        if not priv_cache:
            return

        self._cache.ipv4.combine_cache(priv_cache.ipv4)
        self._cache.ipv6.combine_cache(priv_cache.ipv6)

    def print(self):
        """
        Print the cache data.
        """
        self._cache.ipv4.print()
        self._cache.ipv6.print()

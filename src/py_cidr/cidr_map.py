# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Map cidr prefixes to some value.

Use separate maps for ipv4 and ipv6
"""
from typing import (Any, Iterator)

from py_cidr._network import PrefixVal
from py_cidr._network.ip_version import ip_version

from py_cidr._prefix import PrefixMap
from py_cidr._prefix import PrefixMaps


class CidrMap:
    """
    Class provides map(cidr) -> some value.

     - ipv4 and ipv6 are cached separately
     - built on CidrCache and Cidr classes

    Args:
        cache_dir (str):
        Optional directory to save cache file

    todo: generalize value to be any object not just string
    # def __init__(self, cache_dir: str | None = None):
    """
    def __init__(self, cache_dir: str = '', compact: bool = False):
        """
        Instantiate CidrMap instance.
        """
        self._cache_dir: str = ''
        self.compact = compact

        if cache_dir:
            self._cache_dir = cache_dir

        self.ipv4: PrefixMap = PrefixMap(cache_dir=self._cache_dir, compact=compact)
        self.ipv6: PrefixMap = PrefixMap(cache_dir=self._cache_dir, compact=compact, ipv6=True)

        if cache_dir:
            self.ipv4.load_cache()
            self.ipv6.load_cache()

    def _get_prefix_map(self, cidr: str, private_maps: PrefixMaps | None = None) -> PrefixMap | None:
        """
        Determine which prefix map to use.
        If private_maps is passed in then will be taken from there.
        Otherwise from self.
        """
        if not cidr:
            return None

        ipvers = ip_version(cidr)
        match ipvers:
            case 4:
                if private_maps is not None:
                    return private_maps.ipv4
                return self.ipv4

            case 6:
                if private_maps is not None:
                    return private_maps.ipv6
                return self.ipv6

            case _:
                return None

    def save_cache(self):
        """
        Write cache to files
        """
        self.ipv4.save_cache()
        self.ipv4.save_cache()

    def lookup_lmp(self, cidr: str) -> tuple[str, Any]:
        """
        Check if cidr is in the map. Similar to lookup()
        but returns the longest matching prefix (LMP) and it's value.
        cidr is then the same as or subnet of prefix.
        If not found then empty string for prefix.

        See lookup_all() which returns list of (prefix, val) tuples
        where the first element is the (lmp, val) pair.

        Args:
            cidr (str):
                Cidr value to lookup.

        Returns:
            tuple[prefix: str, value: Any]
                cidr is same as or subnet of prefix and val it's assocated value.
                If not found then prefix is empty string.
        """
        prefix_val: tuple[str, Any] = ('', None)

        prefix_map = self._get_prefix_map(cidr)
        if prefix_map is None:
            return prefix_val

        prefix_val = prefix_map.lookup_lmp(cidr)
        return prefix_val

    def lookup_all(self, cidr: str) -> list[tuple[str, Any]]:
        """
        If cidr is in the map, return list of all (prefix, val) tuples.
        cidr is a subnet of each prefix. The first (prefix, val) returned
        is always the longest matching prefix (LMP) and it's value: (lmp, val)

        The remaining elements will all have shorter prefix length (larger, less specific)
        network blocks.

        Args:
            cidr (str):
                Cidr value to lookup.

        Returns:
            list[tuple[prefix: str, val: Any]]
                Result = map(cidr). If no matching elements found
                returns empty list. Otherwise returns list of values
                for each element for which cidr is a subnet.
        """
        results: list[tuple[str, Any]] = []

        prefix_map = self._get_prefix_map(cidr)
        if prefix_map is None:
            return results

        prefix_vals = prefix_map.lookup_all(cidr)
        return prefix_vals

    @staticmethod
    def create_private_cache() -> PrefixMaps:
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
        private_maps = PrefixMaps(cache_dir='')
        return private_maps

    def add_prefix_val(self, prefix_val: PrefixVal, priv_maps: PrefixMaps | None = None):
        """
        Add cidr to cache.

        Args:
            prefix_val (PrefixVal):
                PrefixVal = tuple[prefix: str, val: Any]
                Add this (prefix, val) pair to the map.

            priv_map (private):
                If using multiple processes/threads then provide this object
                where changes are kept instead of in the instance cache.
                This way the same instance (and its cache) can be used
                across multiple processes/threads.

                Use CidrMap.create_private_cache() to create private_data
        """
        prefix_map = self._get_prefix_map(prefix_val[0], priv_maps)
        if prefix_map is None:
            return

        prefix_map.update(prefix_val)

    def add_prefix_vals(self, prefix_vals: list[PrefixVal]):
        """
        Add list if (prefix, val) tuples.

        Args:
            prefix_vals (list[PrefixVal]):
                List of tuples each being (prefix: str, val: Any)
        """
        if not prefix_vals:
            return

        prefix_map = self._get_prefix_map(prefix_vals[0][0])
        if not prefix_map:
            return

        prefix_map.update(prefix_vals)

    def merge(self, priv_maps: PrefixMaps | None):
        """
        Merge private maps back into into our own maps.

        Args:
            priv_maps (PrefixMaps):
                The "private data" to add map.
                Merge the content of priv_maps into the current data.
                See CidrMap.create_private_cache()
        """
        if not priv_maps:
            return

        self.ipv4.merge_pyt(priv_maps.ipv4.pyt)
        self.ipv6.merge_pyt(priv_maps.ipv6.pyt)

    def print(self):
        """
        Print the cache data.
        """
        self.ipv4.print()
        self.ipv6.print()

    def items(self, v6: bool = False) -> Iterator[tuple[str, Any]]:
        """
        Iterator that returns oen element at a time of the map.
        Args:
            v6 (bool):
                Default is false, and the elements are from IPv4 map
                If True, then elements are taken from the IPv6 map.
        Returns:
            tuple[cidr: str, value: str]:
                The (cidr, value) for each map element
        """
        if v6:
            yield from self.ipv6.items()
        else:
            yield from self.ipv4.items()
    #
    # Deprecated methods - to be removed in a future version.
    #

    def add_cidr(self, cidr: str, val: Any, priv_maps: PrefixMaps | None = None):
        """
        Historical version of add_prefix_val() - use that instead please.
        """
        self.add_prefix_val((cidr, val), priv_maps)

    def add_cidrs(self, prefixes: list[str], vals: list[Any]):
        """
        Historical version - use add_prefix_vals() instead.
        """
        prefix_vals: list[PrefixVal] = list(zip(prefixes, vals))
        self.add_prefix_vals(prefix_vals)

    def lookup(self, cidr: str) -> Any | None:
        """
        Deprecated: Historical. Change to lookup_lmp()

        Same as lookup_lmp() but only returns value not (prefix, value).

        Returns the value of associated with lmp prefix for which
        cidr is subnet (or same) as. The prefix returned is the
        longest matching prefix (LMP).

        Similar to lookup_both() but only the value is returned
        instead of both (prefix, value).

        Args:
            cidr (str):
                Cidr value to lookup.

        Returns:
            Any | None:
                Result = map(cidr) if found else None.
        """
        (_lmp, val) = self.lookup_lmp(cidr)
        return val

    def lookup_both(self, cidr: str) -> tuple[str, Any]:
        """
        Deprecated: Historical - same as lookup_lmp()
        """
        return self.lookup_lmp(cidr)

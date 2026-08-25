# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Map cidr prefixes to some value.

Uses separate maps for ipv4 and ipv6
"""
from typing import (Any, Iterator)

from py_cidr.pycidr_class import PyCidr

from py_cidr._prefix import PrefixVal
from py_cidr._prefix import PrefixMap
from py_cidr._prefix import PrefixMaps


class CidrMap:
    """
    Class provides map(cidr) -> some value.
     - ipv4 and ipv6 are cached separately
     - built on CidrCache and Cidr classes

    :param cache_dir: Optional directory to keep cached copy of map
    :param compact: Optional flag to request a compact map.
                    The standard map keeps every prefix added to map 
                    and this is the default. 
                    If compacting, then adjacent prefixes whose associated
                    values are the same, will have the prefixed compacted to
                    a single prefix.
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

        if PyCidr.is_valid_ipv4(cidr):
            if private_maps is not None:
                return private_maps.ipv4
            return self.ipv4

        if PyCidr.is_valid_ipv6(cidr):
            if private_maps is not None:
                return private_maps.ipv6
            return self.ipv6

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

        :param cidr: Cidr value to lookup.
        :returns: A tuple of (prefix, value) where
                  cidr is same as or a asubnet of prefix and value is the assocated value.
                  If not found then prefix is empty string.
        """
        prefix_val: tuple[str, Any] = ('', None)

        prefix_map = self._get_prefix_map(cidr)
        if prefix_map is None:
            return prefix_val

        prefix_val = prefix_map.lookup_lmp(cidr)
        return prefix_val

    def lookup(self, cidr: str) -> Any | None:
        """
        Return the value associated with the LPM (longest prefix match) of cidr.
        :param cidr: The cidr to lookup
        :returns: The value of the LPM of input cidr.
        """
        prefix_map = self._get_prefix_map(cidr)
        if prefix_map is None:
            return None

        value = prefix_map.lookup(cidr)
        return value

    def lookup_all(self, cidr: str) -> list[tuple[str, Any]]:
        """
        If cidr is in the map, return list of all (prefix, val) tuples.
        cidr is a subnet of each prefix. The first (prefix, val) returned
        is always the longest matching prefix (LMP) and it's value: (lmp, val)

        The remaining elements will all have shorter prefix length (larger, less specific)
        network blocks.

        :param cidr: Cidr value to lookup.
        :returns: A list of tuples (prefix, value]).
                  where cidr is same as or subnet of each prefix.
                  Empty list If no matching elements found
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

        :returns: A private_cache_data object.
        """
        private_maps = PrefixMaps(cache_dir='')
        return private_maps

    def add_prefix_val(self, prefix_val: PrefixVal, priv_maps: PrefixMaps | None = None):
        """
        Add cidr to the map..

        :param prefix_val: The tuple of (prefix, value) to add to the map.
        :param priv_map: Optional private cache.
                         If using multiple processes/threads then provide this object
                         where changes are kept thread local to the private map 
                         instead of in the instance cache.
                         This way the same instance (and its cache) can be used
                         across multiple processes/threads. All the thread local
                         caches can be merged ex post.

                         Use CidrMap.create_private_cache() to create private_data
        """
        prefix_map = self._get_prefix_map(prefix_val[0], priv_maps)
        if prefix_map is None:
            return

        prefix_map.update(prefix_val)

    def add_prefix_vals(self, prefix_vals: list[PrefixVal]):
        """
        Add list if (prefix, val) tuples.

        :param prefix_vals: Add a list of tuples of (prefix, value) to map.
        """
        if not prefix_vals:
            return

        prefix_map = self._get_prefix_map(prefix_vals[0][0])
        if not prefix_map:
            return

        # bulk only handles non-compact
        if self.compact:
            prefix_map.update(prefix_vals)
        else:
            prefix_map.bulk_update(prefix_vals)

    def merge(self, priv_maps: PrefixMaps | None):
        """
        Merge private maps back into into our instance map.

        :param priv_maps: The "private data" to add to the map.
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
        Iterator that returns oen tuple element (prefix, value) at a time 
        fomr the map.

        :prefix v6: Default is false, and the elements are from IPv4 map
                    If True, then elements are taken from the IPv6 map.
        :returns: One tuple (prefix, value)]:
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
        Deprecated Legacy function - use add_prefix_val() instead.
        """
        self.add_prefix_val((cidr, val), priv_maps)

    def add_cidrs(self, prefixes: list[str], vals: list[Any]):
        """
        Deprecated Legacy function - use add_prefix_vals() instead.
        """
        prefix_vals: list[PrefixVal] = list(zip(prefixes, vals))
        self.add_prefix_vals(prefix_vals)


    def lookup_both(self, cidr: str) -> tuple[str, Any]:
        """
        Deprecated: Historical - same as lookup_lmp()
        """
        return self.lookup_lmp(cidr)

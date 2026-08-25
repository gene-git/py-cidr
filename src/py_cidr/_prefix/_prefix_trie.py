# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Cached (cidr, value) pairs: value is string.
network is any ipaddress network (ipv4 or ipv6 )
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
# pylint: disable=too-many-instance-attributes,too-few-public-methods
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
from typing import (Any, Iterable, Iterator, Mapping)

from patricia26 import Patricia26

from py_cidr._prefix._prefix_trie_base import PrefixTrieBase
from py_cidr._prefix.prefix_types import PrefixVal


class PrefixTrie(PrefixTrieBase):
    """
    A collection of (network prefix, val) tuples.
    The collection is held in a Patricia Trie (see PrefixTrieBase)
    """
    def __init__(self, compact: bool = False, ipv6: bool = False):
        super().__init__(compact=compact, ipv6=ipv6)

        self.dirty: bool = False

    def update(self, *args: PrefixVal | Iterable[PrefixVal] | Mapping[str, Any]):
        """
        Update the map.
        Note if any key already exists in the existing map, it will be replaced
        by the updated (key, value) pair.

        Args:
            args (PrefixVal | Iterable[PrefixVal] | Mapping[str, Any]):
                PrefixVal: tuple[cidr: str, val: Any]
                Can be one PrefixVal or a list of PrefixVal or a dcitionary of
                {cidr: val}
        """
        for arg in args:
            if isinstance(arg, tuple):
                self._update_prefix_val(arg)

            elif isinstance(arg, Mapping):
                for prefix_val in arg.items():
                    self._update_prefix_val((prefix_val))
            else:
                for cidr_elem in arg:
                    self._update_prefix_val(cidr_elem)

    def bulk_update(self, pfx_vals: list[PrefixVal]):
        """
        For each (prefix, value) add to the tree.

        Note 1: this always marks the tree dirty.
        Note 2: this ignores "compact"
        """
        self.dirty = True
        self.pyt.bulk_insert(pfx_vals)

    def _update_prefix_val(self, prefix_val: tuple[str, Any]) -> bool:
        """
        Insert prefix_val to the list.
        Works for compact as well as non-compact.
        Args:
            prefix_val (tuple[cidr: str, value: Any]):
                Input (cidr, val) pair.

        Returns:
            False if some error happened.
        """
        #
        # Need input net
        #
        if not prefix_val[0]:
            return True

        if self.compact:
            return self._update_compact(prefix_val)
        return self._update(prefix_val)

    def _update(self, prefix_val: tuple[str, Any]) -> bool:
        """
        Install prefix_val to the list. Non compact.

        Args:
            prefix_val (tuple[cidr: str, value: Any]):
                Input (cidr, val) pair.

        Returns:
            False if some error happened.
        """
        try:
            self.pyt[prefix_val[0]] = prefix_val[1]
            self.dirty = True

        except ValueError as _exc:
            print(f'Error adding {prefix_val}')
            return False
        return True

    def _update_compact(self, prefix_val: tuple[str, Any]) -> bool:
        """
        Install elem to the list - compact version.
        Args:
            prefix_val (tuple[cidr: str, value: Any]):
                Input (cidr, val) pair.

        Returns:
            False if some error happened.

        Each prefix (node) in trie has one parent and zero or more children
        """
        prefix = prefix_val[0]
        val = prefix_val[1]
        pyt = self.pyt

        #
        # 1) Check if prefix exists and has same value
        #
        # NB: has_key() matches exact prefix, "in" matches if same or subnet
        #
        if prefix in pyt and pyt[prefix] == val:
            return True

        #
        # 2) (prefix, val) Not in trie so add it.
        #
        pyt[prefix] = val
        self.dirty = True

        #
        # 3) Check if any (now) redundant children (same value) can be removed
        #
        child_prefixes: list[str] = pyt.children(prefix)
        for pfx in child_prefixes:
            if pyt[pfx] == val:
                del pyt[pfx]

        return True

    def print(self):
        """
        print all the elements
        """
        if len(self.pyt) < 1:
            return
        print(f'Version: {self.vers}')
        print(f'ipv5   : {self.ipv6}')
        print(f'pfxlen : {self.prefixlen}')
        print(f'Compact: {self.compact}')

        for prefix in self.pyt:
            print(f"  {prefix}: {self.pyt[prefix]}")

    def lookup_lpm(self, cidr: str) -> tuple[str, Any]:
        """
        Find and return LPM (longest matching prefix) which "cidr" belongs to
        and return the (lpm, value).

        The longest prefix is the most specific.

        e.g.
            10.0.0.0/22     -> 'net_0_22'
            10.0.0.1/24     -> 'net_1_24'

        then lmp('10.0.0.64') -> ('10.0.0.1/24', 'net_1_24'

        Compare with lookup_parents ->
            [('10.0.0.1/24', 'net_1_24'), ('10.0.0.0/22', 'net_0_22')

        Args:
            cidr (str):
                The cidr block to lookup.

        Returns:
                tuple[prefix: str, value: Any]
                    Where prefix is the LMP prefix and its value is 'value'
        """
        if not cidr:
            return ('', None)

        lpm_str: str = ''
        lpm: str | None = ''
        val: Any = None
        (lpm, val) = self.pyt.lookup_lpm(cidr)

        if lpm is not None:
            lpm_str = lpm

        return (lpm_str, val)

    def lookup(self, cidr: str) -> Any:
        """
        Find and return the value associated with the LPM (longest prefix match) 
        to which "cidr" belongs.

        The longest prefix is the most specific.

        e.g.
            10.0.0.0/22     -> 'net_0_22'
            10.0.0.1/24     -> 'net_1_24'

                lookup('10.0.0.64') -> 'net_1_24'
            lookup_lpm('10.0.0.64') -> ('10.0.0.1/24', 'net_1_24')
            
        :param cidr: The cidr block to lookup.
        :returns: The value associated with the LPM of cidr.
        """
        if not cidr:
            return None

        val: Any = None
        val = self.pyt.lookup(cidr)
        return val

    def lookup_lmp(self, cidr: str) -> tuple[str, Any]:
        """ Alias for lookup_lpm (historical)"""
        return self.lookup_lpm(cidr)

    def lookup_all(self, cidr: str) -> list[tuple[str, Any]]:
        """
        Return list of prefixes and values for which cidr is subnet.
        See also lookup_lpm() which returns only the longest matching prefix.
        """
        pfx_vals:  list[tuple[str, Any]] = []
        prefix: str | None = None
        (prefix, val) = self.lookup_lpm(cidr)
        if not prefix:
            return pfx_vals

        pfx_vals.append((prefix, val))
        pyt = self.pyt
        while prefix is not None:
            prefix = pyt.parent(prefix)
            if prefix is not None:
                pfx_vals.append((prefix, pyt.lookup(prefix)))

        return pfx_vals

    def merge_pyt(self, other_pyt: Patricia26) -> bool:
        """
        Merge other into self where other takes precedence.
        todo: use pyt.bulk_install()
        """
        for prefix in other_pyt:
            self.pyt[prefix] = other_pyt[prefix]

        return True

    def items(self) -> Iterator[PrefixVal]:
        """
        Iterator to return PrefixVal one at a time
        """
        for prefix in self.pyt:
            yield (prefix, self.pyt[prefix])

# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2024-present  Gene C <arch@sapience.com>
"""
Cached (network, value) pairs: value is string.
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
from typing import (Self)

from .cidr_types import (IPvxNetwork)
from ._cidr_compact import (compact_nets)
from ._cache_elem import CidrCacheElem
from ._cache_files import (read_cache_file, write_cache_file)


class CidrCacheData:
    """
    A list of cache elements.
    version used when reading old cache files.
    """
    def __init__(self):
        self.vers: str = 'v2'
        self.elems: list[CidrCacheElem] = []

    def read_cache_file(self, file: str):
        """
        Read data from cache file.
        Caller responsible for locks etc
        """
        elems = read_cache_file(file)
        if not elems:
            return
        self.elems = elems

    def write_cache_file(self, file: str):
        """
        Read data from cache file.
        Caller responsible for locks etc
        """
        write_cache_file(self.elems, file)

    def _compact(self):
        """
        Unused: merge if possible
        """
        _try_merge(self.elems, 0, direction=0)

    def merge_data(self, new_data: Self) -> bool:
        """
        Merge data from new_data
        Args:
            new_data (CidrCacheData)
            The cache data to merge

        Returns:
            bool:
            True if changes to data made.
        """
        if not new_data or not new_data.elems:
            return False

        if not self.elems:
            # this is ok as new_data was built by add() and is sorted/merged
            self.elems = new_data.elems
            return True

        changed = False
        for elem in new_data.elems:
            changed |= self.add_elem(elem)
        return changed

    def print(self):
        """ print all the elements """
        for elem in self.elems:
            elem.print()

    def lookup_elem(self, net: IPvxNetwork) -> CidrCacheElem | None:
        """
        Locate cache element associated with network "net".

        If network in cache then return the Cache Element
        if found. net is either equal to cache_elem.net
        or is a subnet of it.
        If net is not found then Noneis returned.

        Args:
            net (IPvxNetwork):
            The network to lookup.

        Returns:
            CidrCacheElem | None:
            A list of with 2 items: [cache_network, value].
            where net is either equal to cache_network or a subnet of it.
            If net is not found then [None, None]
        """
        (index, ismatch) = self.find_nearest(net)
        if ismatch:
            return self.elems[index]
        return None

    def find_nearest(self, net: IPvxNetwork) -> tuple[int, bool]:
        """
        Find Nearest (internal).

        Find the index of the element (foundnet, value)
        where net is a subnet of foundnet
        or the index of the element after which net would be inserted
        elem[i] <= net < elem[i+1]
        when net = elem[i] (i.e. net is subnet of elem[i]) then ismatch is True

        By default the internal cache (self.data) is searched unless priv_data
        is provided - in which case it is used to do the search.

        Returns:
            tuple[int, bool]:
            tuple of (Index, ismatch). Index refers to cache list.
            Match is True when net is a subnet of the cache element
            at index or is identical to that net.

        """

        if not self.elems:
            return (-1, False)

        (index, ismatch) = _find_nearest(self.elems, net)
        return (index, ismatch)

    def sort(self):
        """
        Sort in network order
        """
        if not self.elems or len(self.elems) < 2:
            return
        self.elems.sort(key=lambda elem: elem.net)

    def add_elem(self, elem: CidrCacheElem) -> bool:
        """
        Add elem to cache
        Add elem = (net, value) to cache.

        Note that if add a (cidr, value) pair exists in cache but is different,
        then the new value added here will replace the existing one.

        Better name might be add_or_replace()

        Args:
            elem (CidrCacheElem):
            Element to add (elem.net, elem.val)

        Returns:
            bool:
            True if cache data changed
            False if not.

        """
        (ind, ismatch) = self.find_nearest(elem.net)
        elems = self.elems
        if ismatch:
            #
            # net is a subnet of (or equal to) elems[i].net
            # If val not same, keep net part and update value
            #
            if elem.val != elems[ind].val:
                # updated value replaces existing
                # if data is not None:
                #     data.append([net, value])
                # else:
                elems[ind].val = elem.val
                return True
            return False

        #
        # if ind+1 is subnet of net then can be replaced by
        # combining the 2 nets. If new value is different we assume
        # its correct - so thus okay to delete
        #
        # if ind+1 and net have same value check if can be merged
        #
        num_elems = len(elems)
        if ind < num_elems - 1:
            en1 = elems[ind+1]
            is_subnet = en1.net.subnet_of(elem.net)  # type: ignore[arg-type]
            if is_subnet:
                del self.elems[ind+1]

        #
        # insert at ind+1
        #
        self.elems.insert(ind+1, elem)

        #
        # Check if changed leads to any network merge opportunity
        #
        _try_merge(self.elems, ind, direction=0)

        return True


def _try_merge(elems: list[CidrCacheElem], ind: int, direction: int = 0):
    """
    Merging any neighboring nets if possible.

    When new net is added it might be possible to merge some of the nets
    So, if possible merge any nets in cache which can be merged.
    The work begins at index 'ind'. Since we keep the cache ordered
    and merged we only need to do this whenever element is inserted.
    and this if i+1 cannot be merged then i+2, i+3 etc likewise.
    Ditto for i-1. So by keeping list merged and sorted we only need
    to check i+1,i-1 (and recurse if we merge anything).
    In this case an element was inserted at index 'ind'

    So first check (ind, ind+1) - if merged then work to next higher and so on
    Then work down (ind, ind-1) similarly
    Input:
        ind : index to start merge (ie what just got inserted into list)
        direction:
            1 only merge i > index
           -1 only merge i < index
            0 merge both ways
    """
    # pylint: disable=chained-comparison
    if ind < 0:
        return

    num_elems = len(elems)
    ind_next = ind + 1
    if direction >= 0 and ind_next < num_elems:
        if elems[ind].val == elems[ind_next].val:
            try_merged = compact_nets([elems[ind].net, elems[ind_next].net])
            if len(try_merged) == 1:
                elems[ind].net = try_merged[0]
                del elems[ind_next]
                _try_merge(elems, ind, direction=1)

    num_elems = len(elems)
    ind_prev = ind - 1
    if direction <= 0 and ind_prev >= 0:
        if elems[ind].val == elems[ind_prev].val:
            try_merged = compact_nets([elems[ind].net, elems[ind_prev].net])
            if len(try_merged) == 1:
                elems[ind_prev].net = try_merged[0]
                del elems[ind]
                _try_merge(elems, ind_prev, direction=-1)


def _find_nearest(elems: list[CidrCacheElem], net: IPvxNetwork
                  ) -> tuple[int, bool]:
    """
    Return (index, ismatch).

    If a match is ound then ismatch -> 1
    where elem = elems[index]

    ismatch = True means net is either identical to
    elem.net or a subnet of elem.net.

    Find index of the element that matches (ismatch = True)
    or index after which net would be added to list to keep it sorted
    if net is small than first element then returns -1 so net should
    be inserted at element 0
    Algorithm is binary search.
    """
    if not elems:
        return (-1, False)

    ismatch = False
    low = 0
    high = len(elems) - 1
    index = -1

    while low <= high:
        mid = (low + high) // 2

        if elems[mid].net <= net:   # type: ignore[operator]
            index = mid
            low = mid + 1
        else:
            high = mid - 1

    if index >= 0:
        if net.subnet_of(elems[index].net):  # type: ignore[arg-type]
            ismatch = True
    return (index, ismatch)

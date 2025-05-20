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
# pylint: disable=too-many-instance-attributes
from typing import (Any, Self, Tuple)
import os

from lockmgr import LockMgr

from .cidr_types import (IPvxNetwork)
from ._cidr_nets import (cidr_to_net)
from ._cache_files import (cache_file_extension)
from ._cache_data import (CidrCacheData, CidrCacheElem)


class CidrCache:
    """
    Provides a cache that maps cidrs to values.

    Implemented as an ordered list of networks.
    All networks must be either ipv4 or ipv6
    as these are kept separate for performance.
    Each network has an assocated value.
    Each elem in ordered list is a typle of (cidr_net, value)

    Note that data list *must* be kept sorted and compressed.
    Compressing ensures that no elem can be subnet of any other element.
    Sorting allows search to work (efficiently).

    We use ipaddress network as the key rather than a string as
    this provides superior performance. This also minimizes
    conversion between network and string representations.

    Args:
        ipt (str):
        One of 'ipv4' or 'ipv6'

        cache_dir (str | None):
        Optional directory where cache files are saved.

    Enhancement: Add cleanup() method to remove lockfile

    """
    def __init__(self, ipt: str, cache_dir: str | None = None):
        self.ipt: str = ipt
        self.dirty: bool = False
        self.cache_dir: str = ''
        self.using_cache_file: bool = False
        self.cache_file: str = ''
        self.cache_time: float = -1.0
        self.cache_data = CidrCacheData()

        if cache_dir:
            self.cache_dir = cache_dir
            self.using_cache_file = True
            ext = ipt + cache_file_extension()
            self.cache_file = os.path.join(self.cache_dir, ext)
            lockfile = _choose_lock_file(self.cache_dir, ipt)
            self.lock_timeout = 120
            self.lockmgr = LockMgr(lockfile)
        else:
            self.cache_data = CidrCacheData()

    def load_cache(self):
        """
        Read cache from file
        """
        if not self.using_cache_file:
            return

        lockmgr = self.lockmgr
        if lockmgr.acquire_lock(wait=True, timeout=self.lock_timeout):
            self.cache_data.read_cache_file(self.cache_file)
            #
            # Cache Element has (net, val).
            # net is a network represented as IPvxNetwork
            # and val can be Any
            #
            if self.cache_data.elems:
                self.cache_time = os.path.getmtime(self.cache_file)
            self.lockmgr.release_lock()
        else:
            print(f'CIDR Cache failed to load cache: {self.cache_file}')

    def write(self):
        """
        Write cache to file if cache_dir was set up.

        Use locking to ensure no file contention.
        """
        if not self.cache_file:
            return

        if self.dirty:
            timeout = self.lock_timeout
            lockmgr = self.lockmgr
            if lockmgr.acquire_lock(wait=True, timeout=timeout):
                # Check if cache changed since we read it in
                if self.cache_time > 0:
                    cache_time_now = os.path.getmtime(self.cache_file)
                    if cache_time_now > self.cache_time:
                        print(' cidr cache updated since prev read - merging')
                        temp_data = CidrCacheData()
                        temp_data.read_cache_file(self.cache_file)
                        if temp_data.elems:
                            self.cache_data.merge_data(temp_data)
                            # temp_cache = None

                self.cache_data.write_cache_file(self.cache_file)
                lockmgr.release_lock()
            else:
                print(f' cache write failed to get lock after {timeout}')
                print('  ** skipping writing cache')

            self.dirty = False

    def sort(self):
        """
        Sort the cached data in network order.
        """
        self.cache_data.sort()

    def lookup_elem(self, net: IPvxNetwork) -> CidrCacheElem | None:
        """
        Lookup value associated with network.

        If network in cache then return the pair [cache_net, value].
        with net either equal to cache_net or a subnet of it.
        If not found then [None, None] is returned.

        Args:
            net (IPvxNetwork):
            The network to lookup.

        Returns:
            [IPvxNetwork, Any]:
            A list of with 2 items: [cache_network, value].
            where net is either equal to cache_network or a subnet of it.
            If net is not found then [None, None]

        """
        return self.cache_data.lookup_elem(net)

    def lookup_cidr(self, cidr: str) -> Any:
        """
        Look up the value associated with cidr string:
         - cache(cidr) -> value

        Args (str):
            Cidr to lookup

        Returns:
            str | None:
            Value associated with the cidr string or None if not found
        """
        net = cidr_to_net(cidr)
        if net:
            elem = self.cache_data.lookup_elem(net)
            if elem:
                return elem.val
        return None

    def lookup(self, net: IPvxNetwork
               ) -> Tuple[IPvxNetwork, Any] | Tuple[None, None]:
        """
        Lookup value associated with network.

        If network in cache then return the pair [cache_net, value].
        with net either equal to cache_net or a subnet of it.
        If not found then [None, None] is returned.

        Args:
            net (IPvxNetwork):
            The network to lookup.

        Returns:
            [IPvxNetwork, Any]:
            A list of with 2 items: [cache_network, value].
            where net is either equal to cache_network or a subnet of it.
            If net is not found then [None, None]

        """
        elem = self.cache_data.lookup_elem(net)
        if elem:
            return (elem.net, elem.val)
        return (None, None)

    def add_cidr(self, cidr: str, value: Any):
        """
        Same as add() but with input a cidr string instead of network.
        """
        net = cidr_to_net(cidr)
        if net is not None:
            self.add(net, value)

    def add(self, net: IPvxNetwork, value: Any):
        """
        Add (net, value) to cache.

        Note that if add a (cidr, value) pair exists in cache but is different,
        then this new added version will replace the existing one.

        Better name might be add_or_replace()

        Args:
            net (IPvxNetwork):
            ipaddress network to add to cache

            value (Any):
            The value associated with net to be cached as (net, value) pair.

            When present, all additions are made to private data
            instead of instance data and our own data is read only until
            all threads/processes finish.

        """
        if net:
            elem = CidrCacheElem()
            elem.net = net
            elem.val = value

            changed = self.cache_data.add_elem(elem)
            if changed:
                self.dirty = True

    def combine_cache(self, new_cache: Self):
        """
        Merge another CidrCache into self.

        Args:
            new_cache (CidrCache)
            Data must be installed .add() to ensure the cache data is
            network sorted.
            Data from new_cache is combined / merged into the instance data.

            NB the network types must match or will be ignored.
        """
        if not new_cache:
            return

        if new_cache.ipt != self.ipt:
            print('Network Type mismatch - cannot combine:')
            print(' {new_cache.ipt} added to {self.ipt}:')
            return

        if not self.cache_data:
            # this is ok as new_data was built by add() and is sorted/merged
            self.cache_data = new_cache.cache_data
            return

        changed = self.cache_data.merge_data(new_cache.cache_data)
        if changed:
            self.dirty = True

    def print(self):
        """
        Print all the data.
        """
        if self.cache_data:
            print(f'# {self.ipt}')
            self.cache_data.print()


def _choose_lock_file(cache_dir: str, ipt: str) -> str:
    """
    Generate lock file to protect cache writes and reads
    lockfile in /tmp but use cache file name to ensure lock applies
    to what its needed for

    NB lockfile must be same across processes so that the lock
    is respected across processes. We prefer to use /tmp
    as this is tmpfs and avoids NFS.

    This means we dont want to use any 'tempdir/tempfile'.

    Preferable to use username.  But when run in chroot there may
    be no user / controlling terminal.

    E.g. When building package in chroot and running tests.
    In this case we use cache_dir.
    """
    if not cache_dir:
        return '-x-'

    try:
        user = os.getlogin()
        lockdir = f'/tmp/py-cidr-{user}'
        lockfile = f'{ipt}.' + os.path.basename(cache_dir) + '.lock'

    except OSError:
        user = 'xxx'
        lockdir = cache_dir
        lockfile = f'{ipt}.lock'

    os.makedirs(lockdir, exist_ok=True)
    path = os.path.join(lockdir, lockfile)
    return path

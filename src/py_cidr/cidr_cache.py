# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2024-present  Gene C <arch@sapience.com>
'''
Cached map of (network, value) pairs: value is string.
network is any ipaddress network (ipv4 or ipv6 or both)
lookup of a cidr returns its val.
cidr matches cache.cidr if cidr is subnet of cidr.
Cache is an ordered list by net.
 See Also:
    CidrMap which uses CidrCache and uses a separate cache for ipv4 and ipv6
 Requires: 
    ipaddress: for cidr/network manipulations
    lockmgr: for ensuring cache can be safely read/written
'''
# pylint: disable=too-many-instance-attributes
import os
from typing import (List)
from ipaddress import (IPv4Network, IPv6Network)

from lockmgr import LockMgr
from .cidr_class import (Cidr)

from .cache_files import (read_cache_file, write_cache_file, cache_file_extension)

class CidrCache:
    '''
    Class provides a cache which maps cidrs to values.
    Implemented as an ordered list of networks where each net has some assocated value
    Each elem in list is a pair of (cidr_net, value)

    data List *must* be kept sorted and compressed (no elem can be subnet of any other element)
    for search to work and work efficiently.

    We use ipaddress network as key instead of a string to for performance reasons.
    This minimizes any mapping between network and string representations.
    '''
    def __init__(self, ipt, cache_dir=None):
        self.ipt : str = ipt
        self.dirty : bool = False
        self.cache_dir : str = cache_dir
        self.data : [[IPv4Network|IPv6Network, str]] = []

        self.cache_file : str = None
        self.cache_time : int = -1
        self.lock_timeout = 120

        if self.cache_dir:
            ext = cache_file_extension()
            self.cache_file = os.path.join(cache_dir, ipt + ext)
            lockfile = choose_lock_file(cache_dir, ipt)
            self.lockmgr = LockMgr(lockfile)

    def load_cache(self):
        '''
        Read cache from file
        '''
        if not self.cache_file:
            self.data = []
            return

        got_lock = self.lockmgr.acquire_lock(wait=True, timeout=self.lock_timeout)
        if got_lock:
            self.data = read_cache_file(self.cache_file)
            if self.data:
                self.cache_time = os.path.getmtime(self.cache_file)
            self.lockmgr.release_lock()
        else:
            print(f'CIDR Cache failed to load cache : {self.cache_file}')

        if not self.data:
            self.data = []

    def write(self):
        '''
        Save to cache file
        '''
        if self.dirty:
            got_lock = self.lockmgr.acquire_lock(wait=True, timeout=self.lock_timeout)
            if got_lock:
                # Check if cache changed since we read it in
                if self.cache_time > 0:
                    cache_time_now = os.path.getmtime(self.cache_file)
                    if cache_time_now > self.cache_time:
                        print(' write cidr cache - updated since we read it - merging')
                        temp_cache = CidrCache(self.cache_dir, self.ipt)
                        if temp_cache.data:
                            self.combine_data(temp_cache.data)
                            temp_cache = None

                write_cache_file(self.data, self.cache_file)
                self.lockmgr.release_lock()
            else:
                print(f' cidr cache write failed to get lock after {self.lock_timeout}')
                print('  ** skipping writing cache')

    def sort(self):
        '''
        sort the data by network
        '''
        if not self.data or len(self.data) < 2:
            return
        self.data.sort(key=lambda elem: elem[0])

    def lookup_cidr(self, cidr:str) -> str|None:
        '''
        Look up the value associated with cidr string 

        :param cidr:
            Cidr string to lookup

        :returns:
            Value associated with the cidr string or None if not found
        '''
        net = Cidr.cidr_to_net(cidr)
        [_network, value] = self.lookup(net)
        return value

    def lookup(self, net) -> [IPv4Network|IPv6Network, str]:
        '''
        Lookup value for net
            If net isin cache then returns pair [cache_net, value].
            net is a cache_net or a subnet it.
            If not found [None, None] is returned.

        :param net:
            The network to lookup 

        :returns:
            List of (cahe_network, value) where net is cache_network or subnet of it.
            If net is not found then [None, None]
        '''
        (index, ismatch) = self.find_nearest(net)
        if ismatch:
            return self.data[index]
        return [None, None]

    def find_nearest(self, net, priv_data=None) -> (int, bool):
        '''
        Find Nearest (internal)
            find the index of the element (foundnet, value) 
            where net is a subnet of foundnet
            or the index of the element after which net would be inserted
            elem[i] <= net < elem[i+1]
            when net = elem[i] (i.e. net is subnet of elem[i]) then ismatch is True

        :returns:
            Tuple of (Index, ismatch). Index refers to cache list. Is match is True when
            net is a subnet of the cache element at index.
        '''
        data = self.data
        if priv_data is not None:
            data = priv_data
        (index, ismatch) = _find_nearest(data, net)
        return (index, ismatch)

    def add_cidr(self, cidr:str, value:str, priv_data=None):
        '''
        same as add() with input a cidr string instead of net
        '''
        net = Cidr.cidr_to_net(cidr)
        self.add(net, value, priv_data)

    def add(self, net, value, priv_data:List[[IPv4Network|IPv6Network, str]] = None):
        '''
        Add (net, value) to cache where.
            if priv_data provided then new data saved there instead of self.data
            Used when have multiple threads/processing using same CidrCache instance

            Note that if add a (cidr, value) pair exists in cache but is different - 
            then this new added version will replace the existing one. 

            Better name might be add_or_replace()

        :param net:
            ipaddress network to add to cache

        :param value:
            the value to cache with net that is associated with it

        :priv_data:
            Optional list to hold added [net, value] pairs until they can be merged 
            into the class instance data via combine_data() method. Needed if sharing
            CidrCache instance across mutliple processes/threads.

            When present, all additions are made to private data instead of instance data
            and our own data is read only until all threads/processes finish

            Once all multiple threads/processes complete, then each private data cache(s) 
            can be combined into this instance data using combine_data(priv_data)

            When private data provided the dirty flag is left alone.
            combine() will set dirty if needed. This trackes where to save 
            cache file if data has changed.

        '''
        data = self.data
        if priv_data is not None:
            data = priv_data
        else:
            self.dirty = True

        (index, ismatch) = self.find_nearest(net, data)
        if ismatch:
            #
            # net is a subnet of (or equal to) elem[i][0]
            # so keep net part and update the value
            #
            if value != data[index][1]:
                # updated value replaces existing
                if data is not None:
                    data.append([net, value])
                else:
                    data[index][1] = value
                    self.dirty = True
            return

        #
        # if index+1 is subnet of net then can be replaced by combining the 2 nets
        # If new value is different we assume its correct - so thus okay to delete
        #
        # if index+1 and net have same value check if can be merged
        #

        num_elems = len(data)
        if index < num_elems - 1 and data[index+1][0].subnet_of(net):
            del data[index+1]

        #
        # insert at index+1
        #
        data.insert(index+1, [net, value])

        #
        # Check if addition admits any network merges
        #
        _try_merge(data, index, direction=0)

    def compact(self):
        '''
        merge wherever possible - not used.
        '''
        _try_merge(self.data, 0, direction=0)

    def combine_data(self, new_data):
        '''
        Combine private data into this instance data

        :param new_data:
            List of data created by add() when provided private data list.
            All data from new_data is combined / merged into the instance data.
        '''
        if not new_data:
            return

        if not self.data:
            # this is ok as new_data was built by add() and is sorted/merged
            self.data = new_data
            return

        for item in new_data:
            self.add(item[0], item[1])

    def print(self):
        '''
        Print all the data
        '''
        if self.data:
            print(f'# {self.ipt}')
            for [net, val] in self.data:
                print(f'{net} = {val}')

def _try_merge(data, ind:int, direction:int=0):
    '''
    When new net is added it might be possible to merge some of the nets
    So, if possible merge any nets in cache which can be merged.
    The work begins at index 'ind'. Since we keep the cache ordered
    and merged we only need to do this whenever element is inserted.
    and this if i+1 cannot be merged then i+2, i+3 etc likewise.
    Ditto for i-1. So by keeping list merged and sorted we only need
    to check i+1,i-1 (and recurse if we merge anything).
    In this case an element was inserted at index 'ind'

    So we first check (ind, ind+1) - if merged then work to next higher and so on
    Then work down (ind, ind-1) similarly
    Input:
        ind : index to start merge (ie what just got inserted into list)
        direction:
            1 only merge i > index
           -1 only merge i < index
            0 merge both ways
    '''
    # pylint: disable=chained-comparison
    if ind < 0:
        return

    num_elems = len(data)
    ind_next = ind + 1
    if direction >= 0 and ind_next < num_elems:
        if data[ind][1] == data[ind_next][1]:
            try_merged = Cidr.compact_nets([data[ind][0], data[ind_next][0]])
            if len(try_merged) == 1:
                data[ind][0] = try_merged[0]
                del data[ind_next]
                _try_merge(data, ind, direction=1)

    num_elems = len(data)
    ind_prev = ind - 1
    if direction <= 0 and ind_prev >= 0:
        if data[ind][1] == data[ind_prev][1]:
            try_merged = Cidr.compact_nets([data[ind][0], data[ind_prev][0]])
            if len(try_merged) == 1:
                data[ind_prev][0] = try_merged[0]
                del data[ind]
                _try_merge(data, ind_prev, direction = -1)

def _find_nearest(data, target_net) -> (int, bool):
    '''
    Return (index, ismatch)
    ismatch True means target_net is subnet of element[index] network
    Find index of the element that matches (ismatch = True)
    or index after which net would be added to list to keep it sorted
    if net is small than first element then returns -1 so net should
    be inserted at element 0
    Algorithm is binary search.
    '''
    if not data:
        return (-1, False)

    ismatch = False
    low = 0
    high = len(data) - 1
    index = -1

    while low <= high:
        mid = (low + high) // 2

        if data[mid][0] <= target_net:
            index = mid
            low = mid + 1
        else:
            high = mid - 1

    if index >= 0:
        if target_net.subnet_of(data[index][0]):
            ismatch = True
    return (index, ismatch)

def choose_lock_file(cache_dir:str, ipt:str) -> str:
    '''
    Generate lock file to protect cache writes and reads
    lockfile in /tmp but use cache file name to ensure lock applies
    to what its needed for
    '''
    if not cache_dir:
        return None

    user = os.getlogin()
    lockdir = f'/tmp/py-cidr-{user}'
    os.makedirs(lockdir, exist_ok = True)

    lockfile = cache_dir.replace('/home/', '').replace(user, '').replace('.cache', '')
    lockfile = lockfile.lstrip('/').rstrip('/')
    lockfile = lockfile.replace('/', '-')
    lockfile = f'{lockfile}.{ipt}'

    path = os.path.join(lockdir, lockfile)
    return path

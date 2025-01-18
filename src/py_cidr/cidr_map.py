# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2024-present  Gene C <arch@sapience.com>
'''
Map cidr/ips to a (str) value.
Requires CidrCache

Keep separate caches for ipv4 and ipv6
cidr matches cache.cidr cidr when cidr is subnet of cache.cidr.

Requires CidrCache for the actual cache management
'''
from typing import (Any, Self)
from ipaddress import (IPv6Network)

from .cidr_class import (Cidr)
from .cidr_cache import CidrCache

class CidrMap:
    '''
    Class provides map(cidr) -> value
     - keeps separate ipv4 and ipv6 cache
     - built on CidrCache and Cidr classes

    :param cache_dir:
        Optional directory to save cache file
    '''
    def __init__(self, cache_dir:str = None) -> Self:
        '''
        Instantiate CidrMap instance

        '''
        self._cache_dir = cache_dir
        self._cache = {}
        self._ipts = ('ipv4', 'ipv6')

        for ipt in self._ipts:
            self._cache[ipt] = CidrCache(ipt, cache_dir=self._cache_dir)
            if self._cache_dir:
                self._cache[ipt].load_cache()

    def get_ipt(self, cidr) -> str|None:
        '''
        Identify cidr as "ipv4" or "ipv6"
        :param cidr:

            Input cidr string
        
        :returns:
            'ipv4' of 'ipv6' based on cidr
        '''
        net = Cidr.cidr_to_net(cidr)
        if not net:
            return None
        ipt = 'ipv4'
        if isinstance(net, IPv6Network):
            ipt = 'ipv6'
        return ipt

    def save_cache(self):
        ''' save cache files '''
        if not self._cache :
            return

        for ipt in self._ipts:
            if self._cache[ipt]:
                self._cache[ipt].write()

    def lookup(self, cidr:str) -> Any|None:
        '''
        Check if cidr is in cache

        :param cidr:

            Cidr value to lookup.

        :returns:

            Result if found else None
        '''
        ipt = self.get_ipt(cidr)
        if not ipt:
            return None

        result = None
        result = self._cache[ipt].lookup_cidr(cidr)
        return result

    @staticmethod
    def create_private_cache() -> dict:
        '''
        Return private cache object to use with add_cidr()
        Needed if one CidrMap instance is used across multiple processes/threads
        Give each process/thread a private data cache and they can be merged
        back into the CidrMap instance after they have all completed.
        '''
        private_cache = {
                'ipv4' : [], 
                'ipv6' : [],
                }
        return private_cache

    def add_cidr(self, cidr:str, result:str, priv_data:dict=None):
        '''
        Add cidr to cache

        :param cidr:
            Add this cidr string and its associated result value to the map.

        :param priv_data:

            If using multiple processes/threads provide this priv_data.
            so that changes are kept in private_data cache instead of instance cache.
            That way instance cache can be used across multiple processes/threads.
            Use CidrMap.create_private_cache() to create private_data

        '''
        ipt = self.get_ipt(cidr)
        if not ipt:
            return

        priv_data_ipt = None
        if priv_data :
            priv_data_ipt = priv_data[ipt]

        self._cache[ipt].add_cidr(cidr, result, priv_data_ipt)

    def merge(self, priv_data:dict):
        '''
        Merge private cache into our cache

        :param priv_data:

            If used private date to add (cidr, result) to the map, then 
            this merges content of priv_data into the current data.
        '''
        if not priv_data:
            return

        for ipt in self._ipts:
            priv_data_ipt = priv_data.get(ipt)
            if priv_data_ipt :
                self._cache[ipt].combine_data(priv_data_ipt)

    def print(self):
        '''
        Print the cache data
        '''
        for ipt in self._ipts:
            self._cache[ipt].print()

# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Map cidr/ips to a (str) value.
Requires CidrCache

Keep separate caches for ipv4 and ipv6
cidr matches cache.cidr cidr when cidr is subnet of cache.cidr.

Requires CidrCache for the actual cache management
"""
from .prefix_map import PrefixMap


class PrefixMaps:
    """
    2 x PrefixMap - 1 for ipv4 and 1 for ipv6
    Keeping separate is simpler, More efficient and avoids cross ipv4/ipv6 issues.
    """
    def __init__(self, cache_dir: str, compact: bool = False):
        self.compact: bool = compact
        self.ipv4: PrefixMap = PrefixMap(cache_dir=cache_dir, compact=compact)
        self.ipv6: PrefixMap = PrefixMap(cache_dir=cache_dir, compact=compact, ipv6=True)

        if cache_dir:
            self.ipv4.load_cache()
            self.ipv6.load_cache()

    def get_prefix_map(self, ipv6: bool = False) -> PrefixMap:
        """
        Returns the cache for ipv4 or ipv6
        Args:
            ipv6 (bool):
                If true return ipv6 cache else ipv4

        Returns:
            PrefixCache for the requested network type
        """
        if ipv6:
            return self.ipv6
        return self.ipv4

    def save_cache(self):
        """
        Save both ipv4 and ipv6 prefix maps to cache_dir
        """
        self.ipv4.save_cache()
        self.ipv6.save_cache()

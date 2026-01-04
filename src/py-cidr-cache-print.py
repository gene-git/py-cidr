#!/usr/bin/python
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Pretty print a py-cidr cache file
"""
# pylint: disable=invalid-name
import sys
from py_cidr._cidr_cache import CidrCache


def main():
    """
    Read cache dir provided on command line and print it.

    Usage: cache_dir
    """
    if len(sys.argv) < 2:
        return
    cache_dir = sys.argv[1]
    sep = 30*'-'
    for iptype in ('ipv4', 'ipv6'):
        print(f' {sep}')
        cache = CidrCache(iptype, cache_dir=cache_dir)
        cache.load_cache()
        cache.print()


if __name__ == '__main__':
    main()

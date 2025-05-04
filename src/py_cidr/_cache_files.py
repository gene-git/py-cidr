# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Read write cache file
  NB caller should implement locking as appropriate
  To Show content of pickle file use:
    python -m pickletools xxx.pkl
"""
from typing import (List)
import os
import pickle
from pickle import (PickleError)
from ._files import write_file_atomic
from ._cache_elem import (CidrCacheElem)


def read_cache_file(cache_file: str) -> List[CidrCacheElem]:
    """
    Read cache file: cache_file.pkl
    Returns cache or None if no cache.
    """
    if not cache_file or not os.path.exists(cache_file):
        return []

    try:
        cache: List[CidrCacheElem] = []
        with open(cache_file, 'rb') as fob:
            data = fob.read()
            if data:
                cache = pickle.loads(data)
        return cache

    except (OSError, PickleError) as err:
        print(f' Error reading cidr cache: {err}')
        return []


def write_cache_file(cache_elems: List[CidrCacheElem],
                     cache_file: str) -> bool:
    """
    Write pickled cache file.
    Args:
        cache_elems (List[CidrCacheElem]):
        Cache data to write

        cache_file (str):
        File to write to

    Returns:
        bool:
        Success or failure.
    """
    if not cache_elems:
        return True

    try:
        data = pickle.dumps(cache_elems)
    except PickleError as exc:
        print(f' Error saving cidr cache: {exc}')
        return False

    (okay, err) = write_file_atomic(data, cache_file)
    if not okay:
        print(f' Error saving cidr cache: {err}')
        return False
    return True


def cache_file_extension():
    """
    File extension for cache file.
    We are using pickle since cache data is a list of
    CidrCacheElem elements. This has elem.net and elem.val
    It can can be quite general.
    """
    ftype = 'pickle'
    match ftype:
        case 'json':
            return '.json'

        case 'pickle':
            return '.pkl'

        case _:
            return '.other'

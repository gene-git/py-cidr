# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Read write cache file
  NB caller should implement locking as appropriate
'''
import os
import json
import pickle
from pickle import (PickleError)
from .cidr_class import Cidr
from .files import write_file_atomic

def read_cache_file_pickle(cache_file:str) :
    '''
    Read cache file : ipt is 'ipv4' or 'ipv6'
    Returns cache or None if no cache
    '''
    if not os.path.exists(cache_file):
        return None

    try:
        cache = None
        with open(cache_file, 'rb') as fob:
            data = fob.read()
            if data:
                cache = pickle.loads(data)
        return cache

    except (OSError, PickleError) as err:
        print(f' Error reading cidr cache: {err}')
        return None

def write_cache_file_pickle(cache, cache_file):
    '''
    Write pickled cache file
    '''
    if not cache:
        return

    try:
        data = pickle.dumps(cache)
    except PickleError as err:
        print(f' Error saving cidr cache: {err}')
        return

    (okay, err) = write_file_atomic(data, cache_file)
    if not okay:
        print(f' Error saving cidr cache: {err}')


def read_cache_file_json(cache_file:str) :
    '''
    Read cache file : ipt is 'ipv4' or 'ipv6'
    Returns cache or None if no cache
    '''
    if not os.path.exists(cache_file):
        return None

    try:
        cache = None
        with open(cache_file, 'r', encoding='utf-8') as fob:
            data = fob.read()
            if data:
                cache = json.loads(data)
        return cache

    except (OSError, ValueError) as err:
        print(f' Error reading cidr cache: {err}')
        return None

def write_cache_file_json(cache, cache_file):
    '''
    Write json cache file
    '''
    if not cache:
        return

    try:
        data = json.dumps(cache)
    except ValueError as err:
        print(f' Error saving cidr cache: {err}')
        return

    (okay, err) = write_file_atomic(data, cache_file)
    if not okay:
        print(f' Error saving cidr cache: {err}')

def read_cache_file(file, ftype:str='json'):
    '''
    Read cache
    '''
    match(ftype):
        case 'json':
            data = read_cache_file_json(file)

        case 'pickle':
            data = read_cache_file_pickle(file)

        case _:
            print(f' read_cache: Unknown file type {ftype}')
            data = None

    if not data:
        return None

    cache = []
    for item in data:
        net = Cidr.cidr_to_net(item[0])
        val = item[1]
        cache.append([net, val])

    return cache

def write_cache_file(cache, file, ftype:str='json'):
    '''
    Read cache
    '''
    if not cache:
        return None

    # convert net to strings takes less space and json cant handle net
    data = []
    for item in cache:
        data.append([str(item[0]), item[1]])

    match ftype:
        case 'json':
            write_cache_file_json(data, file)

        case 'pickle':
            write_cache_file_pickle(data, file)

        case _:
            print(f' write_cache: Unknown file type {ftype}')
            cache = None

    return cache

def cache_file_extension(ftype:str='json'):
    '''
    File extension to use based on fype
    '''
    match ftype:
        case 'json':
            return '.json'

        case 'pickle':
            return '.pickle'

        case _:
            return '.other'

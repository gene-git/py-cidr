# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
'''
Some cidr utilities 
'''
from .cidr_class import (Cidr, IPvxNetwork)

def is_valid_ip4(address:str) -> bool:
    ''' check if valid address or cidr '''
    return Cidr.is_valid_ip4(address)

def is_valid_ip6(address:str) -> bool:
    ''' check if valid address or cidr '''
    return Cidr.is_valid_ip6(address)

def is_valid_cidr(address:str) -> bool:
    '''
    check if valid ip address
     - returns True/False
    '''
    return Cidr.is_valid_cidr(address)

def cidr_iptype(address:str) -> str|None :
    '''
    Input:
        ip address or cidr string
     Output
        'ip4' or 'ip6' or None
    '''
    return Cidr.cidr_iptype(address)

def cidr_type_network(cidr:str) -> (str, IPvxNetwork):
    '''
    returns ip type (ip4, ip6) along with IPv4Network or IPv6Network
    '''
    return Cidr.cidr_type_network(cidr)

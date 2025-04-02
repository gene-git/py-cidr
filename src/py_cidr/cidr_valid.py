# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Support for type checks
'''
import ipaddress
from ipaddress import (IPv4Address, IPv6Address, IPv4Network, IPv6Network)
from ipaddress import (AddressValueError, NetmaskValueError)

from .cidr_types import (IPvxAddress, IPvxNetwork)

def is_valid_ip4(address) -> bool:
    ''' check if valid address or cidr '''
    try:
        _check = IPv4Network(address, strict=False)
        return True
    except (AddressValueError, NetmaskValueError, ValueError, TypeError):
        return False

def is_valid_ip6(address) -> bool:
    ''' check if valid address or cidr '''
    try:
        _check = IPv6Network(address, strict=False)
        return True
    except (AddressValueError, NetmaskValueError, ValueError, TypeError):
        return False

def is_valid_cidr(address) -> bool:
    '''
    Valid Address or Network
        check if valid ip address or cidr network

    :param address:
        IP or Cidr string to check. Host bits being set is permitted for a cidr network.

    :returns:
        True/False if address is valid
    '''
    if not address:
        return False
    try:
        _check = ipaddress.ip_network(address, strict=False)
        return True
    except (AddressValueError, NetmaskValueError, ValueError, TypeError):
        return False

def cidr_iptype(address:str) -> str|None :
    '''
    Determines if an IP address or CIDR string is ipv4 or ipv6

    :param address:
        ip address or cidr string

     :returns:
        'ip4' or 'ip6' or None
    '''
    if not address:
        return None

    if is_valid_ip4(address) :
        return 'ip4'

    if is_valid_ip6(address):
        return 'ip6'

    return None

def address_iptype(addr:IPvxAddress|IPvxNetwork) -> str|None:
    '''
    Address Type
        Identify if IP address (IPvxAddres) or net (IPvxNetwork) is ipv4 or ipv6

    :param addr:
        IP address or cidr network .

    :returns:
        'ip4', 'ip6' or None
    '''
    if not addr:
        return None
    ipt = type(addr)
    if ipt in (IPv4Address,IPv4Network):
        return 'ip4'
    if ipt in (IPv6Address,IPv6Network):
        return 'ip6'
    return None

def cidr_type_network(cidr:str) -> (str, IPvxNetwork):
    '''
    Cidr Network Type:

    :param cidr:
        Cidr string to examine

    :returns:
        Tuple(ip-type, net-type). ip-type is a string  ('ip4', 'ip6') while
        network type is IPv4Network or IPv6Network
    '''
    ipt = None
    IPNetwork = IPv4Network

    if is_valid_ip4(cidr):
        ipt = 'ip4'
        IPNetwork = IPv4Network

    elif is_valid_ip6(cidr):
        ipt = 'ip6'
        IPNetwork = IPv6Network

    return (ipt, IPNetwork)

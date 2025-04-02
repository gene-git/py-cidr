# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Class support functions for cidr addresses
'''
import ipaddress
import re
from ipaddress import (AddressValueError)
from ipaddress import (IPv4Network, IPv6Network)

from .cidr_types import (IPvxAddress)
from .cidr_valid import (is_valid_ip4, is_valid_ip6)

def ip_to_address(ip:str) -> IPvxAddress|None:
    '''
    IP to Address
        Return ipaddress of given ip.
        If IP has prefix or host bits set, we strip the prefix first and keep host bits

    :param ip:
        The IP string to convert

    :returns:
        IPvxAddress derived from IP or None if not an IP address
    '''
    if not ip:
        return None

    ipin = ip
    if '/' in ip:
        ipin = re.sub(r'/.*$', '',  ip)

    try:
        addr = ipaddress.ip_address(ipin)
    except AddressValueError:
        addr = None
    return addr

def ips_to_addresses(ips:[str]) -> [IPvxAddress]:
    '''
    IPs to Addresses
        Convert list of IP strings to a list of ip addresses

    :param ips:
        List of IP strings to convert

    :returns:
        List of IPvxAddress derived from input IPs.
    '''
    addresses = [ip_to_address(ip) for ip in ips]
    return addresses

def addresses_to_ips(addresses:[IPvxAddress]) -> [str]:
    '''
    Address to IP strings
        For list of IPs in ipaddress format, return list of ip strings

    :param addresses:
        List of IP addresses in ipaddress format

    :returns:
        List of IP strings
    '''
    ips = [str(address) for address in addresses]
    return ips

def ipaddr_cidr_from_string(addr:str, strict:bool=False) -> IPv4Network | IPv6Network | None:
    '''
    IP/CIDR to IPvxNetwork
        Convert string of IP address or cidr net to IPvxNetwork

    :param address:
        String of IP or CIDR network.

    :param strict:
        If true, host bits disallowed for cidr block.

    :returns:
        An IPvXNetwork or None if not valid.
    '''
    if not addr:
        return None
    if is_valid_ip4(addr):
        return ipaddress.IPv4Network(addr, strict=strict)
    if is_valid_ip6(addr):
        return ipaddress.IPv6Network(addr, strict=strict)
    return None

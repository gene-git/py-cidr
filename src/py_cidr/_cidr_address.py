# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Class support functions for cidr addresses
"""
import ipaddress
import re
from ipaddress import (AddressValueError)

from .cidr_types import (IPvxAddress, IPvxNetwork)
from ._cidr_valid import (is_valid_ip4, is_valid_ip6)


def ip_to_address(ip: str) -> IPvxAddress | None:
    """
    Return ipaddress of given ip string.

    If ip has prefix or host bits set, the prefix first stripped and
    host bits are retained.

    :param ip:
        The IP string to convert

    :returns:
        IPvxAddress derived from IP or None if not an IP address
    """
    if not ip:
        return None

    ipin = ip
    if '/' in ip:
        ipin = re.sub(r'/.*$', '',  ip)

    try:
        addr = ipaddress.ip_address(ipin)
    except AddressValueError:
        return None
    return addr


def ips_to_addresses(ips: list[str]) -> list[IPvxAddress]:
    """
    Convert list of IP strings to a list of ip addresses.

    :param ips:
        list of IP strings to convert

    :returns:
        list of IPvxAddress derived from input IPs.
    """
    addresses = [ip_to_address(ip) for ip in ips]
    good_addresses = [ip for ip in addresses if ip is not None]
    return good_addresses


def addresses_to_ips(addresses: list[IPvxAddress]) -> list[str]:
    """
    Address to IP strings
        For list of IPs in ipaddress format, return list of ip strings

    :param addresses:
        list of IP addresses in ipaddress format

    :returns:
        list of IP strings
    """
    ips = [str(address) for address in addresses]
    return ips


def ipaddr_cidr_from_string(addr: str, strict: bool = False
                            ) -> IPvxNetwork | None:
    """
    Convert string with IP address or cidr net to an IPvxNetwork.

    :param address:
        String of IP or CIDR network.

    :param strict:
        If true, host bits disallowed for cidr block.

    :returns:
        An IPvXNetwork or None if not valid.
    """
    if not addr:
        return None
    if is_valid_ip4(addr):
        return ipaddress.IPv4Network(addr, strict=strict)
    if is_valid_ip6(addr):
        return ipaddress.IPv6Network(addr, strict=strict)
    return None

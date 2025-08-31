# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2025-present  Gene C <arch@sapience.com>
"""
Split list of networks by type
"""
from ipaddress import (IPv4Address, IPv4Network, IPv6Address, IPv6Network)

from .cidr_types import (IPvxNetwork, IPv4, IPv6)
from ._cidr_valid import is_valid_ip4
from ._cidr_valid import is_valid_ip6


def cidrs_split_type(cidrs: list[str]
                     ) -> tuple[list[str], list[str], list[str]]:
    """
    Split a list of cidrs into ipv4, ipv6 and other
    Args:
        cidrs (list[str]):
            list of cidr strings
    Returns:
        tuple[ip4: list[str], ip6: list[str], other: list[str]]
        Tuple of lists of ipv4, ipv6 and unknown.
    """
    ip4: list[str] = []
    ip6: list[str] = []
    oth: list[str] = []

    if not cidrs:
        return (ip4, ip6, oth)

    for cidr in cidrs:
        if is_valid_ip4(cidr):
            ip4.append(cidr)

        elif is_valid_ip6(cidr):
            ip6.append(cidr)

        else:
            oth.append(cidr)

    return (ip4, ip6, oth)


def nets_split_type(nets: list[IPvxNetwork]) -> tuple[list[IPv4], list[IPv6]]:
    """
    Split a list of cidrs into ipv4, ipv6 and other
    Args:
        cidrs (list[str]):
            list of cidr strings
    Returns:
        tuple[ip4: list[str], ip6: list[str], other: list[str]]
        Tuple of lists of ipv4, ipv6 and unknown.
    """
    ip4: list[IPv4] = []
    ip6: list[IPv6] = []

    if not nets:
        return (ip4, ip6)

    for net in nets:
        ipt = type(net)
        if ipt in (IPv4Address, IPv4Network):
            ip4.append(net)     # type: ignore[arg-type]

        elif ipt in (IPv6Address, IPv6Network):
            ip6.append(net)     # type: ignore[arg-type]

    return (ip4, ip6)

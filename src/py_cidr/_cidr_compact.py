# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Class support functions to compact lists of cidrs/nets
NB ipaddress.collapse_addresses is known to trigger type hint errors.
   Check no erorrs other than collapse_addresses() then add the ignore.
"""
# mypy:  disable-error-code=type-var
import ipaddress

from .cidr_types import (IPvxNetwork)
from ._cidr_nets import (cidrs_to_nets, nets_to_cidrs)
from ._cidr_split_type import cidrs_split_type


def cidr_list_compact(cidrs: list[str],
                      to_cidrs: bool = True) -> list[str] | list[IPvxNetwork]:
    """
    Deprecated function.
    Compact list of cidr networks to smallest list possible.

    :param cidrs:
        list of cidr strings to compact.

    :param to_cidrs:
        If true (default) returns list of strings, else a list of IPvxNetworks

    :returns:
        Compressed list of cidrs as ipaddress networks (string=False)
        or list of strings when string=True
    """
    print('** Warning cidr_list_compact deprecated')
    if to_cidrs:
        print('   Use compact_cidrs')
        return compact_cidrs(cidrs)
    print('   Use compact_cidrs_to_nets')
    return compact_cidrs_to_nets(cidrs)


def compact_nets(nets: list[IPvxNetwork]) -> list[IPvxNetwork]:
    """
    Compact list of networks and return netorks

    Args:
        cidrs (list(IPvxNetwork):
            list of networks

    Returns:
        list[IPvxNetwork]:
            list of compacted IPvxNetworks
    """
    if not nets:
        return []

    try:
        nets_compact = list(ipaddress.collapse_addresses(nets))
        return nets_compact
    except (TypeError, ValueError) as exc:
        raise TypeError('**Error: Bad IPv4/IPv6 net or mixed types') from exc


def compact_cidrs_to_nets(cidrs: list[str]) -> list[IPvxNetwork]:
    """
    Compact list of cidr strings and return as list of netorks

    Args:
        cidrs (list(str):
        list of cidr strings

    Returns:
        list[IPvxNetwork]:
        list of IPvxNetworks
    """
    if cidrs is None or len(cidrs) < 1:
        # raise ValueError('Missing input: list of cidrs ')
        return []

    nets = cidrs_to_nets(cidrs, strict=False)
    nets = compact_nets(nets)
    return nets


def compact_cidrs(cidrs: list[str]) -> list[str]:
    """
    Compact list of cidrs to smallest list possible.
    Any bad cidr will raise ValueError

    Args:
        cidrs (list[str]):
            list of cidr strings to compact.

    Returns:
        list[str]:
            Compact list of cidr strings
    """
    cidrs_compact: list[str] = []
    if not cidrs:
        return cidrs_compact

    (ip4, ip6, oth) = cidrs_split_type(cidrs)

    # if oth:
    #     raise ValueError('Bad cidr input invalid')

    if ip4:
        nets = compact_cidrs_to_nets(ip4)
        cidrs_compact += nets_to_cidrs(nets)

    if ip6:
        nets = compact_cidrs_to_nets(ip6)
        cidrs_compact += nets_to_cidrs(nets)

    if oth:
        # could have host bits set.
        nets = compact_cidrs_to_nets(oth)
        cidrs_compact += nets_to_cidrs(nets)

    return cidrs_compact

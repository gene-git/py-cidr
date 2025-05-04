# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Class support functions for networks
"""
from typing import (List)
import ipaddress

from .cidr_types import (IPvxNetwork)


def cidr_to_net(cidr: str, strict: bool = False) -> IPvxNetwork | None:
    """
    Convert cidr string to ipaddress network.

    :param cidr:
        Input cidr string

    :param strict:
        If true then cidr is considered invalid if host bits are set.
        Defaults to False. (see ipaddress docs).

    :returns:
        The ipaddress network derived from cidr string
        as either IPvxNetwork = IPv4Network or IPv6Network.
    """
    if not cidr:
        return None

    return ipaddress.ip_network(cidr, strict=strict)


def cidrs_to_nets(cidrs: List[str], strict: bool = False) -> List[IPvxNetwork]:
    """
    Convert list of cidr strings to list of IPvxNetwork.

    :param cidrs:
        List of cidr strings

    :param strict:
        If true, then any cidr with host bits is invalid. Defaults to false.

    :returns:
        List of IPvxNetworks.
    """
    if cidrs is None or len(cidrs) < 1:
        return []

    try:
        nets = [ipaddress.ip_network(cidr, strict=strict) for cidr in cidrs]
        return nets

    except ipaddress.AddressValueError as exc:
        raise ValueError from exc


def nets_to_cidrs(nets: List[IPvxNetwork]) -> List[str]:
    """
    Nets to Strings
        Convert list of ipaddress networks to list of cidr strings.

    :param nets:
        List of nets to convert

    :returns:
        List of cidr strings
    """
    if nets is None or len(nets) < 1:
        return []
    cidrs = [str(net) for net in nets]
    return cidrs

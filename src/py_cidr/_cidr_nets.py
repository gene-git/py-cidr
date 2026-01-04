# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Class support functions for networks
"""
import ipaddress
from ipaddress import (IPv4Address, IPv6Address, IPv4Network, IPv6Network)

from .cidr_types import (IPAddress, IPvxNetwork)


def address_to_net(addr: IPAddress | IPvxNetwork, strict: bool = False
                   ) -> IPvxNetwork | None:
    """
    Convert an address to IPvxNetwork.

    Be flexible with input address. Can be
    IPAddress (includes string) or even IPvxNetwork.

    Args:
        addr (IPAddress | IPvxNetwork):
            Input address.

        strict (bool):
            If true then cidr is considered invalid if host bits are set.
            Defaults to False. (see ipaddress docs).

    Returns:
        IPvxNetwork | None:
            The IPvxNetwork derived from input "addr" or None if
            not an address/network.
    """
    if not addr or addr is None:
        return None

    if isinstance(addr, (IPv4Network, IPv6Network)):
        return addr

    if isinstance(addr, (str, IPv4Address, IPv6Address)):
        return ipaddress.ip_network(addr, strict=strict)

    return None


def cidr_to_net(cidr: str, strict: bool = False) -> IPvxNetwork | None:
    """
    Convert cidr string to ipaddress network.

    Special case of address_to_net.

    Args:
        cidr (str):
            Input cidr string

        strict (bool):
            If true then cidr is considered invalid if host bits are set.
            Defaults to False. (see ipaddress docs).

    Returns:
        IPvxNetwork | None:
            The ipaddress network derived from cidr string
            as either IPvxNetwork = IPv4Network or IPv6Network.
    """
    if not cidr:
        return None

    return ipaddress.ip_network(cidr, strict=strict)


def cidrs_to_nets(cidrs: list[str], strict: bool = False) -> list[IPvxNetwork]:
    """
    Convert list of cidr strings to list of IPvxNetwork.

    :param cidrs:
        list of cidr strings

    :param strict:
        If true, then any cidr with host bits is invalid. Defaults to false.

    :returns:
        list of IPvxNetworks.
    """
    if cidrs is None or len(cidrs) < 1:
        return []

    try:
        nets = [ipaddress.ip_network(cidr, strict=strict) for cidr in cidrs]
        return nets

    except ipaddress.AddressValueError as exc:
        raise ValueError from exc


def nets_to_cidrs(nets: list[IPvxNetwork]) -> list[str]:
    """
    Nets to Strings
        Convert list of ipaddress networks to list of cidr strings.

    :param nets:
        list of nets to convert

    :returns:
        list of cidr strings
    """
    if nets is None or len(nets) < 1:
        return []
    cidrs = [str(net) for net in nets]
    return cidrs


def net_to_cidr(net: IPvxNetwork) -> str:
    """
    Net to Cidr String
        Convert an ipaddress network to a cidr string.

    Args:
        net (IPvxNetwork):
            Ipaddress Network to convert.

    Returns:
        str:
        Cidr string from net. If unable to conver,
        then empty string is returned.
    """
    if not net:
        return ''

    cidr = str(net)
    return cidr

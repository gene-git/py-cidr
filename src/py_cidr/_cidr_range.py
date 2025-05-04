# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Class support functions for range of cidrs
"""
from typing import (List, Tuple)
import ipaddress
from ipaddress import (IPv4Address, IPv6Address)
from .cidr_types import (IPvxNetwork, IPvxAddress, IPAddress)
from ._cidr_nets import (cidr_to_net)


def range_to_nets(start: IPAddress, end: IPAddress) -> List[IPvxNetwork]:
    """
    Generate a list of cidr/nets from an IP range.

    :param start:
        Start of IP range as IPAddress (IPv4Address,  IPv6Address or string)

    :param end:
        End of IP range as IPAddress (IPv4Address,  IPv6Address or string)

    :param string:
        If True then returns list of cidr strings otherwise IPvxNetwork

    :returns:
        List of cidr network blocks representing the IP range.
        List elements are IPvxAddress or str if parameter string=True
    """
    # pylint: disable=unnecessary-comprehension
    if isinstance(start, str):
        start = ipaddress.ip_address(start)

    if isinstance(end, str):
        end = ipaddress.ip_address(end)

    ipv4 = isinstance(start, IPv4Address) and isinstance(end, IPv4Address)
    ipv6 = isinstance(end, IPv6Address) and isinstance(end, IPv6Address)

    if ipv4 or ipv6:
        nets = [net for net in ipaddress.summarize_address_range(start, end)]
    else:
        raise TypeError('range_to_cidrs error: IP types must be same')

    return nets


def range_to_cidrs(start: IPAddress, end: IPAddress) -> List[str]:
    """
    Generate a list of cidr/nets from an IP range.

    :param start:
        Start of IP range as IPAddress (IPv4Address,  IPv6Address or string)

    :param end:
        End of IP range as IPAddress (IPv4Address,  IPv6Address or string)

    :param string:
        If True then returns list of cidr strings otherwise IPvxNetwork

    :returns:
        List of cidr network blocks representing the IP range.
        List elements are IPvxAddress or str if parameter string=True
    """
    nets = range_to_nets(start, end)
    cidrs = [str(cidr) for cidr in nets]
    return cidrs


def net_to_range_nets(net: IPvxNetwork
                      ) -> Tuple[IPvxAddress | None, IPvxAddress | None]:
    """
    Network to IP Range

    :param net:
        The ipaddress network (IPvxNetwork) to examine

    :param string:
        If True then returns cidr strings instead of IPvxAddress

    :returns:
        Tuple (ip0, ip1) of first and last IP address in net
        (ip0, ip1) are IPvxAddress or str when string is True
    """
    if not net:
        return (None, None)

    addr_start = net.network_address
    addr_end = net.broadcast_address
    return (addr_start, addr_end)


def net_to_range_cidrs(net: IPvxNetwork
                       ) -> Tuple[str | None, str | None]:
    """
    Network to IP Range

    :param net:
        The ipaddress network (IPvxNetwork) to examine

    :param string:
        If True then returns cidr strings instead of IPvxAddress

    :returns:
        Tuple (ip0, ip1) of first and last IP address in net
        (ip0, ip1) are IPvxAddress or str when string is True
    """
    if not net:
        return (None, None)
    (addr_start, addr_end) = net_to_range_nets(net)
    return (str(addr_start), str(addr_end))


def cidr_to_range_nets(cidr: str
                       ) -> Tuple[IPvxAddress | None, IPvxAddress | None]:
    """
    Cidr string to an IP Range

    :param cidr:
        The cidr string to examine

    :returns:
        Tuple (ip0, ip1) of first and last IP address in net
        (ip0, ip1) are each IPvxAddress.
    """
    net = cidr_to_net(cidr, strict=False)
    if not net:
        return (None, None)
    return net_to_range_nets(net)


def cidr_to_range_cidrs(cidr: str
                        ) -> Tuple[str | None, str | None]:
    """
    Cidr string to an IP Range

    :param cidr:
        The cidr string to examine

    :returns:
        Tuple (ip0, ip1) of first and last IP address in net
        (ip0, ip1) are each a cidr str
    """
    net = cidr_to_net(cidr, strict=False)
    if not net:
        return (None, None)
    return net_to_range_cidrs(net)

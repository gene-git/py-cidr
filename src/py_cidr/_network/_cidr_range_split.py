# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Tool to split a valid network into 3 IP addresses
"""
import ipaddress

from .cidr_types import (IPvxAddress, IPvxNetwork)
from ._cidr_valid import is_valid_cidr
from ._cidr_nets import cidr_to_net


def net_range_split(net: IPvxNetwork) -> tuple[IPvxAddress, IPvxAddress, IPvxAddress]:
    """
    Take a valid network and split it into 3 ip addresses:
    - ip_first
    - ip_mid
    - ip_last
    Being the first, mid and last ip in the block
    NB No input validation is performed

    Input:
        net (IPvxNetwork):
            A valid network

    Returns
        tuple[ip_first: IPvxAddress, ip_mid: IPvxAddress, ip_last: IPvxAddress]
            The first ip, the middle ip and the last ip.
    """
    ip0: IPvxAddress = net.network_address
    ip1 = net.broadcast_address

    ip_num = int(ip0) + int((int(ip1) - int(ip0))/2)
    ip_mid = ipaddress.ip_address(ip_num)

    return (ip0, ip_mid, ip1)


def cidr_range_split(cidr: str) -> tuple[str, str, str]:
    """
    Take a valid network and split it into 3 ip addresses:
    - ip_first
    - ip_mid
    - ip_last
    Being the first, mid and last ip in the block
    NB No input validation is performed

    Input:
        net (IPvxNetwork):
            A valid network

    Returns
        tuple[cidr_first: str, cidr_mid: str, cidr_last: str]
            The first ip, the middle ip and the last ip.
            Each address is a returned as a string without any prefix
            for example '10.0.2.1'
    """
    if not (cidr and is_valid_cidr(cidr)):
        return ('', '', '')

    net = cidr_to_net(cidr)
    if net is None:
        return ('', '', '')

    ip_first: IPvxAddress
    ip_mid: IPvxAddress
    ip_last: IPvxAddress

    (ip_first, ip_mid, ip_last) = net_range_split(net)

    return (str(ip_first), str(ip_mid), str(ip_last))

# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Support for type checks
"""
from typing import (Any)
import ipaddress
from ipaddress import (IPv4Address, IPv6Address, IPv4Network, IPv6Network)
from ipaddress import (AddressValueError, NetmaskValueError)

from .cidr_types import (IPvxAddress, IPvxNetwork)
from ._cidr_nets import cidr_to_net


def _ip_version(addr: IPvxNetwork | IPvxAddress) -> int:
    """
    Args:
        addr (IPvxNetwork | IPvxAddress):
            IP address or IP Network

    Returns:
        int:
            4 if addr_or_net is IPv4Network or IPv4Address
            6 if addr_or_net is IPv6Network or IPv5Address
            0 otherwise
    """
    try:
        return addr.version

    except (AddressValueError, NetmaskValueError, ValueError, TypeError):
        pass
    return 0


def ip_version(addr_or_net: str | IPvxNetwork | IPvxAddress) -> int:
    """
    Returns 4 if addr_or_net is IPv4Network or IPv4Address
            6 if addr_or_net is IPv6Network or IPv5Address
            0 otherwise
    """
    if not addr_or_net:
        return 0

    if isinstance(addr_or_net, str):
        net = cidr_to_net(addr_or_net)
        if net is not None:
            return _ip_version(net)
        return 0

    return _ip_version(addr_or_net)

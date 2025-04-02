# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Class support functions to compact lists of cidrs/nets
'''
import ipaddress

from .cidr_types import (IPvxNetwork)

def cidr_list_compact(cidrs_in:[str], string=True) -> [str|IPvxNetwork]:
    """
    Cidr Compact:
        Compact list of cidr networks to smallest list possible.

    :param cidrs_in:
        List of cidr strings to compact.

    :param string:
        If true (default) returns list of strings, else a list of IPvxNetworks

    :returns:
        Compressed list of cidrs as ipaddress networks (string=False)
        or list of strings when string=True
    """
    if not cidrs_in:
        return cidrs_in

    ip_nets = [ipaddress.ip_network(cidr, strict=False) for cidr in cidrs_in]
    cidrs_out = []
    for cidr in ipaddress.collapse_addresses(ip_nets):
        if string:
            cidrs_out.append(str(cidr))
        else:
            cidrs_out.append(cidr)
    return cidrs_out

def compact_cidrs(cidrs:[str], nets=False) -> [str|IPvxNetwork]:
    ''' combine em '''
    ip_nets = [ipaddress.ip_network(cidr, strict=False) for cidr in cidrs]
    if nets:
        return ip_nets
    compact = [str(net) for net in ipaddress.collapse_addresses(ip_nets)]
    return compact

def compact_nets(nets:[IPvxNetwork]) -> [IPvxNetwork]:
    ''' combine em '''
    compact = list(ipaddress.collapse_addresses(nets))
    return compact

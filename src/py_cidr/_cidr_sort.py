# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Class support functions to sort lists of cidrs/nets
"""
import ipaddress

from .cidr_types import IPvxNetwork
from ._cidr_nets import (cidrs_to_nets, nets_to_cidrs)
from ._cidr_address import (ips_to_addresses, addresses_to_ips)


def sort_cidrs(cidrs: list[str]) -> list[str]:
    """
    Sort the list of cidr strings.
    """
    nets = cidrs_to_nets(cidrs)
    if not nets:
        return cidrs

    key_ip = ipaddress.get_mixed_type_key
    nets.sort(key=key_ip)                           # type: ignore[arg-type]
    cidrs_sorted = nets_to_cidrs(nets)
    return cidrs_sorted


def sort_ips(ips: list[str]) -> list[str]:
    """
    Sort the list of cidr strings.
    """
    addresses = ips_to_addresses(ips)

    key_ip = ipaddress.get_mixed_type_key
    addresses.sort(key=key_ip)                      # type: ignore[arg-type]
    ips_sorted = addresses_to_ips(addresses)
    return ips_sorted


def sort_nets(nets: list[IPvxNetwork]) -> list[IPvxNetwork]:
    """
    Sort list of networks.
    """
    nets_sorted: list[IPvxNetwork] = []
    if not nets:
        return nets_sorted

    key_ip = ipaddress.get_mixed_type_key
    nets_sorted = sorted(nets, key=key_ip)          # type: ignore[arg-type]
    return nets_sorted

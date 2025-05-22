# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Class support functions to sort lists of cidrs/nets
"""
import ipaddress

from ._cidr_nets import (cidrs_to_nets, nets_to_cidrs)
from ._cidr_address import (ips_to_addresses, addresses_to_ips)


def sort_cidrs(cidrs: list[str]) -> list[str]:
    """
    Sort the list of cidr strings.
    """
    nets = cidrs_to_nets(cidrs)
    if not nets:
        return cidrs
    nets.sort(key=ipaddress.get_mixed_type_key)     # type: ignore[arg-type]
    cidrs_sorted = nets_to_cidrs(nets)
    return cidrs_sorted


def sort_ips(ips: list[str]) -> list[str]:
    """
    Sort the list of cidr strings.
    """
    addresses = ips_to_addresses(ips)
    addresses.sort(key=ipaddress.get_mixed_type_key)  # type: ignore[arg-type]
    ips_sorted = addresses_to_ips(addresses)
    return ips_sorted

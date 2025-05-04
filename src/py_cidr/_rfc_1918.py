# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Tools interacting with RFC 1918
"""
# pylint: disable=invalid-name
from typing import (List, Tuple)
from .cidr_types import IPvxNetwork
from ._cidr_subnet import (cidr_is_subnet)
from ._cidr_nets import (cidrs_to_nets)


def is_rfc_1918(cidr: str) -> bool:
    """
    Check if cidr is any RFC 1918.

    Args:
        cidr (str):
        IP or Cidr to check if RFC 1918

    Returns:
        bool:
        True if cidr is an RGC 1918 address
        False if not.
    """
    if not cidr:
        return False

    rfc_1918 = rfc_1918_nets()
    if cidr_is_subnet(cidr, rfc_1918):
        return True
    return False


def rfc_1918_nets() -> List[IPvxNetwork]:
    """
    Return list of rfc 1918 networks.

    Returns:
        List[IPvxNetwork]:
        List of all RFC 1918 networks. Each element is ipaddress.IPv4Network
    """
    rfc_1918_str = rfc_1918_cidrs()
    rfc_1918 = cidrs_to_nets(rfc_1918_str)
    return rfc_1918


def rfc_1918_cidrs() -> List[str]:
    """
    Return list of rfc 1918 networks cidr strings.

    Returns:
        List[str]:
        List of RFC 1918 networks as cidr strings
    """
    rfc_1918s = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
    return rfc_1918s


def remove_rfc_1918(cidrs_in: str | List[str]
                    ) -> Tuple[str | List[str], str | List[str]]:
    """
    Given list of cidrs, return list without any rfc 1918.

    Args:
        cidrs_in (str | List[str])::
        Cidr string or list of cidr strings.

    Returns:
        Tuple[str | List[str], str | List[str]]:
        Returns (cidrs_cleaned, rfc_1918_cidrs_found):

        - cidrs_cleaned = list of cidrs with all rfc_1918 removed
        - rfc_1918_cidrs_found = list of rfc 1918 found in the input cidr(s)

        If input a list, then output will be a list (possibly empty).
        If input cidr not a list then returned items will be string or None.

    """
    if cidrs_in is None:
        return (None, None)
    if not cidrs_in:
        return (cidrs_in, [])

    rfc_1918 = rfc_1918_nets()

    #
    # input is list of cidrs
    #
    if isinstance(cidrs_in, list):
        found_1918 = []

        found_1918 = [
                cidr for cidr in cidrs_in
                if cidr_is_subnet(cidr, rfc_1918)
                ]
        if found_1918:
            set_1918 = set(found_1918)
            set_orig = set(cidrs_in)
            cleaned = list(set_orig - set_1918)
            return (cleaned, found_1918)
        return (cidrs_in, [])

    # input is one cidr
    if cidr_is_subnet(cidrs_in,  rfc_1918):
        return ('', cidrs_in)
    return (cidrs_in, [])

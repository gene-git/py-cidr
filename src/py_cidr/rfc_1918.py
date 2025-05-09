# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Tools interacting with RFC 1918
'''
# pylint: disable=invalid-name
from typing import List
from ipaddress import (IPv4Network)
from .cidr_subnet import (cidr_is_subnet)
from .cidr_nets import (cidrs_to_nets)

def is_rfc_1918(cidr: str) -> bool:
    '''
    Check if cidr is any RFC 1918

    :param cidr:
        IP or Cidr to check if RFC 1918

    :returns:
        True if cidr is an RGC 1918 address
        False if not.
    '''
    if not cidr:
        return False

    rfc_1918 = rfc_1918_nets()
    if cidr_is_subnet(cidr, rfc_1918):
        return True
    return False

def rfc_1918_nets() -> [IPv4Network]:
    '''
    Return list of rfc 1918 networks

    :returns:
        List of all RFC 1918 networks. Each element is ipaddress.IPv4Network
    '''
    rfc_1918_str = rfc_1918_cidrs()
    rfc_1918 = cidrs_to_nets(rfc_1918_str)
    return rfc_1918

def rfc_1918_cidrs() -> [str]:
    '''
    Return list of rfc 1918 networks cidr strings

    :returns:
        List of RFC 1918 networks as cidr strings
    '''
    rfc_1918s = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
    return rfc_1918s

def remove_rfc_1918(cidrs_in: str|List[str]) -> (str|List[str], str|List[str]):
    '''
    Given list of cidrs, return list without any rfc 1918

    :param cidrs_in:
        Cidr string or list of cidr strings.

    :returns:
        Returns (cidrs_cleaned, rfc_1918_cidrs_found)
        cidrs_cleaned = list of cidrs with all rfc_1918 removed
        rfc_1918_cidrs_found = list of any rfc 1918 found in the input cidr(s)
        If input cidr(s) is a list, then output will be a list (possibly empty).
        If input cidr not a list then returned items will be string or None.
    '''
    if cidrs_in is None:
        return (None, None)
    if not cidrs_in :
        return (cidrs_in, [])

    rfc_1918 = rfc_1918_nets()

    #
    # input is list of cidrs
    #
    if isinstance(cidrs_in, list):
        found_1918 = []

        found_1918 = [cidr for cidr in cidrs_in if cidr_is_subnet(cidr, rfc_1918)]
        if found_1918:
            set_1918 = set(found_1918)
            set_orig = set(cidrs_in)
            cleaned = list(set_orig - set_1918)
            return (cleaned, found_1918)
        return (cidrs_in, found_1918)

    # input is one cidr
    if cidr_is_subnet(cidrs_in,  rfc_1918):
        return (None, cidrs_in)
    return (cidrs_in, None)

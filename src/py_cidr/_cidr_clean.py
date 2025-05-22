# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Class support functions to clean/tidy cidrs
"""
from ._cidr_valid import (is_valid_cidr)
from ._cidr_nets import (cidr_to_net)


def clean_cidr(cidr: str) -> str | None:
    """
    returns None if not valid
     - we to fix class C : a.b.c -> a.b.c.0/24
    """
    if not cidr:
        return None

    if is_valid_cidr(cidr):
        cidr = fix_cidr_host_bits(cidr)
        return cidr

    if cidr.endswith('.'):
        cidr = cidr[0:-1]

    num_dots = cidr.count('.')
    if num_dots == 2:
        cidr += '.0/24'

    elif num_dots == 1:
        cidr += '.0.0/16'

    elif num_dots == 0:
        cidr += '.0.0.0/8'

    if is_valid_cidr(cidr):
        cidr = fix_cidr_host_bits(cidr)
        return cidr

    return None


def clean_cidrs(cidrs: list[str]) -> list[str]:
    """ clean cidr array """
    if not cidrs:
        return []

    cleans = []
    for cidr in cidrs:
        clean = clean_cidr(cidr)
        if clean:
            cleans.append(clean)
    return cleans


def fix_cidr_host_bits(cidr: str, verb: bool = False) -> str:
    """ zero any host bits """
    net = cidr_to_net(cidr)
    fix = str(net)
    if verb and cidr != fix:
        print(f'\t Fixed: {cidr} -> {fix}')
    return fix


def fix_cidrs_host_bits(cidrs: list[str], verb: bool = False):
    """ zero any host bits """
    if not cidrs:
        return cidrs

    fixed = []
    for cidr in cidrs:
        fix = str(cidr_to_net(cidr))
        if verb and cidr != fix:
            print(f'\t Fixed: {cidr} -> {fix}')
        fixed.append(fix)

    return fixed

# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Class support functions for subnets
"""
from typing import (List)
import ipaddress

from .cidr_types import (IPvxNetwork)
from ._cidr_valid import (cidr_iptype)
from ._cidr_nets import (cidr_to_net, nets_to_cidrs)
from ._cidr_address import (ipaddr_cidr_from_string)
from ._cidr_compact import (compact_nets, compact_cidrs_to_nets)


def cidr_set_prefix(cidr: str, prefix: int) -> str:
    """
    Set Prefix
        Set new prefix for cidr and return new cidr string

    :param cidr:
        Cidr string to use

    :param prefix:
        The new prefix to use

    :returns:
        Cidr string using the specified prefix
    """
    addr = ipaddr_cidr_from_string(cidr)
    if not addr:
        raise ValueError(f'Bad cidr {cidr}')

    addr_new = addr.supernet(new_prefix=prefix)
    return str(addr_new)


def cidr_is_subnet(cidr: str, ipa_nets: List[IPvxNetwork]) -> bool:
    """
    Is Subnet:
        Check if cidr is a subnet of any of the list of IPvxNetworks .

    :param cidr:
        Cidr string to check.

    :param ipa_nets:
        List of IPvxNetworks to check in.

    :returns:
        True if cidr is subnet of any of the ipa_nets, else False.
    """
    if not cidr or not ipa_nets:
        return False

    this_net = cidr_to_net(cidr)
    if not this_net:
        return False

    this_ipt = cidr_iptype(this_net)

    for net in ipa_nets:
        net_ipt = cidr_iptype(net)
        if net_ipt != this_ipt:
            return False
        if this_net.subnet_of(net):         # type: ignore[arg-type]
            return True

    return False


def net_exclude(net1: IPvxNetwork, nets2: List[IPvxNetwork]
                ) -> List[IPvxNetwork]:
    """
    Exclude net1 from any of networks in net2
    return resulting list of nets (without net1)
    """
    if not net1 or not nets2:
        return nets2

    nets: List[IPvxNetwork] = []
    for net in nets2:
        if net1.subnet_of(net):                      # type: ignore[arg-type]
            # remove the net1 subnet from net
            nets += list(net.address_exclude(net1))  # type: ignore[arg-type]
        elif net.subnet_of(net1):                    # type: ignore[arg-type]
            # remove net entirely as part of net1
            continue
        else:
            # keep net
            nets.append(net)
    nets = compact_nets(nets)
    return nets


def nets_exclude(nets1: List[IPvxNetwork], nets2: List[IPvxNetwork]
                 ) -> List[IPvxNetwork]:
    """
    Exclude every nets1 network from from any networks in nets2
    """
    final = []
    nets1 = compact_nets(nets1)
    final = compact_nets(nets2)
    for net1 in nets1:
        final = net_exclude(net1, final)
    return final


def cidrs_exclude(cidrs1: List[str], cidrs2: List[str]) -> List[str]:
    """ old name """
    return cidrs2_minus_cidrs1(cidrs1, cidrs2)


def cidrs2_minus_cidrs1(cidrs1: List[str], cidrs2: List[str]
                        ) -> List[str]:
    """
    Exclude all of cidrs1 from cidrs2
    i.e. return cidrs2 - cidrs1
    """
    nets1 = [ipaddress.ip_network(cidr, strict=False) for cidr in cidrs1]
    nets2 = [ipaddress.ip_network(cidr, strict=False) for cidr in cidrs2]
    nets = nets_exclude(nets1, nets2)
    cidrs = [str(net) for net in nets]
    return cidrs


def cidr_exclude(cidr1: str, cidrs2: List[str]) -> List[str]:
    """
    Exclude cidr1 from any of networks in cidrs2
    return resulting list of cidrs (without cidr1)
    """
    if not cidr1 or not cidrs2:
        if not cidrs2:
            return []
        return cidrs2

    net1 = cidr_to_net(cidr1)
    if net1 is None:
        return cidrs2
    net2 = compact_cidrs_to_nets(cidrs2)
    nets = net_exclude(net1, net2)
    return nets_to_cidrs(nets)


def get_host_bits(ip: str, pfx: int = 24) -> int:
    """
    Gets the host bits from an IP address given the netmask
    """
    ipa = ipaddress.ip_address(ip)
    net = ipaddress.ip_network(ip)
    netpfx = net.supernet(new_prefix=pfx)

    hostmask = netpfx.hostmask
    host_bits = int(ipa) & int(hostmask)

    return host_bits

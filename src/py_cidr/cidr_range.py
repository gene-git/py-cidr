# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Class support functions for range of cidrs
'''
import ipaddress

from .cidr_types import (IPvxNetwork, IPvxAddress, IPAddress)
from .cidr_nets import (cidr_to_net)

def range_to_cidrs(addr_start:IPAddress, addr_end:IPAddress, string=False) -> [IPvxNetwork|str]:
    '''
    Generate a list of cidr/nets from an IP range.

    :param addr_start:
        Start of IP range as IPAddress (IPv4Address,  IPv6Address or string)

    :param addr_end:
        End of IP range as IPAddress (IPv4Address,  IPv6Address or string)
    
    :param string:
        If True then returns list of cidr strings otherwise IPvxNetwork

    :returns:
        List of cidr network blocks representing the IP range. 
        List elements are IPvxAddress or str if parameter string=True
    '''
    ip0 = addr_start
    if not isinstance(addr_start, IPvxAddress) :
        ip0 = ipaddress.ip_address(addr_start)

    ip1 = addr_end
    if not isinstance(addr_end, IPvxAddress):
        ip1 = ipaddress.ip_address(addr_end)

    if string:
        cidrs = [str(cidr) for cidr in ipaddress.summarize_address_range(ip0, ip1)]
    else:
        cidrs = list(ipaddress.summarize_address_range(ip0, ip1))
    return cidrs

def net_to_range(net:IPvxNetwork, string:bool=False) -> (IPAddress, IPAddress):
    '''
    Network to IP Range

    :param net:
        The ipaddress network (IPvxNetwork) to examine

    :param string:
        If True then returns cidr strings instead of IPvxAddress

    :returns:
        Tuple (ip0, ip1) of first and last IP address in net
        (ip0, ip1) are IPvxAddress or str when string is True
    '''
    if not net:
        return (None, None)

    ip0 = net.network_address
    ip1 = net.broadcast_address

    if string:
        ip0 = str(ip0)
        ip1 = str(ip1)
    return (ip0, ip1)

def cidr_to_range(cidr:str, string:bool=False) -> (IPAddress, IPAddress):
    '''
    Cidr string to an IP Range

    :param cidr:
        The cidr string to examine

    :param string:
        If True then returns cidr strings instead of IPvxAddress

    :returns:
        Tuple (ip0, ip1) of first and last IP address in net
        (ip0, ip1) are IPvxAddress or str when string is True
    '''
    net = cidr_to_net(cidr, strict=False)
    return net_to_range(net, string)

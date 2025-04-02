# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Class providing some common CIDR utilities
'''
# pylint: disable=too-many-public-methods
from typing import (List)
from ipaddress import (IPv4Network, IPv6Network)

from .cidr_types import (IPvxNetwork, IPvxAddress, IPAddress)
from .version import version

from .cidr_clean import (clean_cidr, clean_cidrs, fix_cidr_host_bits, fix_cidrs_host_bits)

from .cidr_address import (ip_to_address, ips_to_addresses, addresses_to_ips, ipaddr_cidr_from_string)

from .cidr_subnet import (cidr_set_prefix, get_host_bits)
from .cidr_subnet import (cidr_is_subnet, net_exclude, nets_exclude, cidrs_exclude)
from .cidr_subnet import (cidrs2_minus_cidrs1, cidr_exclude)

from .cidr_sort import (sort_cidrs, sort_ips)
from .cidr_compact import (cidr_list_compact, compact_cidrs, compact_nets)
from .cidr_nets import (cidr_to_net, cidrs_to_nets, nets_to_cidrs)
from .cidr_range import (range_to_cidrs, net_to_range, cidr_to_range)
from .cidr_valid import (is_valid_ip4, is_valid_ip6, is_valid_cidr, cidr_iptype, cidr_type_network)
from .cidr_valid import (address_iptype)

from .rfc_1918 import (is_rfc_1918, rfc_1918_nets, rfc_1918_cidrs, remove_rfc_1918)

class Cidr:
    '''
    Class provides common CIDR tools
    All mathods are (static) and are thus called withoue instantiating
    the class. for example :

        net = Cidr.cidr_to_net(cidr_string)

    Notation:
        * cidr means a string
        * net means ipaddress network (IPv4Network or IPv6Network)
        * ip means an IP address string
        * addr means an ip address (IPv4Address or IPv6Address)
        * address means either a IP address or a cidr network as a string
    '''
    @staticmethod
    def version() -> str:
        '''
        :returns:
            Version of py-cidr
        '''
        return version()

    @staticmethod
    def cidr_to_net(cidr:str, strict:bool=False) -> IPvxNetwork | None:
        '''
        Cidr to Net
            Convert cidr string to ipaddress network.

        :param cidr:
            Input cidr string

        :param strict:
            If true then cidr is considered invalid if host bits are set.
            Defaults to False. (see ipaddress docs).

        :returns:
            The ipaddress network derived from cidr string as either IPvxNetwork = IPv4Network or IPv6Network.
        '''
        return cidr_to_net(cidr, strict)

    @staticmethod
    def cidrs_to_nets(cidrs:[str], strict:bool=False) -> [IPvxNetwork]:
        '''
        Cidrs to Nets
            Convert list of cidr strings to list of IPvxNetwork

        :param cidrs:
            List of cidr strings

        :param strict:
            If true, then any cidr with host bits is invalid. Defaults to false.

        :returns:
            List of IPvxNetworks.
        '''
        return cidrs_to_nets(cidrs, strict)

    @staticmethod
    def nets_to_cidrs(nets:[IPvxNetwork]) -> [str]:
        '''
        Nets to Strings
            Convert list of ipaddress networks to list of cidr strings.

        :param nets:
            List of nets to convert

        :returns:
            List of cidr strings
        '''
        return nets_to_cidrs(nets)

    @staticmethod
    def ip_to_address(ip:str) -> IPvxAddress|None:
        '''
        IP to Address
            Return ipaddress of given ip.
            If IP has prefix or host bits set, we strip the prefix first and keep host bits

        :param ip:
            The IP string to convert

        :returns:
            IPvxAddress derived from IP or None if not an IP address
        '''
        return ip_to_address(ip)

    @staticmethod
    def ips_to_addresses(ips:[str]) -> [IPvxAddress]:
        '''
        IPs to Addresses
            Convert list of IP strings to a list of ip addresses

        :param ips:
            List of IP strings to convert

        :returns:
            List of IPvxAddress derived from input IPs.
        '''
        return ips_to_addresses(ips)

    @staticmethod
    def addresses_to_ips(addresses:[IPvxAddress]) -> [str]:
        '''
        Address to IP strings
            For list of IPs in ipaddress format, return list of ip strings

        :param addresses:
            List of IP addresses in ipaddress format

        :returns:
            List of IP strings
        '''
        return addresses_to_ips(addresses)

    @staticmethod
    def cidr_set_prefix(cidr:str, prefix:int) -> str:
        '''
        Set Prefix
            Set new prefix for cidr and return new cidr string

        :param cidr:
            Cidr string to use

        :param prefix:
            The new prefix to use

        :returns:
            Cidr string using the specified prefix
        '''
        return cidr_set_prefix(cidr, prefix)

    @staticmethod
    def ipaddr_cidr_from_string(addr:str, strict:bool=False) -> IPv4Network | IPv6Network | None:
        '''
        IP/CIDR to IPvxNetwork
            Convert string of IP address or cidr net to IPvxNetwork

        :param address:
            String of IP or CIDR network.

        :param strict:
            If true, host bits disallowed for cidr block.

        :returns:
            An IPvXNetwork or None if not valid.
        '''
        return ipaddr_cidr_from_string(addr, strict)

    @staticmethod
    def cidr_is_subnet(cidr:str, ipa_nets:[IPv4Network | IPv6Network]) -> bool:
        '''
        Is Subnet:
            Check if cidr is a subnet of any of the list of IPvxNetworks .

        :param cidr:
            Cidr string to check.

        :param ipa_nets:
            List of IPvxNetworks to check in.

        :returns:
            True if cidr is subnet of any of the ipa_nets, else False.
        '''
        return cidr_is_subnet(cidr, ipa_nets)

    @staticmethod
    def address_iptype(addr:IPvxAddress|IPvxNetwork) -> str|None:
        '''
        Address Type
            Identify if IP address (IPvxAddres) or net (IPvxNetwork) is ipv4 or ipv6

        :param addr:
            IP address or cidr network .

        :returns:
            'ip4', 'ip6' or None
        '''
        return address_iptype(addr)

    @staticmethod
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
        return cidr_list_compact(cidrs_in, string)

    @staticmethod
    def compact_cidrs(cidrs:[str], nets=False) -> [str|IPvxNetwork]:
        '''
        Compact cidr list

        :param cidrs:
            List of cidrs 

        :param nets:
            If true result type IPvxNetwork else string, 

        :returns:
            If nets is True, result is list of IPvxNetwork otherwise strings
        '''
        return compact_cidrs(cidrs, nets)

    @staticmethod
    def compact_nets(nets:[IPvxNetwork]) -> [IPvxNetwork]:
        '''
        Compact list of IPvxNetwork

        :param nets:
            Input list 

        :returns:
            Compacted list of IPvxNetwork
        '''
        return compact_nets(nets)

    @staticmethod
    def net_exclude(net1:IPvxNetwork, nets2:[IPvxNetwork]) -> [IPvxNetwork]:
        '''
        Exclude net1 from any of networks in net2
        return resulting list of nets (without net1)
        '''
        return net_exclude(net1, nets2)

    @staticmethod
    def nets_exclude(nets1:[IPvxNetwork], nets2:[IPvxNetwork]) -> [IPvxNetwork]:
        '''
        Exclude every nets1 network from from any networks in nets2
        '''
        return nets_exclude(nets1, nets2)

    @staticmethod
    def cidrs_exclude(cidrs1:[str], cidrs2:[str]) -> [str]:
        ''' old name '''
        return cidrs_exclude(cidrs1, cidrs2)

    @staticmethod
    def cidrs2_minus_cidrs1(cidrs1:[str], cidrs2:[str]) -> [str]:
        '''
        Exclude all of cidrs1 from cidrs2
        i.e. return cidrs2 - cidrs1
        '''
        return cidrs2_minus_cidrs1(cidrs1, cidrs2)

    @staticmethod
    def cidr_exclude(cidr1:str, cidrs2:[str]) -> [str]:
        '''
        Exclude cidr1 from any of networks in cidrs2
        return resulting list of cidrs (without cidr1)
        '''
        return cidr_exclude(cidr1, cidrs2)

    @staticmethod
    def sort_cidrs(cidrs:[str]) -> [str]:
        '''
        Sort the list of cidr strings
        '''
        return sort_cidrs(cidrs)

    @staticmethod
    def sort_ips(ips:[str]) -> [str]:
        '''
        Sort the list of cidr strings
        '''
        return sort_ips(ips)

    @staticmethod
    def get_host_bits(ip:str, pfx:int=24):
        '''
        Gets the host bits from an IP address given the netmask
        '''
        return get_host_bits(ip, pfx)

    @staticmethod
    def clean_cidr(cidr:str) -> str:
        '''
        returns None if not valid
         - we to fix class C : a.b.c -> a.b.c.0/24
        '''
        return clean_cidr(cidr)

    @staticmethod
    def clean_cidrs(cidrs:[str]) -> [str]:
        ''' clean cidr array '''
        return clean_cidrs(cidrs)

    @staticmethod
    def fix_cidr_host_bits(cidr:str, verb:bool=False):
        ''' zero any host bits '''
        return fix_cidr_host_bits(cidr, verb)

    @staticmethod
    def fix_cidrs_host_bits(cidrs:[str], verb:bool=False):
        ''' zero any host bits '''
        return fix_cidrs_host_bits(cidrs, verb)

    @staticmethod
    def is_valid_ip4(address) -> bool:
        ''' check if valid address or cidr '''
        return is_valid_ip4(address)

    @staticmethod
    def is_valid_ip6(address) -> bool:
        ''' check if valid address or cidr '''
        return is_valid_ip6(address)

    @staticmethod
    def is_valid_cidr(address) -> bool:
        '''
        Valid Address or Network
            check if valid ip address or cidr network

        :param address:
            IP or Cidr string to check. Host bits being set is permitted for a cidr network.

        :returns:
            True/False if address is valid
        '''
        return is_valid_cidr(address)

    @staticmethod
    def cidr_iptype(address:str) -> str|None :
        '''
        Determines if an IP address or CIDR string is ipv4 or ipv6

        :param address:
            ip address or cidr string

         :returns:
            'ip4' or 'ip6' or None
        '''
        return cidr_iptype(address)

    @staticmethod
    def cidr_type_network(cidr:str) -> (str, IPvxNetwork):
        '''
        Cidr Network Type:

        :param cidr:
            Cidr string to examine

        :returns:
            Tuple(ip-type, net-type). ip-type is a string  ('ip4', 'ip6') while
            network type is IPv4Network or IPv6Network
        '''
        return cidr_type_network(cidr)

    @staticmethod
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
        return range_to_cidrs(addr_start, addr_end, string)

    @staticmethod
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
        net_to_range(net, string)

    @staticmethod
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
        return cidr_to_range(cidr, string)

    @staticmethod
    def is_rfc_1918(cidr: str) -> bool:
        '''
        Check if cidr is any RFC 1918

        :param cidr:
            IP or Cidr to check if RFC 1918
        
        :returns:
            True if cidr is an RGC 1918 address
            False if not.
        '''
        return is_rfc_1918(cidr)

    @staticmethod
    def rfc_1918_nets() -> [IPv4Network]:
        '''
        Return list of rfc 1918 networks

        :returns:
            List of all RFC 1918 networks. Each element is ipaddress.IPv4Network
        '''
        return rfc_1918_nets()

    @staticmethod
    def rfc_1918_cidrs() -> [str]:
        '''
        Return list of rfc 1918 networks cidr strings

        :returns:
            List of RFC 1918 networks as cidr strings
        '''
        return rfc_1918_cidrs()

    @staticmethod
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
        return remove_rfc_1918(cidrs_in)

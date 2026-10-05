# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Class providing some common CIDR utilities
"""
# pylint: disable=too-many-public-methods
from typing import Any

from py_cidr._network.cidr_types import (IPvxNetwork, IPvxAddress, IPAddress)

from py_cidr._network._cidr_clean import (clean_cidr, clean_cidrs)
from py_cidr._network._cidr_clean import (fix_cidr_host_bits, fix_cidrs_host_bits)

from py_cidr._network._cidr_address import (ip_to_address, ips_to_addresses)
from py_cidr._network._cidr_address import (addresses_to_ips, ipaddr_cidr_from_string)

from py_cidr._network._cidr_subnet import (cidr_set_prefix, get_host_bits)
from py_cidr._network._cidr_subnet import (net_is_subnet, cidr_is_subnet)
from py_cidr._network._cidr_subnet import (net_exclude, nets_exclude, cidrs_exclude)
from py_cidr._network._cidr_subnet import (cidrs2_minus_cidrs1, cidr_exclude)

from py_cidr._network._cidr_sort import (sort_cidrs, sort_ips, sort_nets)
from py_cidr._network._cidr_compact import (compact_cidrs_to_nets, compact_cidrs)
from py_cidr._network._cidr_compact import (compact_nets)

from py_cidr._network._cidr_nets import (cidr_to_net, cidrs_to_nets, nets_to_cidrs)
from py_cidr._network._cidr_nets import (address_to_net, net_to_cidr)

from py_cidr._network._cidr_range import (range_to_cidrs, range_to_nets)
from py_cidr._network._cidr_range import (net_to_range_cidrs, net_to_range_nets)
from py_cidr._network._cidr_range import (cidr_to_range_cidrs, cidr_to_range_nets)

from py_cidr._network._cidr_range_split import (cidr_range_split, net_range_split)

from py_cidr._network._cidr_valid import (is_valid_ip4, is_valid_ip6, is_valid_cidr)
from py_cidr._network._cidr_valid import (cidr_iptype, cidr_type_network)
from py_cidr._network._cidr_valid import (address_iptype)

from py_cidr._network._rfc_1918 import (is_rfc_1918, rfc_1918_nets, rfc_1918_cidrs)
from py_cidr._network._rfc_1918 import (remove_rfc_1918)

from py_cidr._network._cidr_split_type import cidrs_split_type

from py_cidr._network.ip_version import ip_version

from py_cidr._version import version


class Cidr:
    """
    Provides suite of CIDR tools.

    All mathods are (static) and are thus called without need
    to instantiate the class. For example:

        net = Cidr.cidr_to_net(cidr_string)

    Notation:
        * cidr means a string
        * net means ipaddress network (IPv4Network or IPv6Network)
        * ip means an IP address string
        * addr means an ip address (IPv4Address or IPv6Address)
        * address means either a IP address or a cidr network as a string
    """
    @staticmethod
    def version() -> str:
        """
        :returns:
            Version of py-cidr
        """
        return version()

    @staticmethod
    def address_to_net(addr: IPAddress | IPvxNetwork, strict: bool = False
                       ) -> IPvxNetwork | None:
        """
        Convert an address to IPvxNetwork.

        Be flexible with input address. Can be
        IPAddress (includes string) or even IPvxNetwork.

        :param addr: Input address.
        :param strict: If true then cidr is considered invalid if host bits are set.
                       Defaults to False. (see ipaddress docs).
        :returns: The IPvxNetwork derived from input "addr" or None if not an address/network.
        """
        return address_to_net(addr, strict)

    @staticmethod
    def cidr_to_net(cidr: str, strict: bool = False) -> IPvxNetwork | None:
        """
        Convert cidr string to ipaddress network.

        :param cidr: Input cidr string
        :param strict: If true then cidr is considered invalid if host bits are set.
                       Defaults to False. (see ipaddress docs).
        :returns: The ipaddress network derived from cidr string as
                  IPvxNetwork = IPv4Network or IPv6Network or None if invalid.
        """
        return cidr_to_net(cidr, strict)

    @staticmethod
    def cidrs_to_nets(cidrs: list[str], strict: bool = False
                      ) -> list[IPvxNetwork]:
        """
        Convert list of cidr strings to list of IPvxNetwork.

        :param cidrs: list of cidr strings
        :param strict: If true, cidr with host bits set is invalid. Defaults to false.
        :returns: list of IPvxNetworks generated from cidrs.
        """
        return cidrs_to_nets(cidrs, strict)

    @staticmethod
    def nets_to_cidrs(nets: list[IPvxNetwork]) -> list[str]:
        """
        Convert list of ipaddress networks to list of cidr strings.

        :param nets: list of nets to convert.
        :returns: list of cidr strings.
        """
        return nets_to_cidrs(nets)

    @staticmethod
    def net_to_cidr(net: IPvxNetwork) -> str:
        """
        Net to Cidr String
            Convert an ipaddress network to a cidr string.

        :param net: Ipaddress Network to convert.
        :returns: Cidr string from net. If unable to conver, then empty string is returned.
        """
        return net_to_cidr(net)

    @staticmethod
    def ip_to_address(ip: str) -> IPvxAddress | None:
        """
        Return ipaddress of given ip.

        If IP has prefix or host bits set, strip the prefix and keep host bits.

        :param ip: The IP string to convert
        :rreturns: IPvxAddress derived from IP or None if not an IP address.
        """
        return ip_to_address(ip)

    @staticmethod
    def ips_to_addresses(ips: list[str]) -> list[IPvxAddress]:
        """
        Convert list of IP strings to a list of ip addresses

        :param ips: list of IP strings to convert
        :returns: list of IPvxAddress derived from input IPs.
        """
        return ips_to_addresses(ips)

    @staticmethod
    def addresses_to_ips(addresses: list[IPvxAddress]) -> list[str]:
        """
        From list of IPs in ipaddress format, get list of ip strings.

        :param addresses: list of IP addresses in ipaddress format
        :returns: list of IP strings
        """
        return addresses_to_ips(addresses)

    @staticmethod
    def cidr_set_prefix(cidr: str, prefix: int) -> str:
        """
        Set new prefix for cidr and return new cidr string.

        :param cidr: Cidr string to use
        :param prefix: The new prefix to use
        :returns: Cidr string using the specified prefix
        """
        return cidr_set_prefix(cidr, prefix)

    @staticmethod
    def ipaddr_cidr_from_string(address: str, strict: bool = False
                                ) -> IPvxNetwork | None:
        """
        Convert string of IP address or cidr net to IPvxNetwork

        :param address: IP or CIDR network as a string.
        :param strict: If true, host bits are disallowed for cidr block.
        :returns: An IPvxNetwork or None if invalid.
        """
        return ipaddr_cidr_from_string(address, strict)

    @staticmethod
    def cidr_is_subnet(cidr: str, ipa_nets: list[IPvxNetwork]) -> bool:
        """
        Check if cidr is a subnet of any of the list of IPvxNetworks .

        :param cidr: Cidr string to check.
        :param ipa_nets: list of IPvxNetworks to check.
        :returns: True if cidr is subnet of any of the ipa_nets, else False.
        """
        return cidr_is_subnet(cidr, ipa_nets)

    @staticmethod
    def net_is_subnet(net1: IPvxNetwork, net2: IPvxNetwork | list[IPvxNetwork]) -> bool:
        """
        Determines if net1 is a subnet of any of net2.

        :param net1: Network to check if is a subnet.
        :param net2: Network or list of networks to be checked.
        :returns: True if net1 is a subnet of any of net2.
        """
        return net_is_subnet(net1, net2)

    @staticmethod
    def address_iptype(addr: IPvxAddress | IPvxNetwork) -> str:
        """
        Identify address or net (IPvxNetwork) as ipv4, ipv6 or neither.

        :param addr: ipaddress IP or network .
        :returns: 'ip4', 'ip6' or ''
        """
        return address_iptype(addr)

    @staticmethod
    def cidr_list_compact(cidrs: list[str], string: bool = True
                          ) -> list[str] | list[IPvxNetwork]:
        """
        Compact list of cidr networks to smallest list possible.
        Deprecated - use compact_cidrs(cidrs, return_nets)) instead,
        it is the same with the boolean flag reversed.

        :param cidrs: list of cidr strings to compact.
        :string: If True (default), then return is a list of strings.
                 If False, a list of IPvxNetworks.
        :returns: Compressed list of cidrs as ipaddress networks (string=False)
                  or list of strings when string=True
        """
        if string:
            return compact_cidrs(cidrs)
        return compact_cidrs_to_nets(cidrs)

    @staticmethod
    def compact_cidrs_to_cidrs(cidrs: list[str]) -> list[str]:
        """
        Compact list of cidr networks and return list of cidr strings

        Same as compact_cidrs(cidrs, nets=False).
        With single return type this is helpful when using
        type annotation checkers.
        """
        return compact_cidrs(cidrs)

    @staticmethod
    def compact_cidrs(cidrs: list[str], nets: bool = False) -> list[str] | list[IPvxNetwork]:
        """
        Compact a list of cidr networks as strings.

        :param cidrs: list of cidrs to compact.
        :param nets: If False, the default, the result will be list of strings
                     else a list of IPvxNetwork's.
        :returns: A list of compacted networks whose elements are strings
                  if return_nets is False or IPvxNetworks if True.
        """
        if nets:
            return compact_cidrs_to_nets(cidrs)
        return compact_cidrs(cidrs)

    @staticmethod
    def compact_nets(nets: list[IPvxNetwork]) -> list[IPvxNetwork]:
        """
        Compact list of IPvxNetwork.

        :param nets: Input list if networks to compact.
        :returns: Compacted list of IPvxNetworks.
        """
        return compact_nets(nets)

    @staticmethod
    def net_exclude(net1: IPvxNetwork, nets2: list[IPvxNetwork]) -> list[IPvxNetwork]:
        """
        Exclude net1 from any of networks in net2 and
        return resulting list of nets (without net1).

        :param net1: Network to be ecluded.
        :param nets2: list of networks from which net1 will be excluded from.
        :returns: Resultant list of networks "nets2 - net1".
        """
        return net_exclude(net1, nets2)

    @staticmethod
    def nets_exclude(nets1: list[IPvxNetwork], nets2: list[IPvxNetwork]) -> list[IPvxNetwork]:
        """
        Exclude every nets1 network from from any networks in nets2.

        Similar to net_exclude() except this version has a list
        to be excluded instead of a single network.

        :param nets1: list of nets to be excluded.
        :param nets2: list of nets from which will exclude any of nets1.
        :returns: list of resultant networks ("nets2" - "nets1")
        """
        return nets_exclude(nets1, nets2)

    @staticmethod
    def cidrs_exclude(cidrs1: list[str], cidrs2: list[str]) -> list[str]:
        """ Deprecated: replaced by cidrs2_minus_cidrs1()"""
        return cidrs_exclude(cidrs1, cidrs2)

    @staticmethod
    def cidrs2_minus_cidrs1(cidrs1: list[str], cidrs2: list[str]) -> list[str]:
        """
        Exclude all of cidrs1 from cidrs2.

        i.e. return "cidrs2" - "cidrs1".

        :param cidrs1: list of cidr strings to be excluded.
        :param cidrs2: list of cidr strings from which cidrs1 are excluded.
        :returns: Resulting list of cidr strings = "cidrs2" - "cidrs1".
        """
        return cidrs2_minus_cidrs1(cidrs1, cidrs2)

    @staticmethod
    def cidr_exclude(cidr1: str, cidrs2: list[str]) -> list[str]:
        """
        Exclude cidr1 from any of networks in cidrs2.

        :param cidr1: cidr to be excluded.
        :param cidrs2: list fo cidrs from which cidr1 will be excluded.
        :returns: Resulting list of cidrs ("cidrs2" - "cidr1")
        """
        return cidr_exclude(cidr1, cidrs2)

    @staticmethod
    def sort_cidrs(cidrs: list[str]) -> list[str]:
        """
        Sort the list of cidr strings.

        :param cidrs: list of cidrs.
        :returns: Sorted copy of cidr list
        """
        return sort_cidrs(cidrs)

    @staticmethod
    def sort_ips(ips: list[str]) -> list[str]:
        """
        Sort a list of IP addresses.

        :param ips: list of ips to be sorted.
        :returns: Sorted copy of ips.
        """
        return sort_ips(ips)

    @staticmethod
    def sort_nets(nets: list[IPvxNetwork]) -> list[IPvxNetwork]:
        """
        Sort a list of networks.

        :param nets: list of networks to be sorted.
        :returns: Sorted copy of networks.
        """
        return sort_nets(nets)

    @staticmethod
    def get_host_bits(ip: str, pfx: int = 24) -> int:
        """
        Gets the host bits from an IP address given the netmask.

        :param ip: The IP to examine.
        :param pfx: The cidr prefix.
        :returns: The host bits from the IP.
        """
        return get_host_bits(ip, pfx)

    @staticmethod
    def clean_cidr(cidr: str) -> str | None:
        """
        Clean up a cidr address.

        Does:
         - fix up host bits to match the prefix
         - convert old class A,B,C style IPv4 addresses to cidr.

        e.g.
            a.b.c -> a.b.c.0/24
            a.b.c.23/24 -> a.b.c.0/24

        :param cidr: Cidr string to clean up.
        :returns: - cidr string if valid
                  - None if cidr is invalid.

        """
        return clean_cidr(cidr)

    @staticmethod
    def clean_cidrs(cidrs: list[str]) -> list[str]:
        """
        Clean list of cidrs.

        Similar to clean_cidr() but for a list.

        :param cidrs: list of cidr strings to clean up.
        :returns: list of cleaned cidrs.
                  If input cidr is invalid then its returnded as None
        """
        return clean_cidrs(cidrs)

    @staticmethod
    def fix_cidr_host_bits(cidr: str, verb: bool = False) -> str:
        """
        zero out any host bits.

        A strictly valid cidr address must have host bits set to zero.

        :param cidr: The cidr to "fix" if needed.
        :parm verb: Some info on stdout when set True. Defaults to False.
        :returns: The cidr with any non-zero host bits now zeroed out.
        """
        return fix_cidr_host_bits(cidr, verb)

    @staticmethod
    def fix_cidrs_host_bits(cidrs: list[str], verb: bool = False) -> list[str]:
        """
        zero any host bits for a list of cidrs.

        Similar to fix_cidr_host_bits() but for a list of cidrs.

        :param cidrs: list of cidrs to fix up.
        :param verb: Some info on stdout when set True. Defaults to False.
        :returns: The list of cidrs each with any non-zero host bits now zeroed out.
        """
        return fix_cidrs_host_bits(cidrs, verb)

    @staticmethod
    def is_valid_ip4(address: Any) -> bool:
        """
        check if valid IPv4 address or cidr.

        :param address: Check if this is a valid IPv4 address or cidr.
        :returns: True if valid IPv4 else False
        """
        return is_valid_ip4(address)

    @staticmethod
    def is_valid_ip6(address: Any) -> bool:
        """
        check if valid IPv6 address or cidr.

        :param address: Check if this is a valid IPv6 address or cidr.
        :returns: True if valid IPv6 else False
        """
        return is_valid_ip6(address)

    @staticmethod
    def is_valid_cidr(address: Any) -> bool:
        """
        Check if address is a valid ip or cidr network.

        :parram address: Address to check. Host bits set is permitted for a cidr network.
        :returns: True/False if address is valid IPv4 or IPv6 address or network.
        """
        return is_valid_cidr(address)

    @staticmethod
    def cidr_iptype(address: Any) -> str:
        """
        Determines if address string is valid ipv4 or ipv6 or not.

        :param address: address or cidr string
        :returns: 'ip4' or 'ip6' or empty string, '', if address invalid.
                   Note. Earlier versions returned None instead of
                   empty string if unable to be converted.
        """
        return cidr_iptype(address)

    @staticmethod
    def ip_version(addr_or_net: str | IPvxNetwork | IPvxAddress) -> int:
        """
        Determines the IP version of an address or network:

        :param addr_or_net: Can be IP addess or network either a string or ip_address format.
        :returns: 4 if addr_or_net is IPv4Network or IPv4Address
                  6 if addr_or_net is IPv6Network or IPv5Address
                  0 otherwise
        """
        return ip_version(addr_or_net)

    @staticmethod
    def cidr_type_network(cidr: str) -> tuple[str, type[IPvxNetwork]]:
        """
        Cidr Network Type.

        :param cidr: Cidr string to examine
        :returns: tuple('ip4' or 'ip6', IPv4Network or IPv6Network).
        """
        return cidr_type_network(cidr)

    @staticmethod
    def range_to_cidrs(addr_start: IPAddress, addr_end: IPAddress,
                       string: bool = False) -> list[IPvxNetwork] | list[str]:
        """
        Generate a list of cidr/nets from an IP range.

        :param addr_start: Start of IP range
        :param addr_end: End of IP range
        :string: If True then returns list of cidr strings otherwise IPvxNetwork
        :returns: list of cidr network blocks representing the IP range.
                  list elements are IPvxAddress or str if parameter string=True
        """
        if string:
            return range_to_cidrs(addr_start, addr_end)
        return range_to_nets(addr_start, addr_end)

    @staticmethod
    def net_to_range(net: IPvxNetwork, string: bool = False
                     ) -> tuple[IPvxAddress | str | None,
                                IPvxAddress | str | None]:
        """
        Convert network to IP Range.

        :param net: The network (IPvxNetwork) to examine.
        :param string: If True then returns cidr strings instead of IPvxAddress
        :returns: tuple (ip0, ip1) of first and last IP address in net
                  Each (ip0, ip1) is IPvxAddress or a string if "string" == True
        """
        if string:
            return net_to_range_cidrs(net)
        return net_to_range_nets(net)

    @staticmethod
    def cidr_to_range(cidr: str, string: bool = False
                      ) -> tuple[IPvxAddress | str | None,
                                 IPvxAddress | str | None]:
        """
        Cidr string to an IP Range.

        :param cidr: The cidr string to examine.
        :param string: If True then returns cidr strings instead of IPvxAddress
        :returns: tuple (ip0, ip1) of first and last IP address in net
                  (ip0, ip1) are IPvxAddress or str when string is True
        """
        if string:
            return cidr_to_range_cidrs(cidr)
        return cidr_to_range_nets(cidr)

    @staticmethod
    def net_range_split(net: IPvxNetwork) -> tuple[IPvxAddress, IPvxAddress, IPvxAddress]:
        """
        Convert network to IP Range.

        :param net: The network (IPvxNetwork) to examine.
        :param string: If True then returns cidr strings instead of IPvxAddress
        :returns: tuple of 3 IPvxAddress: (first IP, middle IP, last IP) in the cidr block
        """
        return net_range_split(net)

    @staticmethod
    def cidr_range_split(cidr: str) -> tuple[str, str, str]:
        """
        Convert network to IP Range.

        :param net: The network (IPvxNetwork) to examine.
        :param string: If True then returns cidr strings instead of IPvxAddress
        :returns: strings of the first IP, middle IP and last IP in the cidr block
        """
        return cidr_range_split(cidr)

    @staticmethod
    def is_rfc_1918(cidr: str) -> bool:
        """
        Check if cidr is any RFC 1918.

        :param cidr: IP or Cidr to check if RFC 1918.
        :returns: True if cidr is an RFC 1918 address.  False if not.
        """
        return is_rfc_1918(cidr)

    @staticmethod
    def rfc_1918_nets() -> list[IPvxNetwork]:
        """
        Return list of rfc 1918 networks

        :returns: list of RFC 1918 networks.
        """
        return rfc_1918_nets()

    @staticmethod
    def rfc_1918_cidrs() -> list[str]:
        """
        Return list of rfc 1918 networks cidr strings

        :returns: list of RFC 1918 networks as cidr strings
        """
        return rfc_1918_cidrs()

    @staticmethod
    def remove_rfc_1918(cidrs_in: str | list[str]
                        ) -> tuple[str | list[str], str | list[str]]:
        """
        Given list of cidrs, return list without any rfc 1918

        :param cidrs_in: Cidr string or list of cidr strings.
        :returns: Returns (tuple[cidrs_cleaned, rfc_1918_cidrs_found]):
                  - cidrs_cleaned:
                  list of cidrs with all rfc_1918 removed.
                  - rfc_1918_cidrs_found:
                  list of any rfc 1918 found in the input.

                  If input cidr(s) is a list, then items in output
                  are a (possibly empty) list
                  If not a list then returned items will be string or None.
        """
        return remove_rfc_1918(cidrs_in)

    @staticmethod
    def cidrs_split_type(cidrs: list[str]
                         ) -> tuple[list[str], list[str], list[str]]:
        """
        Split a list of cidrs into ipv4, ipv6 and other.

        :param cidrs: list of cidr strings
        :returns: Tuple of lists of ipv4, ipv6 and unknown.
        """
        return cidrs_split_type(cidrs)

    @staticmethod
    def compact(cidrs: list[str]) -> list[str]:
        """
        Compact list of cidrs - can be mixed ipv4/ipv6.
        Returns 1 type, making type annotation simpler for caller.

        :param cidrs: Input list of cidr strings.
        :returns: Compacted list of cidrs. If mixed ipv4 is before ipv6

        Recommended methods are compact() or compact_nets().
        Others are kept for backward compatibility.
        """
        return compact_cidrs(cidrs)

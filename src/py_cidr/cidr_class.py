# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Class providing some common CIDR utilities
"""
# pylint: disable=too-many-public-methods
from typing import (Any)

from .cidr_types import (IPvxNetwork, IPvxAddress, IPAddress)
from ._version import version

from ._cidr_clean import (clean_cidr, clean_cidrs)
from ._cidr_clean import (fix_cidr_host_bits, fix_cidrs_host_bits)

from ._cidr_address import (ip_to_address, ips_to_addresses)
from ._cidr_address import (addresses_to_ips, ipaddr_cidr_from_string)

from ._cidr_subnet import (cidr_set_prefix, get_host_bits)
from ._cidr_subnet import (net_is_subnet, cidr_is_subnet)
from ._cidr_subnet import (net_exclude, nets_exclude, cidrs_exclude)
from ._cidr_subnet import (cidrs2_minus_cidrs1, cidr_exclude)

from ._cidr_sort import (sort_cidrs, sort_ips, sort_nets)
from ._cidr_compact import (compact_cidrs_to_nets, compact_cidrs)
from ._cidr_compact import (compact_nets)

from ._cidr_nets import (cidr_to_net, cidrs_to_nets, nets_to_cidrs)
from ._cidr_nets import (address_to_net, net_to_cidr)

from ._cidr_range import (range_to_cidrs, range_to_nets)
from ._cidr_range import (net_to_range_cidrs, net_to_range_nets)
from ._cidr_range import (cidr_to_range_cidrs, cidr_to_range_nets)

from ._cidr_range_split import (cidr_range_split, net_range_split)

from ._cidr_valid import (is_valid_ip4, is_valid_ip6, is_valid_cidr)
from ._cidr_valid import (cidr_iptype, cidr_type_network)
from ._cidr_valid import (address_iptype)

from ._rfc_1918 import (is_rfc_1918, rfc_1918_nets, rfc_1918_cidrs)
from ._rfc_1918 import (remove_rfc_1918)

from ._cidr_split_type import cidrs_split_type


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

        Args:
            addr (IPAddress | IPvxNetwork):
                Input address.

            strict (bool):
                If true then cidr is considered invalid if host bits are set.
                Defaults to False. (see ipaddress docs).

        Returns:
            IPvxNetwork | None:
                The IPvxNetwork derived from input "addr" or None if
                not an address/network.
        """
        return address_to_net(addr, strict)

    @staticmethod
    def cidr_to_net(cidr: str, strict: bool = False) -> IPvxNetwork | None:
        """
        Convert cidr string to ipaddress network.

        Args:
            cidr (str):
            Input cidr string

            strict (bool):
            If true then cidr is considered invalid if host bits are set.
            Defaults to False. (see ipaddress docs).

        Returns:
            IPvxNetwork | None:
            The ipaddress network derived from cidr string as
            IPvxNetwork = IPv4Network or IPv6Network or None if invalid.
        """
        return cidr_to_net(cidr, strict)

    @staticmethod
    def cidrs_to_nets(cidrs: list[str], strict: bool = False
                      ) -> list[IPvxNetwork]:
        """
        Convert list of cidr strings to list of IPvxNetwork.

        Args:
            cidrs (list[str]):
            list of cidr strings

            strict (bool):
            If true, cidr with host bits set is invalid. Defaults to false.

        Returns:
            list[IPvxNetwork]:
            list of IPvxNetworks generated from cidrs.
        """
        return cidrs_to_nets(cidrs, strict)

    @staticmethod
    def nets_to_cidrs(nets: list[IPvxNetwork]) -> list[str]:
        """
        Convert list of ipaddress networks to list of cidr strings.

        Args:
            nets (list[IPvxNetwork]):
            list of nets to convert.

        Returns:
            list[str]:
            list of cidr strings.
        """
        return nets_to_cidrs(nets)

    @staticmethod
    def net_to_cidr(net: IPvxNetwork) -> str:
        """
        Net to Cidr String
            Convert an ipaddress network to a cidr string.

        Args:
            net (IPvxNetwork):
                Ipaddress Network to convert.

        Returns:
            str:
            Cidr string from net. If unable to conver,
            then empty string is returned.
        """
        return net_to_cidr(net)

    @staticmethod
    def ip_to_address(ip: str) -> IPvxAddress | None:
        """
        Return ipaddress of given ip.

        If IP has prefix or host bits set, strip the prefix and keep host bits.

        Args:
            ip (str):
            The IP string to convert

            Rreturns (IPvxAddress | None):
            IPvxAddress derived from IP or None if not an IP address.
        """
        return ip_to_address(ip)

    @staticmethod
    def ips_to_addresses(ips: list[str]) -> list[IPvxAddress]:
        """
        Convert list of IP strings to a list of ip addresses

        Args:
            ips (list[str]):
            list of IP strings to convert

        Returns:
            list[IPvxAddress]:
            list of IPvxAddress derived from input IPs.
        """
        return ips_to_addresses(ips)

    @staticmethod
    def addresses_to_ips(addresses: list[IPvxAddress]) -> list[str]:
        """
        From list of IPs in ipaddress format, get list of ip strings.

        Args:
            addresses (list[IPvxAddress]):
            list of IP addresses in ipaddress format

        Returns:
            list[str]:
            list of IP strings
        """
        return addresses_to_ips(addresses)

    @staticmethod
    def cidr_set_prefix(cidr: str, prefix: int) -> str:
        """
        Set new prefix for cidr and return new cidr string.

        Args:
            cidr (str):
            Cidr string to use

            prefix (int):
            The new prefix to use

        Returns:
            str:
            Cidr string using the specified prefix
        """
        return cidr_set_prefix(cidr, prefix)

    @staticmethod
    def ipaddr_cidr_from_string(address: str, strict: bool = False
                                ) -> IPvxNetwork | None:
        """
        Convert string of IP address or cidr net to IPvxNetwork

        Args:
            address:
            IP or CIDR network as a string.

            strict (bool):
            If true, host bits are disallowed for cidr block.

        Returns:
            IPvxNetwork | None:
            An IPvxNetwork or None if invalid.
        """
        return ipaddr_cidr_from_string(address, strict)

    @staticmethod
    def cidr_is_subnet(cidr: str, ipa_nets: list[IPvxNetwork]) -> bool:
        """
        Check if cidr is a subnet of any of the list of IPvxNetworks .

        Args:
            cidr (str):
            Cidr string to check.

            ipa_nets (list[IPvxNetwork]):
            list of IPvxNetworks to check.

        Returns:
            bool:
            True if cidr is subnet of any of the ipa_nets, else False.
        """
        return cidr_is_subnet(cidr, ipa_nets)

    @staticmethod
    def net_is_subnet(net1: IPvxNetwork, net2: IPvxNetwork | list[IPvxNetwork]
                      ) -> bool:
        """
        Determines if net1 is a subnet of any of net2.

        Args:
            net1 (IPvxNetwork):
                Network to check if is a subnet.

            net2 (IPvxNetwork | list[IPvxNetwork]):
                Network or list of networks to be checked.

        Returns:
            bool:
                True if net1 is a subnet of any of net2.
        """
        return net_is_subnet(net1, net2)

    @staticmethod
    def address_iptype(addr: IPvxAddress | IPvxNetwork) -> str:
        """
        Identify address or net (IPvxNetwork) as ipv4, ipv6 or neither.

        Args:
            addr (str):
            ipaddress IP or network .

        Returns:
            str | None:
            'ip4', 'ip6' or ''
        """
        return address_iptype(addr)

    @staticmethod
    def cidr_list_compact(cidrs: list[str], string: bool = True
                          ) -> list[str] | list[IPvxNetwork]:
        """
        Compact list of cidr networks to smallest list possible.
        Deprecated - use compact_cidrs(cidrs, return_nets)) instead,
        it is the same with the boolean flag reversed.

        Args:
            cidrs (list[str]):
            list of cidr strings to compact.

            string (bool):
             - If True (default), then return is a list of strings.
             - If False, a list of IPvxNetworks.

        Returns:
            list[str] | list[IPvxNetwork]:
            Compressed list of cidrs as ipaddress networks (string=False)
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
    def compact_cidrs(cidrs: list[str], nets: bool = False
                      ) -> list[str] | list[IPvxNetwork]:
        """
        Compact a list of cidr networks as strings.

        Args:
            cidrs (list[str]):
            list of cidrs to compact.

            nets (bool):
            If False, the default, the result will be list of strings
            else a list of IPvxNetwork's.

        Returns:
            list[str | IPvxNetwork]:
            A list of compacted networks whose elements are strings
            if return_nets is False or IPvxNetworks if True.
        """
        if nets:
            return compact_cidrs_to_nets(cidrs)
        return compact_cidrs(cidrs)

    @staticmethod
    def compact_nets(nets: list[IPvxNetwork]) -> list[IPvxNetwork]:
        """
        Compact list of IPvxNetwork.

        Args:
            nets (list[IPvxNetwork]):
            Input list if networks to compact.

        Returns:
            list[IPvxNetwork]:
            Compacted list of IPvxNetworks.
        """
        return compact_nets(nets)

    @staticmethod
    def net_exclude(net1: IPvxNetwork, nets2: list[IPvxNetwork]
                    ) -> list[IPvxNetwork]:
        """
        Exclude net1 from any of networks in net2 and
        return resulting list of nets (without net1).

        Args:
            net1 (IPvxNetwork):
            Network to be ecluded.

            nets2 (list[IPvxNetwork]):
            list of networks from which net1 will be excluded
            from.

        Returns:
            list[IPvxNetwork]:
            Resultant list of networks "nets2 - net1".
        """
        return net_exclude(net1, nets2)

    @staticmethod
    def nets_exclude(nets1: list[IPvxNetwork], nets2: list[IPvxNetwork]
                     ) -> list[IPvxNetwork]:
        """
        Exclude every nets1 network from from any networks in nets2.

        Similar to net_exclude() except this version has a list
        to be excluded instead of a single network.

        Args:
            nets1 (list[IPvxNetwork]):
            list of nets to be excluded.

            nets2: (list[IPvxNetwork]):
            list of nets from which will exclude any of nets1.

        Returns:
            list[IPvxNetwork]:
            list of resultant networks ("nets2" - "nets1")

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

        Args:
            cidrs1 (list[str]):
            list of cidr strings to be excluded.

            cidrs2 (list[str]):
            list of cidr strings from which cidrs1 are excluded.

        Returns:
            list[str]:
            Resulting list of cidr strings = "cidrs2" - "cidrs1".

        """
        return cidrs2_minus_cidrs1(cidrs1, cidrs2)

    @staticmethod
    def cidr_exclude(cidr1: str, cidrs2: list[str]) -> list[str]:
        """
        Exclude cidr1 from any of networks in cidrs2.

        Args:
            cidr1 (str):
            cidr to be excluded.

            cidrs2 (list[str]):
            list fo cidrs from which cidr1 will be excluded.

        Returns:
            list[str]:
            Resulting list of cidrs ("cidrs2" - "cidr1")
        """
        return cidr_exclude(cidr1, cidrs2)

    @staticmethod
    def sort_cidrs(cidrs: list[str]) -> list[str]:
        """
        Sort the list of cidr strings.

        Args:
            cidrs (list[str]):
            list of cidrs.

        Returns:
            list[str]:
            Sorted copy of cidr list
        """
        return sort_cidrs(cidrs)

    @staticmethod
    def sort_ips(ips: list[str]) -> list[str]:
        """
        Sort a list of IP addresses.

        Args:
            ips (list[str]):
            list of ips to be sorted.

        Returns:
            list[str]:
            Sorted copy of ips.
        """
        return sort_ips(ips)

    @staticmethod
    def sort_nets(nets: list[IPvxNetwork]) -> list[IPvxNetwork]:
        """
        Sort a list of networks.

        Args:
            nets (list[IPvxNetwork]):
                list of networks to be sorted.

        Returns:
            list[IPvxNetwork]:
                Sorted copy of networks.
        """
        return sort_nets(nets)

    @staticmethod
    def get_host_bits(ip: str, pfx: int = 24) -> int:
        """
        Gets the host bits from an IP address given the netmask.

        Args:
            ip (str):
            The IP to examine.

            pfx (int):
            The cidr prefix.

        Returns:
            int:
            The host bits from the IP.
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

        Args:
            cidr (str):
            Cidr string to clean up.

        Returns:
            str | None:
             - cidr string if valid
             - None if cidr is invalid.

        """
        return clean_cidr(cidr)

    @staticmethod
    def clean_cidrs(cidrs: list[str]) -> list[str]:
        """
        Clean list of cidrs.

        Similar to clean_cidr() but for a list.

        Args:
            cidrs (list[str]):
            list of cidr strings to clean up.

        Returns:
            list[str]:
            list of cleaned cidrs.
            If input cidr is invalid then its returnded as None

        """
        return clean_cidrs(cidrs)

    @staticmethod
    def fix_cidr_host_bits(cidr: str, verb: bool = False) -> str:
        """
        zero out any host bits.

        A strictly valid cidr address must have host bits set to zero.

        Args:
            cidr (str):
            The cidr to "fix" if needed.

            verb (bool):
            Some info on stdout when set True. Defaults to False.

        Returns:
            str:
            The cidr with any non-zero host bits now zeroed out.

        """
        return fix_cidr_host_bits(cidr, verb)

    @staticmethod
    def fix_cidrs_host_bits(cidrs: list[str], verb: bool = False) -> list[str]:
        """
        zero any host bits for a list of cidrs.

        Similar to fix_cidr_host_bits() but for a list of cidrs.

        Args:
            cidrs (list[str]):
            list of cidrs to fix up.

            verb (bool):
            Some info on stdout when set True. Defaults to False.

        Returns:
            list[str]:
            The list of cidrs each with any non-zero host bits now zeroed out.

        """
        return fix_cidrs_host_bits(cidrs, verb)

    @staticmethod
    def is_valid_ip4(address: Any) -> bool:
        """
        check if valid IPv4 address or cidr.

        Args:
            address (Any):
            Check if this is a valid IPv4 address or cidr.

        Returns:
            bool:
            True if valid IPv4 else False
        """
        return is_valid_ip4(address)

    @staticmethod
    def is_valid_ip6(address: Any) -> bool:
        """
        check if valid IPv6 address or cidr.

        Args:
            address (Any):
            Check if this is a valid IPv6 address or cidr.

        Returns:
            bool:
            True if valid IPv6 else False
        """
        return is_valid_ip6(address)

    @staticmethod
    def is_valid_cidr(address: Any) -> bool:
        """
        Check if address is a valid ip or cidr network.

        Args:
            address (Any):
            Address to check. Host bits set is permitted for a cidr network.

        Returns:
            bool:
            True/False if address is valid IPv4 or IPv6 address or network.
        """
        return is_valid_cidr(address)

    @staticmethod
    def cidr_iptype(address: Any) -> str:
        """
        Determines if address string is valid ipv4 or ipv6 or not.

        Args:
            address (Any):
                address or cidr string

         Returns:
            str :
                'ip4' or 'ip6' or empty string, '', if address invalid.
                Note. Earlier versions returned None instead of
                empty string if unable to be converted.
        """
        return cidr_iptype(address)

    @staticmethod
    def cidr_type_network(cidr: str) -> tuple[str, type[IPvxNetwork]]:
        """
        Cidr Network Type.

        Args:
            cidr (str):
            Cidr string to examine

        Returns:
            tuple[str, IPvxNetwork]:
            tuple(ip-type, net-type). ip-type is a string  ('ip4', 'ip6') while
            network type is IPv4Network or IPv6Network
        """
        return cidr_type_network(cidr)

    @staticmethod
    def range_to_cidrs(addr_start: IPAddress, addr_end: IPAddress,
                       string: bool = False) -> list[IPvxNetwork] | list[str]:
        """
        Generate a list of cidr/nets from an IP range.

        Args:
            addr_start (IPAddress):
            Start of IP range

            addr_end (IPAddress):
            End of IP range

            string (bool):
            If True then returns list of cidr strings otherwise IPvxNetwork

        Returns:
            list[IPvxNetwork] | list[str]
            list of cidr network blocks representing the IP range.
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

        Args:
            net (IPvxNetwork):
            The network (IPvxNetwork) to examine.

            string (bool):
            If True then returns cidr strings instead of IPvxAddress

        Returns:
            tuple[IPAddress, IPAddress]:
            tuple (ip0, ip1) of first and last IP address in net
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

        Args:
            cidr (str):
            The cidr string to examine.

            string (bool):
            If True then returns cidr strings instead of IPvxAddress

        Returns:
            tuple[IPAddress, IPAddress]:
            tuple (ip0, ip1) of first and last IP address in net
            (ip0, ip1) are IPvxAddress or str when string is True
        """
        if string:
            return cidr_to_range_cidrs(cidr)
        return cidr_to_range_nets(cidr)

    @staticmethod
    def net_range_split(net: IPvxNetwork) -> tuple[IPvxAddress, IPvxAddress, IPvxAddress]:
        """
        Convert network to IP Range.

        Args:
            net (IPvxNetwork):
            The network (IPvxNetwork) to examine.

            string (bool):
            If True then returns cidr strings instead of IPvxAddress

        Returns:
            tuple[, IPvxAddressIPAddress, , IPvxAddressIPAddress, IPvxAddress]:
            that are the first IP, middle IP and last IP in the cidr block
        """
        return net_range_split(net)

    @staticmethod
    def cidr_range_split(cidr: str) -> tuple[str, str, str]:
        """
        Convert network to IP Range.

        Args:
            net (IPvxNetwork):
            The network (IPvxNetwork) to examine.

            string (bool):
            If True then returns cidr strings instead of IPvxAddress

        Returns:
            tuple[str, str, str]:
            that are strings of the first IP, middle IP and last IP in the cidr block
        """
        return cidr_range_split(cidr)

    @staticmethod
    def is_rfc_1918(cidr: str) -> bool:
        """
        Check if cidr is any RFC 1918.

        Args:
            cidr (str):
            IP or Cidr to check if RFC 1918.

        Returns:
            bool:
            True if cidr is an RFC 1918 address.
            False if not.
        """
        return is_rfc_1918(cidr)

    @staticmethod
    def rfc_1918_nets() -> list[IPvxNetwork]:
        """
        Return list of rfc 1918 networks

        Returns:
            list[IPv4Network]:
            list of RFC 1918 networks.
        """
        return rfc_1918_nets()

    @staticmethod
    def rfc_1918_cidrs() -> list[str]:
        """
        Return list of rfc 1918 networks cidr strings

        Returns (list[str]):
            list of RFC 1918 networks as cidr strings
        """
        return rfc_1918_cidrs()

    @staticmethod
    def remove_rfc_1918(cidrs_in: str | list[str]
                        ) -> tuple[str | list[str], str | list[str]]:
        """
        Given list of cidrs, return list without any rfc 1918

        Args:
            cidrs_in (str | list[str]:
            Cidr string or list of cidr strings.

        Returns:
            tuple[str | list[str], str | list[str]]:
            Returns (tuple[cidrs_cleaned, rfc_1918_cidrs_found]):

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

        Args:
            cidrs (list[str]):
                list of cidr strings
        Returns:
            tuple[ip4: list[str], ip6: list[str], other: list[str]]
            Tuple of lists of ipv4, ipv6 and unknown.
        """
        return cidrs_split_type(cidrs)

    @staticmethod
    def compact(cidrs: list[str]) -> list[str]:
        """
        Compact list of cidrs - can be mixed ipv4/ipv6.
        Returns 1 type, making type annotation simpler for caller.

        Args:
            cidrs (list[str]):
                Input list of cidr strings.

        Returns:
            list[str]:
                Compacted list of cidrs. If mixed ipv4 is before ipv6

        Recommended methods are compact() or compact_nets().
        Others are kept for backward compatibility.
        """
        return compact_cidrs(cidrs)

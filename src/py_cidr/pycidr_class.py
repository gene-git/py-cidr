# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
PyCidr provides a suitr of common network CIDR utilities

- PyCidr works esclusively with strings. 
  This contrasts with the older Cidr class which also supports Python's ipaddress.
"""
# pylint: disable=too-many-public-methods
from cidrtools import CidrBlock, CidrBlocks, CidrTools
from ._version import version


class PyCidr:
    """
    Provides a suite of network CIDR tools using the cidrtools compiled library.

    All mathods are static and are called without need to instantiate the class.
    For example:

        new_cidrs = PyCidr.compact(cidrs)

    It does not use or support any data types from ipaddress (far too slow)
    """
    @staticmethod
    def version() -> str:
        """
        :returns: Returns the py-cidr Version
        """
        return version()

    @staticmethod
    def ct_version() -> str:
        """
        :returns: The cidrtools library version
        """
        return CidrTools.ct_version()

    @staticmethod
    def set_prefix(cidr: str, prefix: int) -> str:
        """
        Set new prefix for cidr and return new cidr string.

        :param cidr: Cidr string to use
        :prefix: The new prefix to use
        :returns: Cidr string using the specified prefix
        """
        cidr_block = CidrBlock(cidr)
        cidr_block.set_prefix(prefix)
        return str(cidr_block)

    @staticmethod
    def is_subnet(cidr: str, cidrs: list[str]) -> bool:
        """
        Check if cidr is a subnet of any of the list of IPvxNetworks .

        :param cidr: Cidr string to check.
        :param cidrs: list of network blocks to check.
        :returns: True if cidr is subnet of any of the cidrs list, else False.
        """
        if not (cidr and cidrs):
            return False

        cidr_block = CidrBlock(cidr)
        cidr_blocks = CidrBlocks(cidrs)

        return cidr_block.is_subnet_of(cidr_blocks)

    @staticmethod
    def exclude_cidrs(all_cidrs: list[str], excluded_cidrs: list[str]) -> list[str]:
        """
        Return new list of cidrs made by removing all excluded_cidrs from all_cidrs.
        Safely segregates mixed stacks to prevent invalid cross-version failures.

        :param all_cidrs: The full list of cidrs
        :excluded_cidrs: The cidrs to be removed from the full list
        :returns: Mew list of cidrs after the excluded_cidrs are removed.
        """
        cidr_blocks = CidrBlocks(all_cidrs)
        excluded_cidr_blocks = CidrBlocks(excluded_cidrs)
        cidr_blocks.exclude(excluded_cidr_blocks)
        return cidr_blocks.to_strings()

    @staticmethod
    def sort(cidrs: list[str]) -> list[str]:
        """
        Sort the list of cidr strings.

        :param cidrs: list of cidrs.
        :returns: Sorted copy of cidr list
        """
        cidr_blocks = CidrBlocks(cidrs)
        cidr_blocks.sort()
        return cidr_blocks.to_strings()

    @staticmethod
    def get_host_bits(cidr: str) -> str:
        """
        Extracts the host bits of an IPv4 or IPv6 address
        by masking off the network bits defined by the prefix.

        :param cidr: The cidr to examine.
        :returns: String with network bits zero showing host bit.
        """
        cidr_block = CidrBlock(cidr)
        return str(cidr_block.get_host_bits())

    @staticmethod
    def format_host_bits(cidr: str) -> str:
        """
        Extracts the host bits of an IPv4 or IPv6 address
        by masking off the network bits defined by the prefix.

        alias of get_host_bits().

        :param cidr: The cidr to examine.
        :returns: String with network bits zero showing host bit.
        """
        cidr_block = CidrBlock(cidr)
        return str(cidr_block.format_host_bits())

    @staticmethod
    def clean_cidr(cidr: str) -> str:
        """
        Clean up a cidr address.

        What it does:
         - Ensures host bits are set to zero to match the prefix.
         - Ensure the prefix is appropriate for the IP family,
           bounded by /32 or /128 for IPv4 or IPv6.
         - Non-cidr (bad) strings are set to '' 

        :param cidr: Cidr string to clean up.
        :returns: cidr string if valid (empty if not valid)
        """
        cidr_block = CidrBlock(cidr)

        if not cidr_block:
            return ''

        if not cidr_block.clean():
            return ''

        return str(cidr_block)

    @staticmethod
    def clean_cidrs(cidrs: list[str]) -> list[str]:
        """
        Takes a list of raw input CIDR strings, filters out any invalid items entirely,
        and returns a clean list of canonical networks with corrected host bits.
        Skips invalid entries completely instead of leaving them as empty strings.
        
        :param cidrs: List of cidr strings to be cleaned
        :returns: New list of cidrs that are now clean. Bad cidrs are returned 
                  as empty strings.
        """
        cidr_blocks = CidrBlocks(cidrs)
        cidr_blocks.clean()
        return cidr_blocks.to_strings()

    @staticmethod
    def fix_host_bits(cidr: str) -> str:
        """
        Ensures that host bits in an IPv4 or IPv6 CIDR string are set to 0.

        Examples:
            "10.0.0.22/32" -> "10.0.0.22/32"
            "10.0.0.22/24" -> "10.0.0.0/24"

        A strictly valid cidr address must have host bits set to zero.

        :param cidr: The cidr to "fix" if needed.
        :returns: The cidr with any non-zero host bits now zeroed out.
        """
        cidr_block = CidrBlock(cidr)
        cidr_block.fix_host_bits()
        return str(cidr_block)

    @staticmethod
    def is_valid_ipv4(cidr: str) -> bool:
        """
        Check if input is a valid IPv4 cidr or IP address

        :param cidr: Check if this cidr is valid.
        :returns: True if valid IPv4 else False
        """
        try:
            cidr_block = CidrBlock(cidr)
        except ValueError:
            return False
        return cidr_block.is_ipv4

    @staticmethod
    def is_valid_ipv6(cidr: str) -> bool:
        """
        Check if input is a valid IPv6 cidr or IP address

        :param cidr: Check if this is a valid IPv6 address or cidr.
        :returns: True if valid IPv6 else False
        """
        try:
            cidr_block = CidrBlock(cidr)
        except ValueError:
            return False
        return cidr_block.is_ipv6

    @staticmethod
    def is_valid_cidr(cidr: str) -> bool:
        """
        Check if string is valid cidr or IP address (either IPv4 or IPv6)
        Equivalen to
        - is_valid_ipv4(cidr) or is_valid_ipv6(cidr)

        :param: Address to check. Host bits set is permitted for a cidr network.
        :returns: True/False if address is valid IPv4 or IPv6 address or network.
        """
        try:
            cidr_block = CidrBlock(cidr)
        except ValueError:
            return False
        is_valid = bool(cidr_block.is_ipv4_or_ipv6)
        return is_valid

    @staticmethod
    def ip_type(cidr: str) -> str:
        """
        Determines if address string is valid ipv4 or ipv6 or not.

        :param cidr: ip address or cidr string
        :returns: 'ip4' or 'ip6' or empty string, '', if invalid address
        """
        try:
            cidr_block = CidrBlock(cidr)
        except ValueError:
            return ''

        if cidr_block.is_ipv4:
            return 'ip4'

        if cidr_block.is_ipv6:
            return 'ip6'

        return ''

    @staticmethod
    def ip_version(cidr: str) -> int:
        """
        Determines the IP version number (4 or 6 or 0 if neither)

        :param cidr: IP addess or cidr string.
        :returns: 4 if IPv4,  6 if IPv6, 0 otherwise
        """
        cidr_block = CidrBlock(cidr)

        if cidr_block.is_ipv4:
            return 4

        if cidr_block.is_ipv6:
            return 6

        return 0

    @staticmethod
    def range_to_cidrs(start_ip: str, end_ip: str) -> list[str]:
        """
        Generate a list of cidrs from an IP range.

        :param start_ip: First IP in range
        :param end_ip: Last IP in range
        :returns: list of cidr network blocks representing the IP range.
        """
        cidr_blocks = CidrTools.range_to_cidrs(start_ip, end_ip)
        return cidr_blocks.to_strings()

    @staticmethod
    def cidr_to_range(cidr: str) -> tuple[str, str, str]:
        """
        Cidr string to an IP Range : (First, Middle, Last) IPs

        :param cidr: The cidr string to examine.
        :returns: A tuple (ip0, mid, ip1) First, Middle and Last IP address of the cidr block.
        """
        cidr_block = CidrBlock(cidr)
        (first, mid, last) = cidr_block.to_range_mid()
        return (first, mid, last)

    @staticmethod
    def is_rfc_1918(cidr: str) -> bool:
        """
        Check if cidr is any RFC 1918.

        :param cidr: IP or Cidr to check if RFC 1918.
        :returns: True if cidr is an RFC 1918 address, False if not.
        """
        cidr_block = CidrBlock(cidr)
        rfc_1918 = PyCidr.rfc_1918_cidrs()
        rfc_1918_cidrs = CidrBlocks(rfc_1918)

        return cidr_block.is_subnet_of(rfc_1918_cidrs)

    @staticmethod
    def rfc_1918_cidrs() -> list[str]:
        """
        Return list of rfc 1918 networks cidr strings

        :returns: list of RFC 1918 networks as cidr strings
        """
        rfc_1918 = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
        return rfc_1918

    @staticmethod
    def remove_rfc_1918(cidrs: list[str]) -> list[str]:
        """
        Given list of cidrs, return list without any rfc 1918.

        :param cidrs: list of cidr strings.
        :returns: List of cidrs with any RFC 1918 addresses removed.
        """
        rfc_1918 = PyCidr.rfc_1918_cidrs()
        rfc_1918_cidrs = CidrBlocks(rfc_1918)
        cidr_blocks = CidrBlocks(cidrs)
        cidr_blocks.exclude(rfc_1918_cidrs)

        return cidr_blocks.to_strings()

    @staticmethod
    def split_by_iptype(cidrs: list[str]) -> tuple[list[str], list[str]]:
        """
        Split a list of cidrs into ipv4 and ipv6 lists.
        Historical Alias of split_by_family()

        :param cidrs: list of cidr strings
        :returns: Tuple of an ipv4 cidr list and an ipv6 cidr list
        """
        return PyCidr.split_by_family(cidrs)

    @staticmethod
    def split_by_family(cidrs: list[str]) -> tuple[list[str], list[str]]:
        """
        Split a list of cidrs into ipv4 and ipv6 lists.

        :param cidrs: list of cidr strings
        :returns: Tuple of an ipv4 cidr list and an ipv6 cidr list
        """
        cidr_blocks = CidrBlocks(cidrs)
        (v4_blocks, v6_blocks) = cidr_blocks.split_by_family()
        return (v4_blocks.to_strings(), v6_blocks.to_strings())

    @staticmethod
    def compact(cidrs: list[str]) -> list[str]:
        """
        Compact list of cidrs - can be mixed ipv4/ipv6.
        Returns 1 type, making type annotation simpler for caller.

        :param cidrs: Input list of cidr strings.
        :returns: Compacted list of cidrs. If mixed ipv4 is before ipv6
        """
        cidr_blocks = CidrBlocks(cidrs)
        cidr_blocks.compact()
        return cidr_blocks.to_strings()

    @staticmethod
    def cidr_parts(cidr: str) -> tuple[str, int]:
        """
        Unified entry point splitting any valid IPv4 or IPv6 CIDR block into a
        clean base network address string and its integer prefix length.

        Examples:
            cidr_parts("10.0.0.22/24")    -> ("10.0.0.0", 24)
            cidr_parts("2001:db8::1/64") -> ("2001:db8::", 64)

        :param cidr: The cidr string to examine
        :returns: Tuple of (ip-address, prefix)
        """
        cidr_block = CidrBlock(cidr)
        (ip_str, prefix) = cidr_block.cidr_parts()
        return (ip_str, prefix)

    @staticmethod
    def num_ips(cidr: str) -> int:
        """
        Returns the number of IP addresses in the cidr block.

        :param cidr: The cidr to examine
        :returns: The number of IP addresses in the range. For IPv6 
                  This number is capped at 2^64 (pee cidrtools library)
        """
        cidr_block = CidrBlock(cidr)
        return cidr_block.num_ips

    @staticmethod
    def subnets_split(cidr: str, new_prefix: int) -> list[str]:
        """
        Splits an IPv4 or IPv6 CIDR block into smaller subnets of a larger prefix size.
        If the new prefix is smaller or equal to the existing one, returns the original CIDR.

        Examples:
            subnets_split("10.0.0.0/23", 24)    -> ["10.0.0.0/24", ""10.0.1.0/24")

        :param cidr: the cidr to work on
        :param new_prefix: the prefix to use to split cidr into smaller subnets
        :returns: list of subnets - if compacted will be the input cidr block.
        """
        cidr_block = CidrBlock(cidr)
        cidr_blocks = cidr_block.split(new_prefix)
        return cidr_blocks.to_strings()

    @staticmethod
    def cidrs_intersection(cidrs1: list[str], cidrs2: list[str]) -> list[str]:
        """
        Returns the intersection subnets of 2 lists of cidrs.

        :param cidrs1: First set of cidrs
        :param cidrs2: Second set of cidrs
        :returns: List of the intersecting subnets (may be empty).
        """
        if not cidrs1 or not cidrs2:
            return []

        cidr1_blocks = CidrBlocks(cidrs1)
        cidr2_blocks = CidrBlocks(cidrs2)
        cidrs = CidrBlocks()
        if cidr1_blocks.intersection(cidr2_blocks, cidrs) != 0:
            return []
        return list(cidrs)

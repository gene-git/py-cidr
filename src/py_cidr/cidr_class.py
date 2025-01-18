# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Class providing some common CIDR utilities
'''
# pylint: disable=too-many-public-methods
from typing import TypeAlias
import ipaddress
import re
from ipaddress import (AddressValueError, NetmaskValueError)
from ipaddress import (IPv4Network, IPv6Network, IPv4Address, IPv6Address)

IPvxNetwork: TypeAlias = IPv4Network|IPv6Network
IPvxAddress: TypeAlias = IPv4Address|IPv6Address
IPAddress: TypeAlias = IPvxAddress|str

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
        if not cidr:
            return None

        return ipaddress.ip_network(cidr, strict=strict)

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
        if not cidrs or len(cidrs) < 1:
            return []
        nets = [ipaddress.ip_network(cidr, strict=strict) for cidr in cidrs]
        return nets

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
        cidrs = [str(net) for net in nets]
        return cidrs

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
        if not ip:
            return None

        ipin = ip
        if '/' in ip:
            ipin = re.sub(r'/.*$', '',  ip)

        try:
            addr = ipaddress.ip_address(ipin)
        except AddressValueError:
            addr = None
        return addr

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
        addresses = [Cidr.ip_to_address(ip) for ip in ips]
        return addresses

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
        ips = [str(address) for address in addresses]
        return ips

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
        addr = Cidr.ipaddr_cidr_from_string(cidr)
        addr_new = addr.supernet(new_prefix=prefix)
        return str(addr_new)

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
        if not addr:
            return None
        if Cidr.is_valid_ip4(addr):
            return ipaddress.IPv4Network(addr, strict=strict)
        if Cidr.is_valid_ip6(addr):
            return ipaddress.IPv6Network(addr, strict=strict)
        return None

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
        if not cidr or not ipa_nets:
            return False

        this_net = Cidr.cidr_to_net(cidr)
        if not this_net:
            return False

        this_ipt = Cidr.cidr_iptype(this_net)

        for net in ipa_nets:
            net_ipt = Cidr.cidr_iptype(net)
            if net_ipt != this_ipt:
                return False
            if this_net.subnet_of(net):
                return True

        return False

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
        if not addr:
            return None
        ipt = type(addr)
        if ipt in (IPv4Address,IPv4Network):
            return 'ip4'
        if ipt in (IPv6Address,IPv6Network):
            return 'ip6'
        return None

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
        if not cidrs_in:
            return cidrs_in

        ip_nets = [ipaddress.ip_network(cidr, strict=False) for cidr in cidrs_in]
        cidrs_out = []
        for cidr in ipaddress.collapse_addresses(ip_nets):
            if string:
                cidrs_out.append(str(cidr))
            else:
                cidrs_out.append(cidr)
        return cidrs_out

    @staticmethod
    def compact_cidrs(cidrs:[str], nets=False) -> [str|IPvxNetwork]:
        ''' combine em '''
        ip_nets = [ipaddress.ip_network(cidr, strict=False) for cidr in cidrs]
        if nets:
            return ip_nets
        compact = [str(net) for net in ipaddress.collapse_addresses(ip_nets)]
        return compact

    @staticmethod
    def compact_nets(nets:[IPvxNetwork]) -> [IPvxNetwork]:
        ''' combine em '''
        compact = list(ipaddress.collapse_addresses(nets))
        return compact

    @staticmethod
    def net_exclude(net1:IPvxNetwork, nets2:[IPvxNetwork]) -> [IPvxNetwork]:
        '''
        Exclude net1 from any of networks in net2
        return resulting list of nets (without net1)
        '''
        if not net1 or not nets2:
            return nets2

        nets = []
        for net in nets2:
            if net1.subnet_of(net):
                # remove the net1 subnet from net
                nets += list(net.address_exclude(net1))
            elif net.subnet_of(net1):
                # remove net entirely as part of net1
                continue
            else:
                # keep net
                nets.append(net)
        nets = Cidr.compact_nets(nets)
        return nets

    @staticmethod
    def nets_exclude(nets1:[IPvxNetwork], nets2:[IPvxNetwork]) -> [IPvxNetwork]:
        '''
        Exclude every nets1 network from from any networks in nets2
        '''
        final = []
        nets1 = Cidr.compact_nets(nets1)
        final = Cidr.compact_nets(nets2)
        for net1 in nets1:
            final = Cidr.net_exclude(net1, final)
        return final

    @staticmethod
    def cidrs_exclude(cidrs1:[str], cidrs2:[str]) -> [str]:
        ''' old name '''
        return Cidr.cidrs2_minus_cidrs1(cidrs1, cidrs2)

    @staticmethod
    def cidrs2_minus_cidrs1(cidrs1:[str], cidrs2:[str]) -> [str]:
        '''
        Exclude all of cidrs1 from cidrs2
        i.e. return cidrs2 - cidrs1
        '''
        nets1 = [ipaddress.ip_network(cidr, strict=False) for cidr in cidrs1]
        nets2 = [ipaddress.ip_network(cidr, strict=False) for cidr in cidrs2]
        nets = Cidr.nets_exclude(nets1, nets2)
        cidrs = [str(net) for net in nets]
        return cidrs

    @staticmethod
    def cidr_exclude(cidr1:str, cidrs2:[str]) -> [str]:
        '''
        Exclude cidr1 from any of networks in cidrs2
        return resulting list of cidrs (without cidr1)
        '''
        if not cidr1 or not cidrs2:
            if not cidrs2:
                return []
            return cidrs2

        net1 = Cidr.cidr_to_net(cidr1)
        nets2 = Cidr.compact_cidrs(cidrs2)
        nets = Cidr.net_exclude(net1, nets2)
        return Cidr.nets_to_cidrs(nets)

    @staticmethod
    def sort_cidrs(cidrs:[str]) -> [str]:
        '''
        Sort the list of cidr strings
        '''
        nets = Cidr.cidrs_to_nets(cidrs)
        if not nets:
            return cidrs
        nets.sort()
        cidrs_sorted = Cidr.nets_to_cidrs(nets)
        return cidrs_sorted

    @staticmethod
    def sort_ips(ips:[str]) -> [str]:
        '''
        Sort the list of cidr strings
        '''
        addresses = Cidr.ips_to_addresses(ips)
        addresses.sort()
        ips_sorted = Cidr.addresses_to_ips(addresses)
        return ips_sorted

    @staticmethod
    def get_host_bits(ip:str, pfx:int=24):
        '''
        Gets the host bits from an IP address given the netmask
        '''
        ipa = ipaddress.ip_address(ip)
        net = ipaddress.ip_network(ip)
        netpfx = net.supernet(new_prefix=pfx)

        hostmask = netpfx.hostmask
        host_bits = int(ipa) & int(hostmask)

        return host_bits

    @staticmethod
    def clean_cidr(cidr:str) -> str:
        '''
        returns None if not valid
         - we to fix class C : a.b.c -> a.b.c.0/24
        '''
        if Cidr.is_valid_cidr(cidr):
            cidr = Cidr.fix_cidr_host_bits(cidr)
            return cidr

        if cidr.count('.') == 2:
            cidr = cidr + '.0/24'

        if Cidr.is_valid_cidr(cidr):
            cidr = Cidr.fix_cidr_host_bits(cidr)
            return cidr

        return None

    @staticmethod
    def clean_cidrs(cidrs:[str]) -> [str]:
        ''' clean cidr array '''
        if not cidrs:
            return []

        cleans = []
        for cidr in cidrs:
            clean = Cidr.clean_cidr(cidr)
            if clean:
                cleans.append(clean)
        return cleans

    @staticmethod
    def fix_cidr_host_bits(cidr:str, verb:bool=False):
        ''' zero any host bits '''
        net = Cidr.cidr_to_net(cidr)
        fix = str(net)
        if verb and cidr != fix:
            print(f'\t Fixed: {cidr} -> {fix}')
        return fix

    @staticmethod
    def fix_cidrs_host_bits(cidrs:[str], verb:bool=False):
        ''' zero any host bits '''
        if not cidrs:
            return cidrs

        fixed = []
        for cidr in cidrs:
            fix = str(Cidr.cidr_to_net(cidr))
            if verb and cidr != fix:
                print(f'\t Fixed: {cidr} -> {fix}')
            fixed.append(fix)

        return fixed

    @staticmethod
    def is_valid_ip4(address) -> bool:
        ''' check if valid address or cidr '''
        try:
            _check = IPv4Network(address, strict=False)
            return True
        except (AddressValueError, NetmaskValueError, ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_ip6(address) -> bool:
        ''' check if valid address or cidr '''
        try:
            _check = IPv6Network(address, strict=False)
            return True
        except (AddressValueError, NetmaskValueError, ValueError, TypeError):
            return False

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
        if not address:
            return False
        try:
            _check = ipaddress.ip_network(address, strict=False)
            return True
        except (AddressValueError, NetmaskValueError, ValueError, TypeError):
            return False
        #if Cidr.is_valid_ip4(address) or Cidr.is_valid_ip6(address):
        #    return True
        #return False

    @staticmethod
    def cidr_iptype(address:str) -> str|None :
        '''
        Determines if an IP address or CIDR string is ipv4 or ipv6

        :param address:
            ip address or cidr string

         :returns:
            'ip4' or 'ip6' or None
        '''
        if not address:
            return None

        if Cidr.is_valid_ip4(address) :
            return 'ip4'

        if Cidr.is_valid_ip6(address):
            return 'ip6'

        return None

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
        ipt = None
        IPNetwork = IPv4Network

        if Cidr.is_valid_ip4(cidr):
            ipt = 'ip4'
            IPNetwork = IPv4Network

        elif Cidr.is_valid_ip6(cidr):
            ipt = 'ip6'
            IPNetwork = IPv6Network

        return (ipt, IPNetwork)

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
        if not net:
            return (None, None)

        ip0 = net.network_address
        ip1 = net.broadcast_address

        if string:
            ip0 = str(ip0)
            ip1 = str(ip1)
        return (ip0, ip1)

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
        net = Cidr.cidr_to_net(cidr, strict=False)
        return Cidr.net_to_range(net, string)

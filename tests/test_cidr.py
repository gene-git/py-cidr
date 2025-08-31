"""
Test:
    Read / Write cache file
"""
from py_cidr.cidr_class import Cidr


class TestCidr:
    """
    Cidr Class Tests
    """

    def test_valid(self):
        """ test valid cidrs """
        ip4_good = '10.1.2.0/24'
        ip4_bad = '10.1.2.A/24'
        ip6_good = '2025::0/64'
        ip6_bad = '2025::1::2::3/56'

        num_good = 0
        num_good += 1 if Cidr.is_valid_cidr(ip4_good) else 0
        num_good += Cidr.is_valid_cidr(ip6_good)

        num_bad = 0
        num_bad += 1 if not Cidr.is_valid_cidr(ip4_bad) else 0
        num_bad += 1 if not Cidr.is_valid_cidr(ip6_bad) else 0

        all_ok = num_good == 2 and num_bad == 2
        assert all_ok

    def test_compact(self):
        """ test compacting cidrs """
        cidrs = ['10.0.0.0/24', '10.0.1.0/24', '10.10.0.0/16']

        compact = Cidr.compact(cidrs)
        all_ok = False
        if compact and len(compact) == 2:
            all_ok = True
        assert all_ok

    def test_compact_mixed(self):
        """ test compacting ipv4/ipv6 mixed cidrs """
        cidrs = ['10.0.0.0/24', '10.0.1.0/24', '10.10.0.0/16']
        cidrs += ['fc00:22:22::1', 'fc00:22:22::/64', 'fc00:22:22::10']

        compact = Cidr.compact(cidrs)
        all_ok = False
        if compact and len(compact) == 3:
            all_ok = True
        assert all_ok

    def test_fix_hostbits(self):
        """ fix host bits """
        cidr = '10.1.1.22/24'
        target = '10.1.1.0/24'
        cidr_fix = Cidr.fix_cidr_host_bits(cidr)

        all_ok = cidr_fix == target
        assert all_ok

    def test_set_prefix(self):
        """ fix host bits """
        cidr = '10.1.1.0/24'
        target = '10.1.0.0/16'

        cidr_fix = Cidr.cidr_set_prefix(cidr, 16)

        all_ok = cidr_fix == target
        assert all_ok

    def test_is_subnet(self):
        """ fix host bits """
        cidr = '10.1.1.0/24'
        super_cidrs = ['10.2.0.0/16', '10.1.0.0/16']
        super_nets = Cidr.cidrs_to_nets(super_cidrs)

        is_subnet = Cidr.cidr_is_subnet(cidr, super_nets)
        assert is_subnet

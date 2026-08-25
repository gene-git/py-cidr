"""
Test:
    Read / Write cache file
"""
# pylint: disable=duplicate-code
from py_cidr.pycidr_class import PyCidr


class TestPyCidr:
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
        num_good += 1 if PyCidr.is_valid_cidr(ip4_good) else 0
        num_good += PyCidr.is_valid_cidr(ip6_good)

        num_bad = 0
        num_bad += 1 if not PyCidr.is_valid_cidr(ip4_bad) else 0
        num_bad += 1 if not PyCidr.is_valid_cidr(ip6_bad) else 0

        all_ok = num_good == 2 and num_bad == 2
        assert all_ok

    def test_split_by_iptype(self):
        """ test that ipv4 can be split from ipv6"""
        v4s = ['10.0.0.0/24', '10.0.1.0/24', '10.10.0.0/16']
        v6s = ['fc00:22:22::1/128', 'fc00:22:22::/64']

        (cidrs_4, cidrs_6) = PyCidr.split_by_iptype(v4s + v6s)
        assert cidrs_4 == v4s
        assert cidrs_6 == v6s

    def test_compact(self):
        """ test compacting cidrs """
        cidrs = ['10.0.0.0/24', '10.0.1.0/24', '10.10.0.0/16']

        compact = PyCidr.compact(cidrs)
        all_ok = False
        if compact and len(compact) == 2:
            all_ok = True
        assert all_ok

    def test_compact_mixed(self):
        """ test compacting ipv4/ipv6 mixed cidrs """
        cidrs = ['10.0.0.0/24', '10.0.1.0/24', '10.10.0.0/16']
        cidrs += ['fc00:22:22::1', 'fc00:22:22::/64', 'fc00:22:22::10']

        compact = PyCidr.compact(cidrs)
        all_ok = False
        if compact and len(compact) == 3:
            all_ok = True
        assert all_ok

    def test_fix_hostbits(self):
        """ fix host bits """
        cidr = '10.1.1.22/24'
        target = '10.1.1.0/24'
        cidr_fix = PyCidr.fix_host_bits(cidr)

        all_ok = cidr_fix == target
        assert all_ok

    def test_set_prefix(self):
        """ fix host bits """
        cidr = '10.1.1.0/24'
        target = '10.1.0.0/16'

        cidr_fix = PyCidr.set_prefix(cidr, 16)

        all_ok = cidr_fix == target
        assert all_ok

    def test_is_subnet(self):
        """ fix host bits """
        cidr = '10.1.1.0/24'
        super_nets = ['10.2.0.0/16', '10.1.0.0/16']

        is_subnet = PyCidr.is_subnet(cidr, super_nets)
        assert is_subnet

    def test_sort(self):
        """
        Sort cidr blocks
        """
        cidrs = ['10.2.0.0/16', '10.1.0.0/16', '1.1.1.0/23']
        cidrs += ['fc00:22:22::1', 'fc00:22:22::2', 'fc00:10:22::1']

        target = ['1.1.0.0/23', '10.1.0.0/16', '10.2.0.0/16', 'fc00:10:22::1/128',
                  'fc00:22:22::1/128', 'fc00:22:22::2/128']

        cidrs_sorted = PyCidr.sort(cidrs)
        assert cidrs_sorted == target

    def test_cidr_parts(self):
        """
        Splitting cidr into parts.
        """
        parts_1 = PyCidr.cidr_parts('10.0.0.22/24')
        target_1 = ('10.0.0.22', 24)

        parts_2 = PyCidr.cidr_parts('2001:db8::1/64')
        target_2 = ('2001:db8::1', 64)

        assert parts_1 == target_1
        assert parts_2 == target_2

    def test_cidrs_intersection(self):
        """
        Intersection of 2 cidr sets of cidrs
        """
        cidrs1 = ["192.168.1.0/24", "10.1.0.0/24"]
        cidrs2 = ["10.1.0.0/22", "100.100.100.0/23"]
        expect = ["10.1.0.0/24"]

        cidrs = PyCidr.cidrs_intersection(cidrs1, cidrs2)
        assert cidrs
        assert len(cidrs) == len(expect)
        assert cidrs == expect

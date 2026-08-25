"""
Test:
    Read / Write cache file
"""
# pylint: disable=too-few-public-methods
# pylint: disable=duplicate-code
import os
import shutil
from py_cidr import CidrMap
from py_cidr import PrefixVal


class _TestData:
    """
    Initialize for test
    Expect lookup_all:
    - [0] '10.0.0.0/22' -> ('10.0.0.0/22', aaa)
    - [1] '10.0.0.0/24' -> ('10.0.0.0/24', 'bbb', '10.0.0.0/22', aaa
    - [2] '10.0.1.0/24' -> ('10.0.1.0/24', 'ccc', '10.0.1.0/22', aaa
    - [3] '10.0.2.0/24' -> ('10.0.2.0/24', 'ddd', '10.0.2.0/22', aaa
    - [4] '10.0.5.0/24' -> ('10.0.5.0/24', 'eee')
    """
    def __init__(self):
        self.cidr_vals: list[PrefixVal] = [
                ('10.0.0.0/22', 'net-0/22'),
                ('10.0.0.0/24', 'net-0/24'),
                ('10.0.1.0/24', 'net-1/24'),
                ('10.0.2.0/24', 'net-2/24'),
                ('10.0.5.0/24', 'net-5/24'),
                ]

        pid: int = os.getpid()
        self.cache_dir: str = f'/tmp/_py-cidr-test/{pid}'
        os.makedirs(self.cache_dir, exist_ok=True)

    def clean(self):
        """
        Clean up mess
        """
        try:
            shutil.rmtree(self.cache_dir)
        except (FileNotFoundError, OSError):
            pass


class TestCidrMapNC:
    """
    Create cidr map
     - write to cache file
     - read cache file
     - confirm data read in is same.
    """

    def test_cidr_map_noncompact(self):
        """ write and read back """

        # create mape
        tdata = _TestData()
        cidr_map = CidrMap(tdata.cache_dir, compact=False)
        cidr_map.add_prefix_vals(tdata.cidr_vals)

        # save to cache
        cidr_map.save_cache()

        # check it has correct values for each cidr.
        num_prefix_match = 0
        num_val_match = 0
        num_total: int = len(tdata.cidr_vals)
        for cidr_val in tdata.cidr_vals:
            pval = cidr_map.lookup_lmp(cidr_val[0])
            num_prefix_match += bool(cidr_val[0] == pval[0])
            num_val_match += bool(cidr_val[1] == pval[1])

        assert num_prefix_match == num_total
        assert num_val_match == num_total

        # read cache and check LMP
        cidr_map2 = CidrMap(tdata.cache_dir)
        num_prefix_match = 0
        num_val_match = 0
        for cidr_val in tdata.cidr_vals:
            pval = cidr_map2.lookup_lmp(cidr_val[0])
            num_prefix_match += bool(cidr_val[0] == pval[0])
            num_val_match += bool(cidr_val[1] == pval[1])

        assert num_prefix_match == num_total
        assert num_val_match == num_total

        # all done
        tdata.clean()

    def test_cidr_map_subnet_noncompact(self):
        """ write and read back """

        tdata = _TestData()
        cidr_map = CidrMap(tdata.cache_dir, compact=False)
        cidr_map.add_prefix_vals(tdata.cidr_vals)

        # lookup cidr which is subnet of 2 of elems
        # -> ( '10.0.1.0/24', ' '10.0.0.0/22')
        cidr = '10.0.1.32/27'
        values_expect = ['net-0/22', 'net-1/24']
        cidr_vals = cidr_map.lookup_all(cidr)

        assert len(cidr_vals) == 2

        for (cidr, val) in cidr_vals:
            assert val in values_expect

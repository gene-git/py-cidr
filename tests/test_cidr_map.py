"""
Test:
    Read / Write cache file
"""
# pylint: disable=too-few-public-methods
import os
import shutil
from py_cidr import CidrMap


class _TestData:
    """
    Initialize for test
    """
    def __init__(self):
        self.cidrs: list[str] = ['10.0.0.0/24', '10.0.1.0/24', '10.0.2.0/24']
        self.values: list[str] = ['aaa', 'bbb', 'ccc']

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


class TestCidrMap:
    """
    Create cidr map
     - write to cache file
     - read cache file
     - confirm data read in is same.
    """

    def test_cidr_map(self):
        """ write and read back """

        tdata = _TestData()
        cidr_map = CidrMap(tdata.cache_dir)

        # create mape
        for (cidr, value) in zip(tdata.cidrs, tdata.values):
            cidr_map.add_cidr(cidr, value, None)

        # save to cache
        cidr_map.save_cache()

        # check it has correct values for each cidr.
        num_items = len(tdata.cidrs)
        num_found = 0
        for (cidr, value) in zip(tdata.cidrs, tdata.values):
            value_lookup = cidr_map.lookup(cidr)
            num_found += value_lookup == value
        assert num_found == num_items

        # read cache
        map2 = CidrMap(tdata.cache_dir)
        num_found = 0
        for (cidr, value) in zip(tdata.cidrs, tdata.values):
            value_lookup = map2.lookup(cidr)
            num_found += value_lookup == value
        assert num_found == num_items

        # all done
        tdata.clean()

    def test_cidr_map_subnet(self):
        """ write and read back """

        tdata = _TestData()
        cidr_map = CidrMap(tdata.cache_dir)

        # create mape
        for (cidr, value) in zip(tdata.cidrs, tdata.values):
            cidr_map.add_cidr(cidr, value, None)

        # save to cache
        cidr_map.save_cache()

        # lookup cidr which is subnet of one of elems
        cidr = '10.0.1.32/27'
        (cidr_found, val) = cidr_map.lookup_both(cidr)
        value = val if val is not None else ''

        assert cidr_found == '10.0.1.0/24'
        assert value == 'bbb'

        # all done
        tdata.clean()

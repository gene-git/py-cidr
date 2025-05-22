"""
Test:
    Read / Write cache file
"""
# pylint: disable=too-few-public-methods
import os
from py_cidr import IPvxNetwork
from py_cidr._cidr_nets import cidr_to_net
from py_cidr._cache_elem import CidrCacheElem
from py_cidr._cache_files import (read_cache_file, write_cache_file)


def _compare(ela: list[CidrCacheElem], elb: list[CidrCacheElem]) -> bool:
    """
    check if 2 elems are the same
    """
    if not ela or not elb:
        return False

    if len(ela) != len(elb):
        return False

    for (a, b) in zip(ela, elb):
        if not a.is_equal(b):
            return False
    return True


class _TestData:
    """
    Initialize for test
    """
    def __init__(self):
        self.nets: list[IPvxNetwork] = []
        self.elems: list[CidrCacheElem] = []
        self.cidrs: list[str] = ['10.0.0.0/24', '10.0.1.0/24', '10.0.2.0/24']

        pid: int = os.getpid()
        self.file: str = f'/tmp/_xxxx.{pid}'

        value = 1
        for cidr in self.cidrs:
            elem = CidrCacheElem()
            net = cidr_to_net(cidr)
            if net is not None:
                elem.net = net
            elem.val = value
            value += 1
            self.elems.append(elem)


class TestReadWriteCache:
    """
    Write cache file and read back.
    """

    def test_read_write_cache_file(self):
        """ write and read back """
        read_ok = write_ok = False
        data = _TestData()

        write_ok = write_cache_file(data.elems, data.file)
        assert write_ok

        if write_ok:
            elems = read_cache_file(data.file)
            read_ok = _compare(elems, data.elems)
            os.unlink(data.file)
        assert read_ok

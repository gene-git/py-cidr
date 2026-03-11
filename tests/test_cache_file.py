"""
Test:
    Read / Write cache file
"""
# pylint: disable=too-few-public-methods
import os

from pytricia import PyTricia

from py_cidr import PrefixVal
from py_cidr._prefix import PrefixMap


def _compare_pyt(pyt_a: PyTricia, pyt_b: PyTricia) -> bool:
    for pfx in pyt_a:
        if not (pyt_b.has_key(pfx) and pyt_b[pfx] == pyt_a[pfx]):
            return False
    return True


class _TestData:
    """
    Initialize for test
    """
    def __init__(self, compact: bool):
        self.compact = compact
        self.prefix_map: PrefixMap = PrefixMap(compact=compact)
        self.cidrs: list[str] = ['10.0.0.0/24', '10.0.1.0/24', '10.0.2.0/24']

        pid: int = os.getpid()
        self.file: str = f'/tmp/_xxxx.{pid}'

        cidr_vals: list[PrefixVal] = []
        val: int = 1
        for cidr in self.cidrs:
            val += 1
            cidr_vals.append((cidr, val))
        self.prefix_map.update(cidr_vals)

    def read_write_cache_file(self) -> tuple[bool, bool]:
        """
        write and read back
        - remove cache when done
        - returrn (write_status, read_status)
        """
        write_ok: bool = True
        read_ok: bool = True

        write_ok = self.prefix_map.write_cache_file(self.file)

        if write_ok:
            # read back into new cache
            prefix_map_read: PrefixMap = PrefixMap(compact=self.compact)
            prefix_map_read.read_cache_file(self.file)

            # compare
            if prefix_map_read.vers != self.prefix_map.vers:
                read_ok = False

            if prefix_map_read.compact != self.prefix_map.compact:
                read_ok = False

            if not _compare_pyt(prefix_map_read.pyt, self.prefix_map.pyt):
                read_ok = False
            try:
                os.unlink(self.file)
            except OSError:
                pass

        return (write_ok, read_ok)


class TestReadWriteCache:
    """
    Write cache file and read back.
    """

    def test_cache_read_write_compact(self):
        """
        Create compact cache - write and read back - check same
        """
        write_ok: bool = False
        read_ok: bool = False
        compact: bool = True
        data = _TestData(compact)

        (write_ok, read_ok) = data.read_write_cache_file()
        assert write_ok
        assert read_ok

    def test_cache_read_write_noncompact(self):
        """
        Create compact cache - write and read back - check same
        """
        write_ok: bool = False
        read_ok: bool = False
        compact: bool = False
        data = _TestData(compact)

        (write_ok, read_ok) = data.read_write_cache_file()
        assert write_ok
        assert read_ok

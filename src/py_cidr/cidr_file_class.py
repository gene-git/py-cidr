# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
 CidrFile class:
 Read/write a file with list of cidr blocks as strings
 For reading

 - comments ignored
 - pname = is path to the file.
 - cidr are all in column 1
"""
import os
import sys

from py_cidr.pycidr_class import PyCidr
from py_cidr._utils import open_file


def _has_cidr_data(row):
    """
    Return False if line starts with comment or newline etc.
    """
    if not row:
        return False

    if row[0] in ('#', '$', '!', ':', '', '\n'):
        return False
    return True


class CidrFile:
    """
    Some CIDR string file read/writ tools.

    All methods are static so no class instance variable needed.
    """
    @staticmethod
    def read_cidrs(fname: str | None, verb: bool = False) -> tuple[list[str], list[str]]:
        """
        Read file of cidrs and return tuple of separate lists (ip4, ip6).
         - if fname is None or sys.stdin then data is read from stdin.
         - only column 1 of file is used.
         - comments are ignored

        See also read_cidr_file() which returns all cidrs in one list.

        :param fname: File name to read. If None, then reads from stdin.
        :param verb: More verbose output when set to True.
        :returns: A tuple of lists (ipv4, ipv6) of cidrs separated into IPv4 and IPv6.
        """
        cidrs = CidrFile.read_cidr_file(fname, verb)
        (ip4, ip6) = PyCidr.split_by_family(cidrs)

        return (ip4, ip6)

    @staticmethod
    def read_cidr_file(fname: str | None, verb: bool = False) -> list[str]:
        """
         Read file of cidrs and return list of all IPv4 and IPv6.

         See read_cidrs() to have the cidrs split by IP family.

        :param fname: Path to file of cidrs to read. Stdin if set to None
        :param verb: More verbose output
        :returns: list of all cidrs (ip4 and ip6) read from the file
        """
        if verb:
            print(' \tread_cidr_file: {fname}')

        cidrs: list[str] = []

        if fname is not None and isinstance(fname, str):
            if os.path.exists(fname):
                fob = open_file(fname, 'r')
                rows = fob.readlines()
                fob.close()
            else:
                rows = []
        else:
            rows = sys.stdin.readlines()
        #
        # 1. remove rows with comments, empty etc
        # 2. drop all but first column
        #
        rows = [row for row in rows if _has_cidr_data(row.lstrip())]
        for row in rows:
            cols = row.split()
            if cols and cols[0]:
                cidrs.append(cols[0].rstrip())

        # cidrs = [clean for cidr in cidrs if (clean := clean_cidr(cidr))]
        cidrs = PyCidr.clean_cidrs(cidrs)
        return cidrs

    @staticmethod
    def read_cidr_files(targ_dir: str, file_list: list[str]) -> list[str]:
        """
        Read files in a directory and return merged list of cidr strings.

        :param targ_dir: Directory to find each file.
        :param file_list: read from this list of files found in in *targ_dir*
        :returns: list of all cidrs found in the files.
        """
        cidrs: list[str] = []
        if not targ_dir or not file_list:
            return cidrs

        for file in file_list:
            path = os.path.join(targ_dir, file)
            this_cidrs = CidrFile.read_cidr_file(path)
            cidrs += this_cidrs

        cidrs = PyCidr.clean_cidrs(cidrs)

        return cidrs

    @staticmethod
    def write_cidr_file(cidrs: list[str], pname: str) -> bool:
        """
        Write list of cidrs to a file.

        :param cidrs: list of cidr strings to write.
        :param pname: Path to file where cidrs are to be written.
        :returns: True if successful otherwise False.
        """
        data = '\n'.join(cidrs) + '\n'
        if not pname:
            fob = sys.stdout
        else:
            fob = open_file(pname, 'w')

        if fob:
            fob.write(data + '\n')
            if pname:
                fob.close()
            return True
        return False

    @staticmethod
    def copy_cidr_file(src_file: str, dst_file: str) -> bool:
        """
        Copy one file to another.

        :param src_file: Source file to copy.
        :param dst_file: Destination Where to save a copy
        :returns: True if all okay else False
        """
        is_okay = True
        if src_file.endswith('.ip4') or src_file.endswith('.ip6'):
            cidrs = CidrFile.read_cidr_file(src_file)
            if cidrs:
                cidrs = PyCidr.compact(cidrs)
                is_okay = CidrFile.write_cidr_file(cidrs, dst_file)
        return is_okay

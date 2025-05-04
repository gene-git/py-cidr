# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 CidrFile class:
 Read/write a file with list of cidr blocks as strings
 For reading
   - comments ignored
   - pname = is path to the file.
   - cidr are all in column 1
"""
from typing import (List, Tuple)
import os
import sys
from .cidr_class import (Cidr)
from ._cidr_compact import (compact_cidrs)
from ._files import open_file


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
    Provides common CIDR string file reader/writer tools.
    All methods are static so no class instance variable needed.
    """
    @staticmethod
    def read_cidrs(fname: str | None, verb: bool = False
                   ) -> Tuple[List[str], List[str]]:
        """
        Read file of cidrs and return tuple of separate lists (ip4, ip6).

         -  if fname is None or sys.stdin then data is read from stdin.
         -  only column 1 of file is used.
         -  comments are ignored

        Args:
            fname (str | None):
            File name to read.

            verb (bool):
            More verbose output when True.

        Returns:
            Tuple[List[str], List[str]]:
            Tuple of lists of cidrs (ip4, ip6)
        """
        if verb:
            print(' \tread_cidr_file: {fname}')

        ip4 = []
        ip6 = []

        if fname is not None and isinstance(fname, str):
            if os.path.exists(fname):
                fob = open_file(fname, 'r')
                rows = fob.readlines()
                fob.close()
            else:
                rows = []
        else:
            rows = sys.stdin.readlines()

        for row in rows:
            row.lstrip()
            if not _has_cidr_data(row):
                continue

            # Keep first column (also drops trailing comment or anything else)
            cols = row.split()
            if cols and cols[0]:
                row = cols[0].rstrip()

                iptype = Cidr.cidr_iptype(row)
                if not iptype:
                    continue

                if iptype == 'ip4':
                    ip4.append(row)
                elif iptype == 'ip6':
                    ip6.append(row)

        # shouldnt be needed since we ignore empty lines
        ip4 = list(filter(None, ip4))
        ip6 = list(filter(None, ip6))

        return (ip4, ip6)

    @staticmethod
    def read_cidr_file(fname: str, verb: bool = False) -> List[str]:
        """
         Read file of cidrs and return list of all IPv4 and IPv6.

         See read_cidrs() which this uses.

        Args:
            fname (str):
            Path to file of cidrs to read.

            verb (bool):
            More verbose output

        Returns:
            List[str]:
            List of all cidrs (ip4 and ip6 combined)
        """
        (ip4, ip6) = CidrFile.read_cidrs(fname, verb)
        return ip4 + ip6

    @staticmethod
    def read_cidr_files(targ_dir: str, file_list: List[str]) -> List[str]:
        """
        Read files in a directory and return merged list of cidr strings.

        Args:
            targ_dir (str):
            Directory to find each file.

            file_list (List[str]):
            List of files in *targ_dir* to read.

        Returns:
            List[str]:
            List of all cidrs found in the files.

        """
        cidrs: List[str] = []
        if not targ_dir or not file_list:
            return cidrs

        for file in file_list:
            path = os.path.join(targ_dir, file)
            this_cidrs = CidrFile.read_cidr_file(path)
            cidrs += this_cidrs

        # compress if possible
        if cidrs:
            cidrs = compact_cidrs(cidrs)
        return cidrs

    @staticmethod
    def write_cidr_file(cidrs: List[str], pname: str) -> bool:
        """
        Write list of cidrs to a file.

        Args:
            cidrs (List[str]):
            List of cidr strings to write.

            pname (str):
            Path to file where cidrs are to be written.

        Returns:
            bool:
            True if successful otherwise False.
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

        Args:
            src_file (str):
            Source file to copy.

            dst_file (str):
            Where to save copy

        Returns:
            bool:
            True if all okay else False
        """
        is_okay = True
        if src_file.endswith('.ip4') or src_file.endswith('.ip6'):
            cidrs = CidrFile.read_cidr_file(src_file)
            if cidrs:
                cidrs = compact_cidrs(cidrs)
                is_okay = CidrFile.write_cidr_file(cidrs, dst_file)
        return is_okay

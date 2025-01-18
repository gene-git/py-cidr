# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Atomic write file
 - caller responsible for any required locking
'''
import os
import random
import string

def open_file(path, mode, encoding=None):
    """
     Open a file and return file object
     Useful where file is opened and used over wider part of code
     than a simple with open() as loop in one spot.
    """
    # pylint: disable=consider-using-with
    try:
        fobj = open(path, mode, encoding=encoding)
        #if encoding:
        #    fobj = open(path, mode, encoding=encoding)
        #else:
        #    fobj = open(path, mode)
    except OSError as err:
        print(f'Error opening file {path} : {err}')
        fobj = None
    return fobj

def write_file_atomic(data:str|bytes, fpath:str) -> (bool, str|None):
    """
    Write data to fpath - atomic version
    Input:
        data : whatever is to be written
        fpath: path to file to write to
    """
    #
    # Create destination directories if needed
    #
    fpath_dir = os.path.dirname(fpath)
    errors = None
    try:
        os.makedirs(fpath_dir, exist_ok=True)
    except OSError as err:
        errors = f'write_file_atomic - failed making dest dirs {fpath_dir} : {err}'
        return (False, errors)

    #
    # Set write mode
    #
    encoding = None
    mode = 'w'
    if isinstance(data, bytes):
        mode = 'wb'
    #
    # write temp file in same dir.
    #
    extension = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    fpath_tmp = f'{fpath}.{extension}'

    try:
        with open_file(fpath_tmp, mode, encoding=encoding) as fob:
            fob.write(data)
            fob.flush()
            os.fsync(fob.fileno())

    except OSError as err:
        errors = f'write_file_atomic: error opening temp file : {err}'
        return (False, errors)

    #
    # rename
    #
    try:
        os.rename(fpath_tmp, fpath)
    except OSError as err:
        errors = f'write_file_atomic - rename error {err}'
        return (False, errors)

    return (True, None)

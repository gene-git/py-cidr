# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>
"""
Locking file 
"""
import os

from lockmgr import LockMgr


def choose_lock_file(cache_dir: str, ipv6: bool, version: str) -> str:
    """
    Args:
        cache_dir (str):
            The driectory where cache lives.

        ipv6 (bool):
            True if ipv6 cache else ipv4

        version (str)
            net_cache version string (e.g. v4)

    Generate lock file to protect cache writes and reads
    lockfile in /tmp but use cache file name to ensure lock applies
    to what its needed for

    NB lockfile must be same across processes so that the lock
    is respected across processes. We prefer to use /tmp
    as this is tmpfs and avoids NFS.

    This means we dont want to use any 'tempdir/tempfile'.

    Preferable to use username.  But when run in chroot there may
    be no user / controlling terminal.

    E.g. When building package in chroot and running tests.
    In this case we use cache_dir.
    """
    if not cache_dir:
        return '-x-'

    user: str = ''
    try:
        euid = os.geteuid()
        user = str(euid)

    except OSError:         # should never happen
        user = '-x-'

    ipt: str = 'ipv6' if ipv6 else 'ipv4'

    # use /tmp for lock not cache_dir its faster and avoids nfs etc.
    lockdir = f'/tmp/py-cidr-{user}'
    cache_base: str = os.path.basename(cache_dir)
    lockfile = f'{ipt}.{cache_base}.{version}.lock'

    os.makedirs(lockdir, exist_ok=True)
    path = os.path.join(lockdir, lockfile)
    return path

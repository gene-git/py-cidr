.. SPDX-License-Identifier: MIT

#######
py-cidr
#######

Overview
========

py-cidr : python module providing network / CIDR tools

Key features
============

* Built on python's native ipaddress module
* 3 Classes : Cidr, CidrMap, CidrFile
* Cidr provides for many common operations for example:

  - Support for IPv4 and IPv6
  - compact lists of CIDRs to smallest set of CIDR blocks
  - convert an IP range to a list of CIDRs
  - Identify and validate
  - many more

* CidrFile offers common operations on files with lists of cidrs.
  
  - Includes atomic file writes

* CidrMap provides a class that maps CIDRs to values.

  - File cache employs locking to ensure multiple processes handle cache correctly.

See API reference documentation for more details.

New / Interesting
==================

* Add RFC 1918 convenience tools:

  Cidr.is_rfc_1918()
  Cidr.rfc_1918_nets()
  Cidr.rfc_1918_cidrs()
  Cidr.remove_rfc_1918()

* Code reorg; break into smaller chunks in separate files.

###############
Getting Started
###############


py-cidr module 
==============

module functions
----------------

The library provides the following tools:

**CidrMap Class**

CidrMap provides a reasonably optimized tool to cache (cidr, value) pairs.
i.e. it maps a CIDR address to some value (string).
These are cached to file if a cache directory is provided when instantiating the class.

.. code::python

   cidr_cache = CidrMap(cache_dir='/home/bob/.cache/appname')

Ths will create an IPv4 and an IPv6 cache file in the given directory. The code is careful
about reading and writing the cache files and uses locking as well as atomic writes.
For example if application starts, reads cache, updates with new items and some time later
saves the cache - the module will detect if the cache changed (by another process using same cache
directory) since it was read in, and merge its own changes with the changes in the cache file 
before writing out the updated cache.  So nothing should be lost.

This was built this originally for our firewall tool, where part of the data gathering component creates 
maps of CIDR blocks to geolocated country codes for all CIDRs as listed by each of registries. 
This process can take several minutes. Run time was cut roughly in half using 
CidrMap() to provide a mapping of CIDR to location.

Since parallelizing can provide siginificant speedups, the CidrMap::add_cidr() method has
a mechanism to allow that by avoiding multiple threads/processes updating the in memory data
at the same time. It offers the ability for each thread/subprocess to add cidr blocks to thread local 
data. After all the threads/processes complete, then the private data maps of each of the processes 
can be merged together using CidrMap::merge() method.

Additional details are available in the API reference documentation.

Methods provided:

* CidrMap.lookup 
* CidrMap.add_cidr 
* CidrMap.merge 

Static functions:

* create_private_cache


**Cidr Class**

See the API reference in the documentation for details.
This class provides a suite of tools we found ourselves using often, so we encapsulated them in this class.
All methods in the class are *@staticmethod* and thus no instance of the class is needed. Just use
them as functions (*Cidr.xxx()*)

* Cidr.is_valid_ip4
* Cidr.is_valid_ip6
* Cidr.is_valid_cidr
* Cidr.cidr_iptype
* Cidr.cidr_type_network

* Cidr.cidr_to_net
* Cidr.cidrs_to_nets
* Cidr.nets_to_cidrs
* Cidr.compact_cidrs
* Cidr.ip_to_address
* Cidr.ips_to_addresses
* Cidr.addresses_to_ips
* Cidr.cidr_set_prefix
* Cidr.ipaddr_cidr_from_string
* Cidr.cidr_is_subnet
* Cidr.address_iptype
* Cidr.compact_nets
* Cidr.net_exclude
* Cidr.nets_exclude
* Cidr.cidrs_exclude
* Cidr.cidrs2_minus_cidrs1
* Cidr.cidr_exclude
* Cidr.sort_cidrs
* Cidr.sort_ips
* Cidr.get_host_bits
* Cidr.clean_cidr
* Cidr.clean_cidrs
* Cidr.range_to_cidrs
* Cidr.cidr_to_range
* Cidr.fix_cidr_host_bits
* Cidr.fix_cidrs_host_bits

**CidrFile Class**

This class provides a few reader/writer tools for files with lists of CIDR strings.
Readers ignores comments. All methods are *@staticmethod* and thus no instance of the
class is required.  Simply use them as functions (*Cidr.xxx()*)

* Cidr.read_cidr_file(file:str, verb:bool=False) -> [str]:
* Cidr.read_cidr_files(targ_dir:str, file_list:[str]) -> [str]
* Cidr.write_cidr_file(cidrs:[str], pathname:str) -> bool
* Cidr.read_cidrs(fname:str|None, verb:bool=False) -> (ipv4:[str], ipv6:[str]):
* Cidr.copy_cidr_file(src_file:str, dst_file:str) -> None


########
Appendix
########

Installation
============

Available on
* `Github`_
* `Archlinux AUR`_

On Arch you can build using the provided PKGBUILD in the packaging directory or from the AUR.
To build manually, clone the repo and :

 .. code-block:: bash

        rm -f dist/*
        /usr/bin/python -m build --wheel --no-isolation
        root_dest="/"
        ./scripts/do-install $root_dest

When running as non-root then set root_dest a user writable directory

Dependencies
============

**Run Time** :

* python          (3.13 or later)
* lockmgr

**Building Package** :

* git
* hatch           (aka python-hatch)
* wheel           (aka python-wheel)
* build           (aka python-build)
* installer       (aka python-installer)
* rsync

**Optional for building docs** :

* sphinx
* python-myst-parser
* python-sphinx-autoapi
* texlive-latexextra  (archlinux packaguing of texlive tools)

Building docs is not really needed since pre-built docs are provided in the git repo.

Philosophy
==========

We follow the *live at head commit* philosophy. This means we recommend using the
latest commit on git master branch. We also provide git tags. 

This approach is also taken by Google [1]_ [2]_.

License
=======

Created by Gene C. and licensed under the terms of the MIT license.

* SPDX-License-Identifier: MIT
* SPDX-FileCopyrightText: © 2024-present  Gene C <arch@sapience.com>

.. _Github: https://github.com/gene-git/py-cidr
.. _Archlinux AUR: https://aur.archlinux.org/packages/py-cidr

.. [1] https://github.com/google/googletest  
.. [2] https://abseil.io/about/philosophy#upgrade-support



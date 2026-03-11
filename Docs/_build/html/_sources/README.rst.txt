.. SPDX-License-Identifier: GPL-2.0-or-later

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

**3.13.0**

* Lots of pretty big code re-org and changes.
* Biggest change is in CidrMap: 
  - New methods:
  - Significant Changes to CidrMap.
    The API has changed somewhat. As usual we have kept backward compatibility for the previous API.
  - New dependency on python-pytricia which provides a python module of a C-code version of patricia trie. 
    I have made this package available in the AUR `Archlinux AUR PyTricia`_ as it is not available in standard
    Arch repos.
  - lookup_lmp() replaces lookup() and returns a tuple(prefix, value) where prefix is 
    the longest matching prefix
  - lookup_all() returns list of all (preifx, value) tuples, where the first item in the list
    is the LMP.
  - add_prefix_val() takes a tuple[prefix, val] and replaces add_cidr(prefix, val).
  - add_prefix_vals() takes a list of (prefix, val) tuples and replaces the add_cidrs()
    which takes list of prefixes and a list of values.
  - New CIDR map argument type compact: CidrMap(compact=False). Note this defaults to
    False. When no compacting is done, then every (prefix, val) is kept.
    
    When set to True, then the map is kept as compact as possible when adding new (prefix, val)
    pairs. 
    For example, take a compact map that has ('10.0.0.0/22', 'net-A'). If one tries to add
    (('10.0.0.0/24', 'net-A') it will be ignored since the existing map covers it.
    A non-compact map would add the new item.

    If one tries instead to add ((('10.0.0.0/24', 'xxx'), then it is added for compact as well,
    since the *value* is different, even though the prefix is a subnet of existing item.

    Compacting must also check if any children of a newly added prefix are still needed.

* NB There is no conversion of older map cache files to new format. For now you will need
    to recreate new cidr_map and cidr_map.save_cache().
    TODO: make standalone cache converter.

**3.12.0**

* CidrMap : New .items() method provides an Iterator over the map.

  Each iteration yields a tuple[cidr: str, value: Any]

* Add net_range_split/cidr_range_split: 

  split one net/cidr into (first, mid,  last) ip addresses


**3.11.0**

* Code Reorg
* Switch packaging from hatch to uv
* Testing to confirm all working on python 3.14.2
* License GPL-2.0-or-later


**Older**

* Rename *py-cidr-cache-print* (without the .py extension)
* PEP-8, PEP-257 and PEP-484 style changes
* PEP 561 type hints (improves module use for type checkers e.g. *mypy*)
* CidrMap now uses separate CidrCache for "private cache data" instead of just the "data" part.
  CidrCache class no longer needs it's own "private data" functionality.
* Add some tests (via pytest)
* Reorganize CidrMap and simplify/improve way we do private_cache supporing
  multiprocess/multithreading usecase. This is now all done in CidrMap.
* Change cache file storage to pickle format as its more flexible than json
  Provide simple app to show contents of cache:

.. code::

   py-cidr-cache-print <cache_directory>

Documentation:
==============

We include pre-built versions of both html and PDF documentation, including the
API reference.

The PDF file is *Docs/py-cidr.pdf* and after the package is installed it will be available:

    `PDF Documentation </usr/share/py-cidr/Docs/py-cidr.pdf>`_.

and a browser can be used to view:

    `HTML Documentation <file:///usr/share/py-cidr/Docs/_build/html/index.html>`_.

###############
Getting Started
###############

All git tags are signed with arch@sapience.com key which is available via WKD
or download from https://www.sapience.com/tech. Add the key to your package builder gpg keyring.
The key is included in the Arch package and the source= line with *?signed* at the end can be used
to verify the git tag.  You can also manually verify the signature


py-cidr module 
==============

module functions
----------------

The library provides the following tools:

**CidrMap Class**

CidrMap provides an optimized tool to map(network-prefix) to a value.
The map may be saved to file and reused.

To make use of file cache, a *cache_directory* must be provided when instantiating the class.
Note that there are 2 typed of maps, non-compact and compact. The default is non-compact.
With this every (prefix, value) is added to the map.

For a compact map, effort is made to reduce redundant entries. For example if the map
contains the (prefix, tuple) = ('10.0.0.0/22', 'net-1') and then a new tuple
('10.0.0.0/24', 'net-1') is added to the map, the new one is considered redundent
since the network is a subnet of *'10.0.0.0/22'* and the value, *'net-1*' is the same.
If the value was different, then it is not considered redundent.

For non-compact maps, every (prefix, value) is added.

A *CidrMap* contains 2 separate maps. A *PrefixMap*  for IPv4 and one for IPv6.

.. code::python

   cidr_cache = CidrMap(cache_dir='/home/bob/.cache/appname', compact=False)

Ths will create both an IPv4 and an IPv6 cache file in the given directory. The code is careful
about reading and writing the cache files and uses locking and atomic writes to ensure the 
integrity of the data.

For example if application starts, reads cache, updates with new items and some time later
saves the cache - the module will detect if the cache changed (by another process using same cache
directory) since it was last read in, and merge its own changes with the changes in the cache file 
before writing out the updated cache.  This should ensure nothing gets lost.

This was built this originally for our firewall tool, where part of the data gathering component creates 
maps of network prefixes (blocks of IP addresses) to geolocated country codes and other useful
information such as the ASN(s) the prefix belongs to.

When looking up a CIDR, there are 2 methods available. The first, *lookup_lmp()* returns
the (lmp_prefix, val) pair where *lmp_prefix* is the network with the longest matching 
cidr prefix. The longer the cidr prefix, the more specific the network. A */24* os more 
specific than a */22* for example.

The method *lookup_all()* returns every matching prefix and its associated value. the 
LMP is always the first element in returned in the list.

Since parallelizing often provides decent speedups, *CidrMap* provides a mechanism to do that.
It allows each separate process or thread to work with private (thread local) cache. Each of the
private data caches can then be merged together by the top level process or thread.

This avoids multiple threads/processes writing to the same in memory data
at the same time.  This is done using the *CidrMap::merge()* method.

Additional details are available in the API reference documentation.

Methods provided:

* CidrMap.add_prefix_val() 
* CidrMap.add_prefix_vals() 
* CidrMap.lookup_lmp() 
* CidrMap.lookup_all() 
* CidrMap.items() 
* CidrMap.save_cache() 
* CidrMap.merge() 

Static functions:
* CidrMap.create_private_cache() 


**Cidr Class**

See the API reference in the documentation for details.
This class provides a suite of tools we found ourselves using often, so we encapsulated them in this class.
All methods in the class are *@staticmethod* and thus no instance of the class is needed. Just call
them as you would any function (*Cidr.xxx()*).

IP addresses and networks can be represented as strings or the format used by python's
native *ip_address* module. Most functionality is available on both.

Here is a sample of some of the available functionality, see the API doc for complete documentation.

* Cidr.is_valid_ip4()
* Cidr.is_valid_ip6()
* Cidr.is_valid_cidr()
* Cidr.ip_version()
* Cidr.cidr_iptype()

* Cidr.cidr_to_net
* Cidr.cidrs_to_nets
* Cidr.net_to_cidr
* Cidr.nets_to_cidrs
* Cidr.ip_to_address
* Cidr.ips_to_addresses
* Cidr.address_to_ip
* Cidr.addresses_to_ips

* Cidr.cidr_set_prefix
* Cidr.cidr_is_subnet
* Cidr.compact_cidrs
* Cidr.compact_nets
* Cidr.cidrs2_minus_cidrs1
* Cidr.sort_cidrs
* Cidr.get_host_bits
* Cidr.clean_cidr
* Cidr.fix_cidr_host_bits

* Cidr.range_to_cidrs
* Cidr.cidr_range_split

* Cidr.rfc_1918_cidrs
* Cidr.is_rfc_1918

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

We follow the *live at head commit* philosophy as recommended by
Google's Abseil team [1]_.  This means we recommend using the
latest commit on git master branch. 


License
=======

Created by Gene C. and licensed under the terms of the GPL-2.0-or-later license.

* SPDX-License-Identifier: GPL-2.0-or-later
* SPDX-FileCopyrightText: © 2024-present Gene C <arch@sapience.com>

.. _Github: https://github.com/gene-git/py-cidr
.. _Archlinux AUR: https://aur.archlinux.org/packages/py-cidr
.. _Archlinux AUR PyTricia: https://aur.archlinux.org/packages/python-pytricia

.. [1] https://abseil.io/about/philosophy#upgrade-support



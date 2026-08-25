.. SPDX-License-Identifier: GPL-2.0-or-later

=======
py-cidr
=======

Overview
========

py-cidr is a python module with a variety of networking / CIDR tools. 

Key features
============

* PyCidr (As of version 5.0) is now the preferred class. 

  Very fast version that uses compiled C-code to do most of the work.

  Using compiled C-code is simple, cleane, robust, very maintainable, 
  is compiled with modern, restritive compiler and linker flags. 

  All CIDR and IP addresses are strings.

  Depends on two new packages:

  * cidrtools-cffi: `github <https://github.com/gene-git/cidrtools-cffi>`_ and 
    `AUR <https://aur.archlinux.org/packages/cidrtools-cffi>`_.

  * cidrtools: `github <https://github.com/gene-git/cidrtools>`_ and 
    `AUR  <https://aur.archlinux.org/packages/cidrtools>`_.

  *cidrtools-cffi* has python bindinds to the *cidrtools* compiled library.

* Cidr class is still upported. 
  
  It uses Python's own *ipaddress* module. 

  We decided to leave the Cidr class untouched. The primary reason is that 
  this makes it straghtforward to compare with PyCidr.

  So, at least for now, the performance boost requires migrating from Cidr to PyCidr.
  At some point, we may update the Cidr class to take advantage of the 
  very fast *cidrtools* library as well.

* *py_cidr* has four Classes : PyCidr, Cidr, CidrMap, CidrFile

  - PyCidr does everything Cidr class does just a lot faster.

    It is built on top of the compiled library *libcidrtools.so*. The API has changed 
    a little from the *Cidr* class and is, hopefully, a little simpler and cleaner. 
    One of the benefits (and drawbacks) of starting fresh.

  - PyCidr and Cidr offer a number of useful operations on IP addresses and network blocks.

    - Support for both IPv4 and IPv6
    - Compact a list of CIDRs to smallest set of CIDR blocks
    - Convert an range of IP addresses to a list of CIDRs
    - Exclude one list of cidr blocks from another list.
    - Split a CIDR block in a list of *smaller* CIDRs blocks with a larger prefix.
    - Identify and validate
    - more

* CidrFile reads and writes text files with lists of cidrs.
  
  - skips shell style comments when reading
  - Uses atomic file writes

* CidrMap is a way to map cidr strings to values.

  For example mapping IP prefixes (cidr blocks) to their ``ISO`` country codes.

  - File writes use locking to ensure multiple processes handle cached files correctly.

  - Built on Patricia trees using the  `patricia26 <https://github.com/gene-git/patricia26>`_ module.
    particia26 is extremely fast. 

See API reference documentation for details.

Manual
======

There are pre-built versions of of the manual which comes as a PDF file as well
as an HTML version. The manual includes the API reference guide for all classes.

The docs are in *src/data/docs* and the Arch PKGUILD installs them to
*/usr/share/py-cidr/docs*.

Getting Started
===============

All git tags are signed with arch@sapience.com key which is available via WKD
or download from https://www.sapience.com/tech. Add the key to your package builder gpg keyring.
The key is included in the Arch package and the source= line with *?signed* at the end can be used
to verify the git tag.  You can also manually verify the signature

More Detail 
===========

The following are part of the module.

**CidrMap Class**

CidrMap provides an optimized tool to map a network-prefix to a value.
The map may be saved to a (cache) file and reused.

To make use of the file cache, provide a *cache_directory* when instantiating the class.

Note that there are 2 typed of maps, non-compact and compact. The default and by
far the most common is non-compact.
Here, every (prefix, value) is added to the map.

If the data is available as a list of (prefix, value) tuples, then
the best and fastest way is using very fast *bulk_insert* to get the data into the
Patricia tree. 

Bulk inserting is 2 - 3 times faster than inserting the data in a loop one at a time.
For large maps it is hugely benficial to use bulk_intert().

For a compact map, effort is made to reduce redundant entries. For example if the map
contains the (prefix, tuple) = ('10.0.0.0/22', 'net-1') and then a new tuple
('10.0.0.0/24', 'net-1') is added to the map, the new one is considered redundent
since the network is a subnet of *'10.0.0.0/22'* and the value, *'net-1*' is the same.
If the value was different, then it is deemed not compactable.
Note that bulk_insert() is not available with *compact* maps. 

A *CidrMap* contains 2 separate maps one for each network family;
one tree for IPv4 and separate one for IPv6. 

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


**PyCidr Class**

See the API reference in the documentation for details.
This class provides a suite of tools we found ourselves using often, so we encapsulated them in this class.
All methods in the class are *@staticmethod* and thus no instance of the class is needed. Just call
them as you would any function (*PyCidr.xxx()*).

IP addresses and networks are always represented as strings.

Here is a sample of some of the available functionality, see the API doc for complete documentation.

* PyCidr.compact()
* PyCidr.cidr_parts()
* PyCidr.exclude_cidrs()
* PyCidr.is_subnet()
* PyCidr.set_prefix()
* PyCidr.sort()
* PyCidr.get_host_bits(), format_host_bits()
* PyCidr.cidr_to_range(), range_to_cidrs()
* PyCidr.fix_host_bits()
* PyCidr.clean_cidr(), clean_cidrs()
* PyCidr.split_by_iptype()
* PyCidr.num_ips()
* PyCidr.ip_version()
* PyCidr.is_valid_ipv4(), is_valid_ipv6, is_valid_cidr()
* PyCidr.subnets_split()

**CidrFile Class**

This class provides a few reader/writer tools for files with lists of CIDR strings.
Readers ignores comments. All methods are *@staticmethod* and thus no instance of the
class is required.  Simply use them as functions (*Cidr.xxx()*)

* Cidr.read_cidr_file(file:str, verb:bool=False) -> [str]:
* Cidr.read_cidr_files(targ_dir:str, file_list:[str]) -> [str]
* Cidr.write_cidr_file(cidrs:[str], pathname:str) -> bool
* Cidr.read_cidrs(fname:str|None, verb:bool=False) -> (ipv4:[str], ipv6:[str]):
* Cidr.copy_cidr_file(src_file:str, dst_file:str) -> None


**Cidr Class**

Quite similar to PyCidr but not identical.
See the API Reference Guide for more details.


.. _Github: https://github.com/gene-git/py-cidr
.. _Archlinux AUR: https://aur.archlinux.org/packages/py-cidr



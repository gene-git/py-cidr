
PyCidr: Overview
================

Before getting into detail, this is a brief summary of the member functions available.
All member functions are *static* and therefore the member functions are called directly 
using PyCidr.xxx() - no need to instantiate the class.


* compact()

  Takes a list of cidrs and returns a new list with the smallest number of cidrs
  that span exactly the space as the original list.

* cidr_parts()

  Separates a cidr into the IP part and its prefix. 

  Example::

    cidr_parts("10.0.0.0/24")     -> ("10.0.0.0", 24)
    cidr_parts("10.0.0.27/32")    -> ("10.0.0.27", 32)
    cidr_parts("2001:db8::1/64")  -> ("2001:db8::", 64)


* exclude_cidrs()

  Exclude one list of cidrs from another.

.. code-block:: python

  smaller = PyCidr.exclude_cidrs(all_cidrs, excluded_cidrs)

* is_subnet()

  Determine if a cidr block is a subnet of any of a list of networks.

.. code-block:: python

  all_cidrs = ['10.0.0.0/24', ... ]
  is_subnet = PyCidr.is_subnet('10.0.0.22/32', all_cidrs)

* set_prefix()

  Change the prefix (or add a prefix to an IP address).

.. code-block:: python

   cidr = '10.0.0.0/24'
   new_cdr = PyCidr.set_prefix(cidr, 22)

* sort()

  Sorts a list of network blocks.

.. code-block:: python

  sorted_items = PyCidr.sort(all_cidrs)

* get_host_bits(), format_host_bits()

  Extracts the host bits of an IPv4 or IPv6 CIDR string and returns either an 
  integer or human readable string from format_host_bits.

.. code-block:: python

   hbit_str = PyCidr.format_host_bits("10.0.0.22/24)")  # -> "0.0.0.22"

* cidr_to_range(), range_to_cidrs()

  cidr_to_range returns the first, last and middle ip address of a cidr, while
  range_to_cidrs() generates the list of network cidrs that span a range of IPs
  from first to last.

* fix_host_bits()

  Sometimes a cidr has host bits set, this 0's them out.
  For example "10.0.0.22/24" would return "10.0.0.0/24"

* clean_cidr(), clean_cidrs()

  Clean one cidr or a list of cidrs. A clean cidr is one that has 0 for host bits
  For example:
    
    10.1.2.3/24 -> 10.1.2.0/24

* split_by_iptype()

  Takes a list of cidrs, can be mixed IPv4 and IPv4 and separates the 
  IPv4 from the IPv6 blocks. It returns a tuple of [ipv4_cidrs, ipv6_cidrs]

* num_ips()

  Returns the number of IPs in a cidr block.

* ip_version()

  If cidr is IPV4 then this returns the integer *4*. If an IPv6 then retutns *6*.

* is_valid_ipv4(), is_valid_ipv6, is_valid_cidr()

  They each return True or False as appropriate.

* subnets_split()

  Splits an IPv4 or IPv6 CIDR block into smaller subnets of a larger prefix size.

  Examples::

    subnets_split("10.0.0.0/23", 24)    -> ["10.0.0.0/24", ""10.0.1.0/24")


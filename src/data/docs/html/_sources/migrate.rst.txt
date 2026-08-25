Migrating from Cidr to PyCidr
=============================

If existing code uses string representations, it is straightfoward.
If using ipaddress format, then code will need to be migrated to strings 
to get the performance benefits. Cidr class is not going away, so migrating
is optional. 

Note that for any functions with an argument to choose the output in string or ipaddress format
the PyCidr replacement has no such argument because strings are always the output form.

Some examples migrating:

* Compact list of cidrs.


.. code-block:: text

    Cidr.compact(cids)

    PyCidr.compact(cidrs)

    Cidr has some additional forms all of which are replaced as above


* Cidr to IP address range

.. code-block:: text

   (ip_start, ip_end) = Cidr.cidr_to_range(cidr)
   (ip_start, ip_mid, ip_end) = Cidr.cidr_range_split(cidr)

   (ip_start, ip_mid, ip_end) = PyCidr.cidr_to_range(cidr)

* Sorting

  While Cidr distinguished IP addresses from CIDR blocks and therefore provided separate
  functions for some tasks like sorting, PyCidr accepts an IP address (e.g. *10.0.0.22*) 
  or a CIDR (e.g. *10.0.0.0/24* or *10.0.0.22/32*) everywhere. 

.. code-block:: text

    x = Cidr.sort_cidrs(cidrs)
    x = Cidr.sort_ips(ips) 

    x = PyCidr.sort(cidrs)
    x = PyCidr.sort(ips)

However please note that PyCidr returns IP addresses with their prefix (/32 for IPv4 and
/128 for IPv6). To recover just the IP part using cidr_parts()

.. code-block:: text

   (ip_part, pfx_part) = PyCidr.cidr_parts(cidr)


* Checking ip/cidr validity 

.. code-block:: text

  Cidr.is_valid_ip4()
  Cidr.is_valid_ip6()
  Cidr.is_valid_cidr()

  PyCidr.is_valid_ipv4()
  PyCidr.is_valid_ipv6()
  PyCidr.is_valid_cidr()



py_cidr
=======

.. py:module:: py_cidr

.. autoapi-nested-parse::

   Public Methods
   py_cidr 



Classes
-------

.. autoapisummary::

   py_cidr.Cidr
   py_cidr.CidrMap
   py_cidr.CidrCache
   py_cidr.CidrFile


Package Contents
----------------

.. py:class:: Cidr

   Class provides common CIDR tools
   All mathods are (static) and are thus called withoue instantiating
   the class. for example :

       net = Cidr.cidr_to_net(cidr_string)

   Notation:
       * cidr means a string
       * net means ipaddress network (IPv4Network or IPv6Network)
       * ip means an IP address string
       * addr means an ip address (IPv4Address or IPv6Address)
       * address means either a IP address or a cidr network as a string


   .. py:method:: cidr_to_net(cidr: str, strict: bool = False) -> IPvxNetwork | None
      :staticmethod:


      Cidr to Net
          Convert cidr string to ipaddress network.

      :param cidr:
          Input cidr string

      :param strict:
          If true then cidr is considered invalid if host bits are set.
          Defaults to False. (see ipaddress docs).

      :returns:
          The ipaddress network derived from cidr string as either IPvxNetwork = IPv4Network or IPv6Network.



   .. py:method:: cidrs_to_nets(cidrs: [str], strict: bool = False) -> [IPvxNetwork]
      :staticmethod:


      Cidrs to Nets
          Convert list of cidr strings to list of IPvxNetwork

      :param cidrs:
          List of cidr strings

      :param strict:
          If true, then any cidr with host bits is invalid. Defaults to false.

      :returns:
          List of IPvxNetworks.



   .. py:method:: nets_to_cidrs(nets: [IPvxNetwork]) -> [str]
      :staticmethod:


      Nets to Strings
          Convert list of ipaddress networks to list of cidr strings.

      :param nets:
          List of nets to convert

      :returns:
          List of cidr strings



   .. py:method:: ip_to_address(ip: str) -> IPvxAddress | None
      :staticmethod:


      IP to Address
          Return ipaddress of given ip.
          If IP has prefix or host bits set, we strip the prefix first and keep host bits

      :param ip:
          The IP string to convert

      :returns:
          IPvxAddress derived from IP or None if not an IP address



   .. py:method:: ips_to_addresses(ips: [str]) -> [IPvxAddress]
      :staticmethod:


      IPs to Addresses
          Convert list of IP strings to a list of ip addresses

      :param ips:
          List of IP strings to convert

      :returns:
          List of IPvxAddress derived from input IPs.



   .. py:method:: addresses_to_ips(addresses: [IPvxAddress]) -> [str]
      :staticmethod:


      Address to IP strings
          For list of IPs in ipaddress format, return list of ip strings

      :param addresses:
          List of IP addresses in ipaddress format

      :returns:
          List of IP strings



   .. py:method:: cidr_set_prefix(cidr: str, prefix: int) -> str
      :staticmethod:


      Set Prefix
          Set new prefix for cidr and return new cidr string

      :param cidr:
          Cidr string to use

      :param prefix:
          The new prefix to use

      :returns:
          Cidr string using the specified prefix



   .. py:method:: ipaddr_cidr_from_string(addr: str, strict: bool = False) -> ipaddress.IPv4Network | ipaddress.IPv6Network | None
      :staticmethod:


      IP/CIDR to IPvxNetwork
          Convert string of IP address or cidr net to IPvxNetwork

      :param address:
          String of IP or CIDR network.

      :param strict:
          If true, host bits disallowed for cidr block.

      :returns:
          An IPvXNetwork or None if not valid.



   .. py:method:: cidr_is_subnet(cidr: str, ipa_nets: [ipaddress.IPv4Network | ipaddress.IPv6Network]) -> bool
      :staticmethod:


      Is Subnet:
          Check if cidr is a subnet of any of the list of IPvxNetworks .

      :param cidr:
          Cidr string to check.

      :param ipa_nets:
          List of IPvxNetworks to check in.

      :returns:
          True if cidr is subnet of any of the ipa_nets, else False.



   .. py:method:: address_iptype(addr: IPvxAddress | IPvxNetwork) -> str | None
      :staticmethod:


      Address Type
          Identify if IP address (IPvxAddres) or net (IPvxNetwork) is ipv4 or ipv6

      :param addr:
          IP address or cidr network .

      :returns:
          'ip4', 'ip6' or None



   .. py:method:: cidr_list_compact(cidrs_in: [str], string=True) -> [str | IPvxNetwork]
      :staticmethod:


      Cidr Compact:
          Compact list of cidr networks to smallest list possible.

      :param cidrs_in:
          List of cidr strings to compact.

      :param string:
          If true (default) returns list of strings, else a list of IPvxNetworks

      :returns:
          Compressed list of cidrs as ipaddress networks (string=False)
          or list of strings when string=True



   .. py:method:: compact_cidrs(cidrs: [str], nets=False) -> [str | IPvxNetwork]
      :staticmethod:


      combine em 



   .. py:method:: compact_nets(nets: [IPvxNetwork]) -> [IPvxNetwork]
      :staticmethod:


      combine em 



   .. py:method:: net_exclude(net1: IPvxNetwork, nets2: [IPvxNetwork]) -> [IPvxNetwork]
      :staticmethod:


      Exclude net1 from any of networks in net2
      return resulting list of nets (without net1)



   .. py:method:: nets_exclude(nets1: [IPvxNetwork], nets2: [IPvxNetwork]) -> [IPvxNetwork]
      :staticmethod:


      Exclude every nets1 network from from any networks in nets2



   .. py:method:: cidrs_exclude(cidrs1: [str], cidrs2: [str]) -> [str]
      :staticmethod:


      old name 



   .. py:method:: cidrs2_minus_cidrs1(cidrs1: [str], cidrs2: [str]) -> [str]
      :staticmethod:


      Exclude all of cidrs1 from cidrs2
      i.e. return cidrs2 - cidrs1



   .. py:method:: cidr_exclude(cidr1: str, cidrs2: [str]) -> [str]
      :staticmethod:


      Exclude cidr1 from any of networks in cidrs2
      return resulting list of cidrs (without cidr1)



   .. py:method:: sort_cidrs(cidrs: [str]) -> [str]
      :staticmethod:


      Sort the list of cidr strings



   .. py:method:: sort_ips(ips: [str]) -> [str]
      :staticmethod:


      Sort the list of cidr strings



   .. py:method:: get_host_bits(ip: str, pfx: int = 24)
      :staticmethod:


      Gets the host bits from an IP address given the netmask



   .. py:method:: clean_cidr(cidr: str) -> str
      :staticmethod:


      returns None if not valid
       - we to fix class C : a.b.c -> a.b.c.0/24



   .. py:method:: clean_cidrs(cidrs: [str]) -> [str]
      :staticmethod:


      clean cidr array 



   .. py:method:: fix_cidr_host_bits(cidr: str, verb: bool = False)
      :staticmethod:


      zero any host bits 



   .. py:method:: fix_cidrs_host_bits(cidrs: [str], verb: bool = False)
      :staticmethod:


      zero any host bits 



   .. py:method:: is_valid_ip4(address) -> bool
      :staticmethod:


      check if valid address or cidr 



   .. py:method:: is_valid_ip6(address) -> bool
      :staticmethod:


      check if valid address or cidr 



   .. py:method:: is_valid_cidr(address) -> bool
      :staticmethod:


      Valid Address or Network
          check if valid ip address or cidr network

      :param address:
          IP or Cidr string to check. Host bits being set is permitted for a cidr network.

      :returns:
          True/False if address is valid



   .. py:method:: cidr_iptype(address: str) -> str | None
      :staticmethod:


      Determines if an IP address or CIDR string is ipv4 or ipv6

      :param address:
          ip address or cidr string

       :returns:
          'ip4' or 'ip6' or None



   .. py:method:: cidr_type_network(cidr: str) -> (str, IPvxNetwork)
      :staticmethod:


      Cidr Network Type:

      :param cidr:
          Cidr string to examine

      :returns:
          Tuple(ip-type, net-type). ip-type is a string  ('ip4', 'ip6') while
          network type is IPv4Network or IPv6Network



   .. py:method:: range_to_cidrs(addr_start: IPAddress, addr_end: IPAddress, string=False) -> [IPvxNetwork | str]
      :staticmethod:


      Generate a list of cidr/nets from an IP range.

      :param addr_start:
          Start of IP range as IPAddress (IPv4Address,  IPv6Address or string)

      :param addr_end:
          End of IP range as IPAddress (IPv4Address,  IPv6Address or string)

      :param string:
          If True then returns list of cidr strings otherwise IPvxNetwork

      :returns:
          List of cidr network blocks representing the IP range. 
          List elements are IPvxAddress or str if parameter string=True



   .. py:method:: net_to_range(net: IPvxNetwork, string: bool = False) -> (IPAddress, IPAddress)
      :staticmethod:


      Network to IP Range

      :param net:
          The ipaddress network (IPvxNetwork) to examine

      :param string:
          If True then returns cidr strings instead of IPvxAddress

      :returns:
          Tuple (ip0, ip1) of first and last IP address in net
          (ip0, ip1) are IPvxAddress or str when string is True



   .. py:method:: cidr_to_range(cidr: str, string: bool = False) -> (IPAddress, IPAddress)
      :staticmethod:


      Cidr string to an IP Range

      :param cidr:
          The cidr string to examine

      :param string:
          If True then returns cidr strings instead of IPvxAddress

      :returns:
          Tuple (ip0, ip1) of first and last IP address in net
          (ip0, ip1) are IPvxAddress or str when string is True



.. py:class:: CidrMap(cache_dir: str = None)

   Class provides map(cidr) -> value
    - keeps separate ipv4 and ipv6 cache
    - built on CidrCache and Cidr classes

   :param cache_dir:
       Optional directory to save cache file


   .. py:method:: get_ipt(cidr) -> str | None

      Identify cidr as "ipv4" or "ipv6"
      :param cidr:

          Input cidr string

      :returns:
          'ipv4' of 'ipv6' based on cidr



   .. py:method:: save_cache()

      save cache files 



   .. py:method:: lookup(cidr: str) -> Any | None

      Check if cidr is in cache

      :param cidr:

          Cidr value to lookup.

      :returns:

          Result if found else None



   .. py:method:: create_private_cache() -> dict
      :staticmethod:


      Return private cache object to use with add_cidr()
      Needed if one CidrMap instance is used across multiple processes/threads
      Give each process/thread a private data cache and they can be merged
      back into the CidrMap instance after they have all completed.



   .. py:method:: add_cidr(cidr: str, result: str, priv_data: dict = None)

      Add cidr to cache

      :param cidr:
          Add this cidr string and its associated result value to the map.

      :param priv_data:

          If using multiple processes/threads provide this priv_data.
          so that changes are kept in private_data cache instead of instance cache.
          That way instance cache can be used across multiple processes/threads.
          Use CidrMap.create_private_cache() to create private_data




   .. py:method:: merge(priv_data: dict)

      Merge private cache into our cache

      :param priv_data:

          If used private date to add (cidr, result) to the map, then 
          this merges content of priv_data into the current data.



   .. py:method:: print()

      Print the cache data



.. py:class:: CidrCache(ipt, cache_dir=None)

   Class provides a cache which maps cidrs to values.
   Implemented as an ordered list of networks where each net has some assocated value
   Each elem in list is a pair of (cidr_net, value)

   data List *must* be kept sorted and compressed (no elem can be subnet of any other element)
   for search to work and work efficiently.

   We use ipaddress network as key instead of a string to for performance reasons.
   This minimizes any mapping between network and string representations.


   .. py:method:: load_cache()

      Read cache from file



   .. py:method:: write()

      Save to cache file



   .. py:method:: sort()

      sort the data by network



   .. py:method:: lookup_cidr(cidr: str) -> str | None

      Look up the value associated with cidr string 

      :param cidr:
          Cidr string to lookup

      :returns:
          Value associated with the cidr string or None if not found



   .. py:method:: lookup(net) -> [ipaddress.IPv4Network | ipaddress.IPv6Network, str]

      Lookup value for net
          If net isin cache then returns pair [cache_net, value].
          net is a cache_net or a subnet it.
          If not found [None, None] is returned.

      :param net:
          The network to lookup 

      :returns:
          List of (cahe_network, value) where net is cache_network or subnet of it.
          If net is not found then [None, None]



   .. py:method:: find_nearest(net, priv_data=None) -> (int, bool)

      Find Nearest (internal)
          find the index of the element (foundnet, value) 
          where net is a subnet of foundnet
          or the index of the element after which net would be inserted
          elem[i] <= net < elem[i+1]
          when net = elem[i] (i.e. net is subnet of elem[i]) then ismatch is True

      :returns:
          Tuple of (Index, ismatch). Index refers to cache list. Is match is True when
          net is a subnet of the cache element at index.



   .. py:method:: add_cidr(cidr: str, value: str, priv_data=None)

      same as add() with input a cidr string instead of net



   .. py:method:: add(net, value, priv_data: List[[ipaddress.IPv4Network | ipaddress.IPv6Network, str]] = None)

      Add (net, value) to cache where.
          if priv_data provided then new data saved there instead of self.data
          Used when have multiple threads/processing using same CidrCache instance

          Note that if add a (cidr, value) pair exists in cache but is different - 
          then this new added version will replace the existing one. 

          Better name might be add_or_replace()

      :param net:
          ipaddress network to add to cache

      :param value:
          the value to cache with net that is associated with it

      :priv_data:
          Optional list to hold added [net, value] pairs until they can be merged 
          into the class instance data via combine_data() method. Needed if sharing
          CidrCache instance across mutliple processes/threads.

          When present, all additions are made to private data instead of instance data
          and our own data is read only until all threads/processes finish

          Once all multiple threads/processes complete, then each private data cache(s) 
          can be combined into this instance data using combine_data(priv_data)

          When private data provided the dirty flag is left alone.
          combine() will set dirty if needed. This trackes where to save 
          cache file if data has changed.




   .. py:method:: compact()

      merge wherever possible - not used.



   .. py:method:: combine_data(new_data)

      Combine private data into this instance data

      :param new_data:
          List of data created by add() when provided private data list.
          All data from new_data is combined / merged into the instance data.



   .. py:method:: print()

      Print all the data



.. py:class:: CidrFile

   Class provides common CIDR string file reader/writer tools.
   All methods are static so no class instance variable needed.


   .. py:method:: read_cidrs(fname: str | None, verb: bool = False) -> ([str], [str])
      :staticmethod:


      Read file of cidrs and return tuple of separate lists (ip4, ip6)
          *  if fname is None or sys.stdin then data is read from stdin.
          *  only column 1 of file is used.
          *  comments are ignored

      :param fname:
          File name to read

      :param verb:
          More verbose output

      :returns:
          tuple of lists of cidrs (ip4, ip6)



   .. py:method:: read_cidr_file(fname: str, verb: bool = False) -> [str]
      :staticmethod:


       Read file of cidrs. Comments are ignored.
          Uses read_cidrs()

      :param fname:
          File name to read

      :param verb:
          More verbose output

      :returns:
          List of all cidrs (ip4 and ip6 combined)



   .. py:method:: read_cidr_files(targ_dir: str, file_list: [str]) -> [str]
      :staticmethod:


      Read set of files from a directory and return merged list of
      cidr strings



   .. py:method:: write_cidr_file(cidrs: [str], pname: str) -> bool
      :staticmethod:


      Write list of cidrs to a file

      :param cidrs:
          List of cidr strings to save

      :param pname:
          Path to file where cidrs are to be written



   .. py:method:: copy_cidr_file(src_file: str, dst_file: str) -> bool
      :staticmethod:


      Copy one file to another:

      :param src_file:
          Source file to copy

      :param dst_file:
          Where to save copy

      :returns:
          True if all okay else False




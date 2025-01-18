# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Public Methods
py_cidr 
"""
#
# Pre-class backward compat - Please Use Cidr.xxx() instead
#
#from .core import (is_valid_ip4, is_valid_ip6, is_valid_cidr, cidr_iptype, cidr_type_network)
#from .cidr import (cidr_to_net, cidrs_to_nets, nets_to_cidrs, compact_cidrs)
#from .cidr import (ip_to_address, ips_to_addresses, addresses_to_ips)
#from .cidr import (cidr_set_prefix, ipaddr_cidr_from_string, cidr_is_subnet)
#from .cidr import (address_iptype, compact_nets, net_exclude, nets_exclude)
#from .cidr import (cidrs_exclude, cidrs2_minus_cidrs1, cidr_exclude)
#from .cidr import (sort_cidrs, sort_ips)
#from .cidr import (get_host_bits, clean_cidr, clean_cidrs)
#from .cidr import (fix_cidr_host_bits, fix_cidrs_host_bits)
#from .cidr import (range_to_cidrs, cidr_to_range)
#from .cidr_files import (read_cidr_file, write_cidr_file, read_cidrs, read_cidr_files)
#from .cidr_files import (copy_cidr_file)

#
# Public
#
# used by sphinx but will also impact wildcard imports (dont use them)
#__all__ = ('Cidr', 'IPvxNetwork', 'IPvxAddress', 'CidrMap', 'CidrCache', 'CidrFile')

from .cidr_class import (Cidr, IPvxNetwork, IPvxAddress)
from .cidr_map import CidrMap
from .cidr_cache import CidrCache
from .cidr_file_class import CidrFile

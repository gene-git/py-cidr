# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
'''
Convenience types
'''
from typing import (TypeAlias)
from ipaddress import (IPv4Network, IPv6Network, IPv4Address, IPv6Address)

IPvxNetwork: TypeAlias = IPv4Network|IPv6Network
IPvxAddress: TypeAlias = IPv4Address|IPv6Address
IPAddress: TypeAlias = IPvxAddress|str

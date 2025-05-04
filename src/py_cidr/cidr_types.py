# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Convenience types
"""
from ipaddress import (IPv4Network, IPv6Network, IPv4Address, IPv6Address)

type IPvxNetwork = IPv4Network | IPv6Network
type IPvxAddress = IPv4Address | IPv6Address
type IPAddress = IPvxAddress | str

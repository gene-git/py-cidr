# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
"""
Convenience types:

Provides types IPvxNetwork, IPvxAddress and IPAddress which
are based on ipaddress types:

  IPv4Network, IPv6Network, IPv4Address and IPv6Address.

"""
from ipaddress import (IPv4Network, IPv6Network, IPv4Address, IPv6Address)

type IPvxNetwork = IPv4Network | IPv6Network
type IPvxAddress = IPv4Address | IPv6Address
type IPAddress = IPvxAddress | str

type IPv4 = IPv4Address | IPv4Network
type IPv6 = IPv6Address | IPv6Network

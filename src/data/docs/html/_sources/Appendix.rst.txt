.. SPDX-License-Identifier: GPL-2.0-or-later

========
Appendix
========

Installation
============

Available on
* `Github`_
* `Archlinux AUR`_

On Arch you can build using the provided PKGBUILD in the packaging directory or from the AUR.
To build manually, clone the repo and :

 .. code-block:: bash

        rm -f dist/*
        ./scripts/do-build
        ./scripts/do-install [destination]

The default destination is *build/pkg*.

Dependencies
============

**Run Time** :

* python          (3.14 or later)
* lockmgr
* patricia26

**Building Package** :

* cython
* gcc
* git
* meson
* meson-python
* uv
* python-uv-build
* rsync
* python-pytest
* python-pytest-asyncio


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

AI Tooling
==========

Assistance from:

* Anthropic's `Claude <https://claude.ai>`_ played a significant role updating and checking all C-code.

* Google's `Gemini <https://gemini.google.com/>`_ was especially helpful with Cython code.


.. _Github: https://github.com/gene-git/py-cidr
.. _Archlinux AUR: https://aur.archlinux.org/packages/py-cidr

.. [1] https://abseil.io/about/philosophy#upgrade-support



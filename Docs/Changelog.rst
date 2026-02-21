Changelog
=========

Tags
====

.. code-block:: text

	2.6.0 (2025-01-18) -> 3.12.0 (2026-02-21)
	41 commits.

Commits
=======


* 2026-02-21  : **3.12.0**

.. code-block:: text

              - **3.12.0**
            
                * CidrMap : New .items() method provides an Iterator over the map.
                  Each iteration yields a tuple[cidr: str, value: Any]
            
                * Add net_range_split/cidr_range_split:
                  split one net/cidr into (first, mid,  last) ip addresses
 2026-01-04   ⋯

.. code-block:: text

              - update Docs/Changelogs

* 2026-01-04  : **3.11.0**

.. code-block:: text

              - **3.11.0**
            
                * Code Reorg
                * Switch packaging from hatch to uv
                * Testing to confirm all working on python 3.14.2
                * License GPL-2.0-or-later

* 2025-09-01  : **3.10.0**

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf
              - Cidr.compact(): with  mixed ipv4/ipv6 - allow host bits in cidrs
 2025-08-31   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-08-31  : **3.9.0**

.. code-block:: text

              - compact(cidrs) can now handle mixed ipv4/ipv6
 2025-07-17   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-07-17  : **3.8.0**

.. code-block:: text

              - Cidr cache lockfile name use effective user id instead of username.

* 2025-07-17  : **3.7.0**

.. code-block:: text

              - Cidr cache lockfile: remove getlogin() line accidently left in - reported by AUR user @piate
 2025-07-16   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-07-16  : **3.6.0**

.. code-block:: text

              - Add net_to_cidr()
                Add sort_nets()
                Add net_is_subnet()
                Add address_to_net()
                Change cidr_iptype() address_iptype() to return empty string on invalid insteed of None
                Cidr Cache lockfile name: use effective user instead of real user
 2025-05-21   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-05-21  : **3.5.0**

.. code-block:: text

              - Use builtin types where possible. e.g. typing.List -> list
 2025-05-20   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-05-20  : **3.4.0**

.. code-block:: text

              - Remove unused files
              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-05-20  : **3.3.0**

.. code-block:: text

              - Fix for lockfile path when run in chroot.
                  As reported by AUR user @piater
 2025-05-19   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-05-19  : **3.2.2**

.. code-block:: text

              - Add pytest to checkdepnds in arch PKBUILD
                  Thanks to @Reylak pm AUR.
 2025-05-04   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-05-04  : **3.2.1**

.. code-block:: text

              - More documentation tweaks

* 2025-05-04  : **3.2.0**

.. code-block:: text

              - Improve API reference documentation.
                install: rename cache print to /usr/bin/py-cidr-cache-print
              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-05-04  : **3.1.1**

.. code-block:: text

              - Buglet: CidrMap::add_cidr() make private_cache optional argument again
 2025-05-03   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-05-03  : **3.0.1**

.. code-block:: text

              - Add tests to repo
              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf

* 2025-05-03  : **3.0.0**

.. code-block:: text

              - PEP-8, PEP-257 and PEP-484 style changes
                PEP 561 type hints (improves module use for type checkers e.g. *mypy*)
                CidrMap now uses separate CidrCache for "private cache data" instead of just the "data" part.
                  CidrCache class no longer needs its own "private data" functionality.
                Add some tests (via pytest)
                Reorganize CidrMap and simplify/improve way we do private_cache supporing
                  multiprocess/multithreading usecase. This is now all done in CidrMap.
                Change cache file storage to pickle format as its more flexible than json
                  Provide simple app to show contents of cache:
                  py-cidr-cache-print <cache_directory>

* 2025-04-02  : **2.8.0**

.. code-block:: text

              - update Docs/Changelogs Docs/_build/html Docs/py-cidr.pdf
              - Add RFC 1918 tools:
                      Cidr.is_rfc_1918()
                      Cidr.rfc_1918_nets()
                      Cidr.rfc_1918_cidrs()
                      Cidr.remove_rfc_1918()
                Reorganize code and separate into more files for better maintainability
 2025-03-10   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/_build/html Docs/py-cidr.pdf

* 2025-03-10  : **2.7.0**

.. code-block:: text

              - Bugfix: sorting mixed list of IPv4 and IPv6
 2025-01-18   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/_build/html Docs/py-cidr.pdf

* 2025-01-18  : **2.6.3**

.. code-block:: text

              - Readme - removed unused (template) sections
              - update Docs/Changelog.rst Docs/_build/html Docs/py-cidr.pdf

* 2025-01-18  : **2.6.2**

.. code-block:: text

              - fix readme rst syntax
              - update Docs/Changelog.rst Docs/_build/html Docs/py-cidr.pdf

* 2025-01-18  : **2.6.1**

.. code-block:: text

              - Small change to readme
              - update Docs/Changelog.rst Docs/_build/html Docs/py-cidr.pdf

* 2025-01-18  : **2.6.0**

.. code-block:: text

              - Initial release



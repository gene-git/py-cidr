.. SPDX-License-Identifier: GPL-2.0-or-later

Recent Changes
==============

**5.0.2**

* New PyCidr class - replaces functionality in Cidr class.
  Using the pure C-code *cidrtools* library and its python bindings *cidrtools-cffi*

  - Superior performance.  For example compacting lists of cidr blocks runs
    about 10 - 20 times faster.

  - API is similar but migrating the code will unlock the perfomance benefit.
  - Depends on two new packages: *cidrtools* and *cidrtools-cffi*
  - Updated build system using meson and uv.

* Cidr class still supported unchanged. 
  This facilitates testing and comparing Cidr with PyCidr.
  In the future, some/all of Cidr may be migrated to use the new fast codebase.

* See manual for details and how to use the new speedy class!

* Add the manual


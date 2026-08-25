 
API Reference Guide
===================

Cidr is the original class and over time it's API has grown in part to
maintain backward compatibility and in part it has a dual personality.
It is built on top of Python's native *ipaddress* class and ended up supporting
network input/output in both string and *ipaddress* format.

PyCidr is designed for performance and simplicity. It only uses strings for 
IP address and CIDR blocks. The code is writein in Cython/C-code and is significantly
faster than the Cidr class variants. For example, our tests show compacting a list of
CIDRs to the smallest number runs 18 to 22 times faster.

We recommend migrating to PyCidr. This is completely optional. The Cidr class remains
supported. If you choose to migrate then it means using strings only (no ipaddress).
If code is already strings the migration is pretty straight forward and
there is a quick guide how to do so.


The next section has the auto-generated API reference.

PyCidr Class
------------

.. toctree::
   :maxdepth: 2
   :caption: PyCidr Overview:

   pycidr-overview

.. automodule:: py_cidr.pycidr_class
   :members:
   :undoc-members:
   :show-inheritance:

Cidr Class
----------

.. automodule:: py_cidr.cidr_class
   :members:
   :undoc-members:
   :show-inheritance:


File Utilities
--------------

.. automodule:: py_cidr.cidr_file_class
   :members:
   :undoc-members:
   :show-inheritance:


Cidr Map
--------

This tool uses Patricia Tree to maintain a map of cidr -> <value>.
For example a map of all network prefixes where the <value> might be the country
that network is located or registered in.

.. automodule:: py_cidr.cidr_map
   :members:
   :undoc-members:
   :show-inheritance:



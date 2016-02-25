F5 Python SDK Documentation
===========================
|Build Status|

Introduction
------------
This project implements an SDK for the iControl REST interface for the BigIP.
Users of this library can create, edit, update, and delete configuration
objects on a BigIP device.

Submodules
~~~~~~~~~~
bigip
^^^^^
Python API for configuring objects on a BIG-IP device and gathering information
from the device via the REST API.

Installation
------------
.. code:: shell

    $> pip install f5-sdk

*NOTE:* If you are using a pre-release version you must use the ``--pre``
option with the pip command.

Usage
-----
.. code:: python

    from f5.bigip import BigIP
    bigip = BigIP("bigip.example.com", "admin", "somepassword")
    pools = bigip.ltm.pool.getcollection()

SDK Contents
------------
.. toctree::
   :maxdepth: 4

   apidoc/modules


Contact
-------
f5_common_python@f5.com

Copyright
---------
Copyright 2014-2016 F5 Networks Inc.

Support
-------
Maintenance and support of the unmodified F5 code is provided only to customers
who have an existing support contract, purchased separately subject to F5’s
support policies available at http://www.f5.com/about/guidelines-policies/ and
http://askf5.com.  F5 will not provide maintenance and support services of
modified F5 code or code that does not have an existing support contract.

License
-------
Apache V2.0
~~~~~~~~~~~
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.

Contributor License Agreement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Individuals or business entities who contribute to this project must have
completed and submitted the `F5 Contributor License Agreement
<http://f5-openstack-docs.readthedocs.org/en/latest/cla_landing.html>`__
to Openstack_CLA@f5.com prior to their code submission being included in this
project.

.. |Build Status| image:: https://travis-ci.com/F5Networks/f5-common-python.svg?token=s9yQgrQoSkLe6ec4WQKS&branch=develop
   :target: https://travis-ci.com/F5Networks/f5-common-python

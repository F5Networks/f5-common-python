F5 Python SDK Documentation
===========================
|Build Status| |Docs Build Status|

Introduction
------------
This project implements an object model based SDK for the F5 Networks BIG-IP
iControl REST interface. Users of this library can create, edit, update, and
delete configuration objects on a BIG-IP device.  For more information on the
basic principals that the SDK uses see the :doc:`userguide/index`.

Quick Start
-----------
Installation
~~~~~~~~~~~~
.. code:: shell

    $> pip install f5-sdk

.. note::
    If you are using a pre-release version you must use the ``--pre``
    option with the pip command.

Basic Example
~~~~~~~~~~~~~
.. code:: python

    from f5.bigip import BigIP

    # Connect to the BigIP
    bigip = BigIP("bigip.example.com", "admin", "somepassword")

    # Get a list of all pools on the BigIP and print their name and their
    # members' name
    pools = bigip.ltm.pools.get_collection()
    for pool in pools:
        print pool.name
        for member in pool.members_s.get_collection():
             print member.name

    # Create a new pool on the BigIP
    mypool = bigip.ltm.pools.pool.create(name='mypool', partition='Common')

    # Load an existing pool and update its description
    pool_a = bigip.ltm.pools.pool.load(name='mypool', partition='Common')
    pool_a.description = "New description"
    pool_a.update()

    # Delete a pool if it exists
    if bigip.ltm.pools.pool.exists(name='mypool', partition='Common'):
        pool_b = bigip.ltm.pools.pool.load(name='mypool', partition='Common')
        pool_b.delete()

Detailed Documentation
----------------------

.. toctree::
   :maxdepth: 4

   userguide/index
   devguide
   F5 SDK API Docs <apidoc/modules>


Contact
-------
f5_common_python@f5.com

Copyright
---------
Copyright 2014-2016 F5 Networks Inc.

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

.. |Build Status| image:: https://travis-ci.org/F5Networks/f5-common-python.svg?branch=0.1
    :target: https://travis-ci.org/F5Networks/f5-common-python
    :alt: Build Status

.. |Docs Build Status| image:: http://readthedocs.org/projects/f5-sdk/badge/?version=latest
    :target: http://f5-sdk.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
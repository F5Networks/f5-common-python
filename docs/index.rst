F5 Python SDK Documentation
===========================
|Build Status| |Docs Build Status|

.. raw:: html

    <script async defer src="https://f5-openstack-slack.herokuapp.com/slackin.js"></script>


Introduction
------------
This project implements an object model based SDK for the F5 Networks® BIG-IP®
iControl® REST interface. Users of this library can create, edit, update, and
delete configuration objects on a BIG-IP®. For more information on the
basic principals that the SDK uses, see the :doc:`userguide/index`.

Quick Start
-----------
Installation
~~~~~~~~~~~~
.. code:: shell

    $ pip install f5-sdk


Basic Example
~~~~~~~~~~~~~
.. code:: python

    from f5.bigip import ManagementRoot

    # Connect to the BigIP
    mgmt = ManagementRoot("bigip.example.com", "admin", "somepassword")

    # Get a list of all pools on the BigIP and print their names and their
    # members' names
    pools = mgmt.tm.ltm.pools.get_collection()
    for pool in pools:
        print pool.name
        for member in pool.members_s.get_collection():
             print member.name

    # Create a new pool on the BIG-IP
    mypool = mgmt.tm.ltm.pools.pool.create(name='mypool', partition='Common')

    # Load an existing pool and update its description
    pool_a = mgmt.tm.ltm.pools.pool.load(name='mypool', partition='Common')
    pool_a.description = "New description"
    pool_a.update()

    # Delete a pool if it exists
    if mgmt.tm.ltm.pools.pool.exists(name='mypool', partition='Common'):
        pool_b = mgmt.tm.ltm.pools.pool.load(name='mypool', partition='Common')
        pool_b.delete()

Detailed Documentation
----------------------

.. toctree::
   :maxdepth: 6

   userguide/index
   devguide
   F5 SDK API Docs <apidoc/modules>

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


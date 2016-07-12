f5-common-python
================

|Build Status| |Docs Build Status| |slack badge|

Introduction
------------
This project implements an SDK for the iControl® REST interface for BIG-IP®.
Use this library to use python to automate a BIG-IP® via its REST API.

Documentation
-------------
Please see the project documentation on Read the Docs: http://f5-sdk.readthedocs.io.

Installation
------------

.. code:: shell

    $ pip install f5-sdk

.. note::

    If you are using a pre-release version you must use the ``--pre``
    option for the ``pip`` command.

Usage
-----

.. code:: python

    from f5.bigip import ManagementRoot

    # Connect to the BIG-IP
    mgmt = ManagementRoot("bigip.example.com", "admin", "somepassword")

    # Get a list of all pools on the BigIP and print their name and their
    # members' name
    pools = mgmt.tm.ltm.pools.get_collection()
    for pool in pools:
        print pool.name
        for member in pool.members_s.get_collection():
            print member.name

    # Create a new pool on the BigIP
    mypool = mgmt.tm.ltm.pools.pool.create(name='mypool', partition='Common')

    # Load an existing pool and update its description
    pool_a = mgmt.tm.ltm.pools.pool.load(name='mypool', partition='Common')
    pool_a.description = "New description"
    pool_a.update()

    # Delete a pool if it exists
    if mgmt.tm.ltm.pools.pool.exists(name='mypool', partition='Common'):
        pool_b = mgmt.tm.ltm.pools.pool.load(name='mypool', partition='Common')
        pool_b.delete()

Design Patterns
~~~~~~~~~~~~~~~

I intend the SDK to be easy to use and easy to hack.  These overarching goals
have a strong influence on my thinking when I am reviewing contributions, this
means it is in their own interest that I make them as explicit as possible!

The original interface specification was given to me by Shawn Wormke, who I
believe was influenced by the Jira and Django projects.  At the time I was
reading Brett Slatkin's 'Effective Python', and I tried to follow its advice
where possible.

List of Patterns For Contributing Developers
--------------------------------------------

#. Hack this list to make it more correct/complete
    For list additions assign @zancas as the PR reviewer.
#. The call operator ``()`` means: "Try to communicate with the device."
    This is a strong contract we offer the consumer of the SDK. If an SDK
    function is invoked with the call operator ``()`` the program is initiating
    a communication with the device.  That communication may fail before
    reaching the wire, but it has nonetheless been initiated.  Conversely, if
    an SDK user evaluates an SDK expression that *DOES NOT* invoke the ``()``
    call operator, then the SDK does *NOT* initiate a communication with the
    device.  Any extension to the SDK that is not consistent with this contract
    is unlikely to be incorporated into the supported repository.
#. The SDK is stupid
    The SDK doesn't decide things for the consumer, it's
    simply an interface so that Python programs can manipulate device resources
    without implementing custom URI/HTTP/network logic.  Implications:

   #. NO DEFAULTS
       The consumers of this library are themselves Python
       programs.  The Application programmer must say what they mean in their
       SDK-using program.  It violates a critical separation of concerns to add
       default values to the SDK.  Don't do it!  (Unless you have a good
       reason.)
   #. Failures generate exceptions  
       If the SDK enters a surprising or
       unexpected state it raises an exception.  That's it.  It's not generally
       up to the SDK to implement decision logic that handles edge-cases..
       EXCEPT where the SDK is smoothing known issues in the device REST
       server. (See below.)  
   #. The SDK never interprets responses
       It just records whatever response
       the device returns as attributes of the relevant object. (Except where
       handling significant inconsistencies in the device interface.)

#. public-nonpublic pairs
    e.g. 'create' and '_create' XXX add content here.
#. Handle known issues in the device REST server.
    The SDK intends to provide
    a rational interface to consumers that does the right thing.  This means
    that one case where it does NOT simply do the stupid thing is when it
    handles a known idiosyncrasy in the device REST server.  For example, some?
    resources ignore 'disable' and 'enable' configuration options when they are
    set to 'False'. Rather than force a consumer to learn about this quirk in
    the server, the SDK guesses that '"disable": False' means '"enable": True'
    , and submits that value on the consumers behalf.
#. Implement-Reimplement-Abstract
    Solve the problem concretely and simply, if
    the same problem arises again, solve it concretely, then take the two
    concrete solutions and use them as your specification to generate an
    abstraction. In the SDK this usually goes something like this:

   #. Add logic to a concrete subclass
   #. Add similar logic to another concrete subclass
   #. Create a new method in a mixin or Abstract 'resource.py' base class and
      have both concrete subclasses inherit and use that method.
  

Submodules
~~~~~~~~~~

bigip
^^^^^
Python API for configuring objects on a BIG-IP® device and gathering information
from the device via the REST API.

Filing Issues
-------------
See the Issues section of `Contributing <CONTRIBUTING.md>`__.

Contributing
------------
See `Contributing <CONTRIBUTING.md>`__

Test
----
Before you open a pull request, your code must have passing
`pytest <http://pytest.org>`__ unit tests. In addition, you should
include a set of functional tests written to use a real BIG-IP device
for testing. Information on how to run our set of tests is included
below.

Unit Tests
~~~~~~~~~~
We use pytest for our unit tests.

#. If you haven't already, install the required test packages listed in
   requirements.test.txt in your virtual environment.

   .. code:: shell

       $ pip install -r requirements.test.txt

#. Run the tests and produce a coverage report. The ``--cov-report=html`` will
   create a ``htmlcov/`` directory that you can view in your browser to see the
   missing lines of code.

   .. code:: shell

       py.test --cov ./icontrol --cov-report=html
       open htmlcov/index.html


Style Checks
~~~~~~~~~~~~
We use the hacking module for our style checks (installed as part of step 1 in
the Unit Test section).

.. code:: shell

    $ flake8 ./

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

.. |slack badge| image:: https://f5-openstack-slack.herokuapp.com/badge.svg
    :target: https://f5-openstack-slack.herokuapp.com/
    :alt: Slack

.. |coveralls| image:: https://coveralls.io/repos/github/F5Networks/f5-common-python/badge.svg
    :target: https://coveralls.io/github/F5Networks/f5-common-python
    :alt: Coveralls
f5-common-python
================

|Build Status|

Introduction
------------
F5 Networks BIG-IP python SDK. This project implements an SDK for the iControl
REST interface for the BigIP. Users of this library can create, edit, update,
and delete configuration objects on a BigIP device.

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
option for the ``pip`` command.

Usage
-----

.. code:: python

    from f5.bigip import BigIP
    bigip = BigIP("bigip.example.com", "admin", "somepassword")
    pools = bigip.ltm.pool.getcollection()

Documentation
-------------

Documentation is hosted on `Read the Docs <https://f5-sdk.readthedocs.org>`__

Filing Issues
-------------
See the Issues section of `Contributing <CONTRIBUTING.md>`__.

Contributing
------------
See `Contributing <CONTRIBUTING.md>`__

Build
-----

#. Python Package:
   To build a python package that can be installed using pip. The
   output is in 'dist'.

   .. code:: shell

       $ make source

#. Debian Package
   On a debian system you can build debian packages if you have
   installed ``python-all``, ``fakeroot``, and ``python-stdeb``

   .. code:: shell

       $ sudo apt-get install python-all fakeroot python-stdeb
       $ make debs

   On a system that has docker installed, you can use the docker\_debs target.
   This will launch a trusty container to build a debian package.

   .. code:: shell

       $ make docker_debs

#. RedHat/Centos 7 Package
   On a RedHat/Centos 7 system you can build RPMS if you have installed make
   and rpm-build rpms.

   .. code:: shell

       $ sudo yum install make rpm-build
       $ make rpms

   On a system that has docker installed, you can use the docker\_rpms target.
   This will launch a centos7 container to build the f5-bigip-common package

   .. code:: shell

       $ make docker_rpms

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

#. If you haven't already, install the required test packages and the
   requirements.txt in your virtual environment.

   .. code:: shell

       $ pip install hacking pytest pytest-cov
       $ pip install -r requirements.txt

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

    flake8 ./

Contact
-------

f5_common_python@f5.com

Copyright
---------

Copyright 2014-2016 F5 Networks Inc.

Support
-------

See `Support <SUPPORT.md>`__

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
<http://f5networks.github.io/f5-openstack-docs/cla_landing/index.html>`__
to Openstack_CLA@f5.com prior to their code submission being included in this
project.

.. |Build Status| image:: https://travis-ci.org/F5Networks/f5-common-python.svg?branch=0.1
    :target: https://travis-ci.org/F5Networks/f5-common-python

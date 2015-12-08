f5-common-python
================
[![Build Status](https://magnum.travis-ci.com/F5Networks/f5-common-python.svg?token=s9yQgrQoSkLe6ec4WQKS&branch=develop)](https://magnum.travis-ci.com/F5Networks/f5-common-python)
Introduction
------------
TODO: Add something more meaningful
F5 Networks BIG-IP and BIG-IQ python API.

Submodules
----------
#### bigip
Python API for configuring objects on a BIG-IP device and gathering information
from the device via the REST API.

#### bigiq
TODO: Lets figure out what this does and if we should even have it in this library

Installation
------------
```bash
$> pip install f5
```

Configuration
-------------
TODO: I think this is N/A,but there are some cache directories indicated in the bigip/pycontrol sub libraries

Usage
-----
```python
from f5.bigip import BigIP
bigip = BigIP("bigip.example.com", "admin", "somepassword")
device_name = bigip.devicename()
```

Documentation
-------------
TODO: Point to read the docs and any other usage docs that we may have

Filing Issues
-------------
TODO: How to file bugs vs enhancements

Contributing
------------
See [Contributing](CONTRIBUTING.md)

Build
-----
1. Python Package:

To build a python package that can be installed using pip.  The output is in 'dist'.
```shell
$ make source
```

2. Debian Package

On a debian system you can build debian packages if you have installed python-all, fakeroot, and python-stdeb
```shell
$ sudo apt-get install python-all fakeroot python-stdeb
$ make debs
```

On a system that has docker installed you can use the docker_debs target.  This will launch a trusty container to build
a debian package.
```shell
$ make docker_debs
```

3. RedHat/Centos 7 Package

On a RedHat/Centos 7 system you can build RPMS if you have installed make and rpm-build rpms.
```shell
$ sudo yum install make rpm-build
$ make rpms
```
On a system that has docker installed you can use the docker_rpms target.  This will launch a centos7 container to build
the f5-bigip-common package
```shell
$ make docker_rpms
```

Test
----
All code must have passing [pytest](http://pytest.org) unit tests prior to
submitting a pull request.  In addition there should be a set of functional
tests that are written to use a real BIG-IP device for testing.  Below is
information on how to run our various tests.

We use pytest for our unit and functional tests.  Install the required test 
packages and the requirements.txt in your virtual environment.
```shell
$ pip install hacking pytest pytest-cov
$ pip install -r requirements.txt
```

#### Unit Tests
All unit tests are located in the f5/ directory.  Run the tests and produce a 
coverage report.  The `--cov-report=html` will create a `htmlcov/` directory 
that you can view in your browser to see the missing lines of code.
```shell
$ py.test --cov ./f5 --cov-report=html
$ open htmlcov/index.html
```

#### Functional Tests
All functional tests are located in the test/functional directory.  Functional
tests are BYOD (Bring Your Own Device).  Create a BIG-IP using your favorite
tool or cloud, such as AWS, OpenStack or even bare-metal. The IPv4 address must
be reachable from wherever your will run the tests.
```shell
$ py.test ./test/functional --bigip=10.2.1.4  # run all functional tests
$ py.test ./test/functional/test_nat.py --bigip=10.2.1.4  # run all nat tests
```

Contact
-------
<f5-common-python@f5.com>

Copyright
---------
Copyright 2014 F5 Networks Inc.

License
-------
See [License](LICENSE)

Support
-------
These modules are Free Software available under the Apache License
Version 2.0, and are provided without Warranty or Support under 
existing support contracts for F5 products.

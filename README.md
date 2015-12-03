f5-common-python
================
[![Build Status](https://magnum.travis-ci.com/F5Networks/f5-common-python.svg?token=s9yQgrQoSkLe6ec4WQKS&branch=develop)](https://magnum.travis-ci.com/F5Networks/f5-common-python)
Introduction
------------
TODO: Add something more meaningful
F5 Networks BIG-IP and BIG-IQ python API.

Submodules
----------
TODO: List these and what they do

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
$ make source

2. Debian Package

On a debian system you can build debian packages if you have installed python-all, fakeroot, and python-stdeb
$ sudo apt-get install python-all fakeroot python-stdeb
$ make debs

On a system that has docker installed you can use the docker_debs target.  This will launch a trusty container to build
a debian package.
$ make docker_debs

3. RedHat/Centos 7 Package

On a RedHat/Centos 7 system you can build RPMS if you have installed make and rpm-build rpms.
$ sudo yum install make rpm-build
$ make rpms

On a system that has docker installed you can use the docker_rpms target.  This will launch a centos7 container to build
the f5-bigip-common package
$ make docker_rpms

Test
----
TODO

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

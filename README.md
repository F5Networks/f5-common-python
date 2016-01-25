<!--
Copyright 2015 F5 Networks Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->
# f5-common-python
[![Build Status](https://travis-ci.com/F5Networks/f5-common-python.svg?token=s9yQgrQoSkLe6ec4WQKS&branch=develop)](https://travis-ci.com/F5Networks/f5-common-python)

## Introduction
F5 Networks BIG-IP python SDK.  This project implements an SDK for the
iControl REST interface for the BigIP.  Users of this library can create, edit,
update, and delete configuration objects on a BigIP device.

### Submodules

#### bigip
Python API for configuring objects on a BIG-IP device and gathering information
from the device via the REST API.

## Installation
```
bash
$> pip install f5
```

## Configuration
TODO: I think this is N/A, but there are some cache directories indicated in the bigip/pycontrol sub libraries.

## Usage
```
python
from f5.bigip import BigIP
bigip = BigIP("bigip.example.com", "admin", "somepassword")
device_name = bigip.devicename()
```

## Documentation
TODO: Point to read the docs and any other usage docs that we may have

## Filing Issues
If you find an issue we would love to hear about it. Please let us know by
filing an issue in this repository and tell us as much as you can about what
you found and how you found it.

## Contributing
See [Contributing](CONTRIBUTING.md)

## Build

1. Python Package:
To build a python package that can be installed using pip. The output is in 'dist'.
```
shell
$ make source
```
2. Debian Package
On a debian system you can build debian packages if you have installed `python-all`, `fakeroot`, and `python-stdeb`
```
shell
$ sudo apt-get install python-all fakeroot python-stdeb
$ make debs
```
On a system that has docker installed, you can use the docker_debs target. This will launch a trusty container to build
a debian package.
```shell
$ make docker_debs
```
3. RedHat/Centos 7 Package
On a RedHat/Centos 7 system you can build RPMS if you have installed make and rpm-build rpms.
```
shell
$ sudo yum install make rpm-build
$ make rpms
```
On a system that has docker installed, you can use the docker_rpms target. This will launch a centos7 container to build
the f5-bigip-common package
```shell
$ make docker_rpms
```

## Test
Before you open a pull request, your code must have passing [pytest](http://pytest.org) unit tests. In addition, you should include a set of functional tests written to use a real BIG-IP device for testing. Information on how to run our set of tests is included below.

### Unit Tests
We use pytest for our unit tests.
1. If you haven't already, install the required test packages and the requirements.txt in your virtual environment.
```shell
$ pip install hacking pytest pytest-cov
$ pip install -r requirements.txt
```
2. Run the tests and produce a coverage report.  The `--cov-report=html` will
create a `htmlcov/` directory that you can view in your browser to see the
missing lines of code.
```
shell
py.test --cov ./icontrol --cov-report=html
open htmlcov/index.html
```

### Style Checks
We use the hacking module for our style checks (installed as part of
step 1 in the Unit Test section).
```shell
flake8 ./
```

## Contact
<f5_common_python@f5.com>

## Copyright
Copyright 2014-2016 F5 Networks Inc.

## Support
See [Support](SUPPORT.md)

## License
 
### Apache V2.0
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 
### Contributor License Agreement
Individuals or business entities who contribute to this project must have completed and submitted the [F5 Contributor License Agreement](http://f5networks.github.io/f5-openstack-docs/cla_landing/index.html) to Openstack_CLA@f5.com prior to their
code submission being included in this project.
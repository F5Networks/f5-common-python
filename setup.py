#!/usr/bin/env python

# Copyright 2014 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import f5

from setuptools import find_packages
from setuptools import setup


setup(
    name='f5-sdk',
    description='F5 Networks Python SDK',
    license='Apache License, Version 2.0',
    version=f5.__version__,
    author='F5 Networks',
    author_email='f5_common_python@f5.com',
    url='https://github.com/F5Networks/f5-common-python',
    keywords=['F5', 'sdk', 'api', 'icontrol', 'bigip', 'api', 'ltm'],
    install_requires=['f5-icontrol-rest >= 1.0.6'],
    packages=find_packages(
        exclude=["*.test", "*.test.*", "test.*", "test_*", "test", "test*"]
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: System Administrators',
    ]
)

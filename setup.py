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

import os
import sys

from setuptools import find_packages
from setuptools import setup

if 'PROJECT_DIR' in os.environ:
    project_dir = os.environ['PROJECT_DIR']
else:
    project_dir = os.path.curdir


def version():
    version = ""
    if 'VERSION' in os.environ:
        version = os.environ['VERSION']
    elif os.path.isfile('VERSION'):
        with open('VERSION') as f:
            version = f.read()
    else:
        version = 'Unknown'

    return version


def release():
    if 'RELEASE' in os.environ:
        release = os.environ['RELEASE']
    elif os.path.isfile('RELEASE'):
        with open('RELEASE') as f:
            release = f.read().strip()
    else:
        release = 'Unknown'

    return release

if 'bdist_deb' in sys.argv:
    stdebcfg = open('stdeb.cfg', 'w')
    stdebcfg.write('[DEFAULT]\n')
    stdebcfg.write('Package: f5-bigip-common\n')
    stdebcfg.write('Debian-Version: ' + release() + '\n')
    stdebcfg.write('Depends: python-suds\n')
    stdebcfg.close()

if 'bdist_rpm' in sys.argv:
    setupcfg = open('setup.cfg', 'w')
    setupcfg.write('[bdist_rpm]\n')
    setupcfg.write('release=%s\n' % release())
    setupcfg.write('requires=python-suds > 0.3\n')
    setupcfg.close()


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='f5-bigip-common',
      description='F5 Networks BIG-IP and BIG-IQ python API',
      long_description=readme(),
      version=version(),

      author='f5-common-python',
      author_email='f5-common-python@f5.com',
      url='https://github.com/F5Networks/f5-common-python',

      # Runtime dependencies.
      install_requires=[
          'eventlent',
          'f5-icontrol-rest',
          'netaddr',
          'pyopenssl',
          'requests',
          'suds'],

      packages=find_packages(exclude=["*.test", "*.test.*", "test*", "test"]),

      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Intended Audience :: System Administrators']
      )

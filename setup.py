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

from distutils.core import setup

if 'VERSION' in os.environ:
    version = os.environ['VERSION']
elif os.path.isfile('VERSION'):
    version_file = open('VERSION', 'r')
    version = version_file.read()
    version = version.strip()
    version_file.close()
else:
    version = 'Unknown'

if 'RELEASE' in os.environ:
    release = os.environ['RELEASE']
elif os.path.isfile('RELEASE'):
    release_file = open('RELEASE', 'r')
    release = release_file.read()
    release = release.strip()
    release_file.close()
else:
    release = 'Unknown'

if 'PROJECT_DIR' in os.environ:
    project_dir = os.environ['PROJECT_DIR']
else:
    project_dir = os.path.curdir

if 'bdist_deb' in sys.argv:
    stdebcfg = open('stdeb.cfg', 'w')
    stdebcfg.write('[DEFAULT]\n')
    stdebcfg.write('Package: f5-bigip-common\n')
    stdebcfg.write('Debian-Version: ' + release + '\n')
    stdebcfg.write('Depends: python-suds\n')
    stdebcfg.close()

if 'bdist_rpm' in sys.argv:
    setupcfg = open('setup.cfg', 'w')
    setupcfg.write('[bdist_rpm]\n')
    setupcfg.write('release=%s\n' % release)
    setupcfg.write('requires=python-suds > 0.3\n')
    setupcfg.close()

setup(name='f5-bigip-common',
      description='F5 LBaaS Agent for OpenStack',
      long_description='F5 LBaaS Agent for OpenStack',
      license='Apache License, Version 2.0',
      version=version,
      author='F5 DevCentral',
      author_email='devcentral@f5.com',
      url='http://devcentral.f5.com/openstack',
      py_modules=[
                  'f5.bigip.bigip',
                  'f5.bigip.exceptions',
                  'f5.bigip.interfaces.arp',
                  'f5.bigip.interfaces.cluster',
                  'f5.bigip.interfaces.device',
                  'f5.bigip.interfaces.iapp',
                  'f5.bigip.interfaces.interface',
                  'f5.bigip.interfaces.l2gre',
                  'f5.bigip.interfaces.monitor',
                  'f5.bigip.interfaces.nat',
                  'f5.bigip.interfaces.pool',
                  'f5.bigip.interfaces.route',
                  'f5.bigip.interfaces.rule',
                  'f5.bigip.interfaces.selfip',
                  'f5.bigip.interfaces.snat',
                  'f5.bigip.interfaces.stat',
                  'f5.bigip.interfaces.system',
                  'f5.bigip.interfaces.virtual_server',
                  'f5.bigip.interfaces.vlan',
                  'f5.bigip.interfaces.vxlan',
                  'f5.bigip.pycontrol.pycontrol',
                  'f5.bigiq.bigiq',
                  'f5.common.logger',
                  'f5.common.constants'
      ],
      packages=['f5',
                'f5.bigip',
                'f5.bigip.interfaces',
                'f5.bigip.pycontrol',
                'f5.bigiq',
                'f5.common'
                ],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: Apache Software License',
                   'Environment :: OpenStack',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Intended Audience :: System Administrators']
      )

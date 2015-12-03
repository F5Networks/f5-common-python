# Copyright 2015 F5 Networks Inc.
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

from f5.bigip.sys.iapp import IApp
from f5.bigip.sys.stat import Stat
from f5.bigip.sys.system import System

base_uri = 'sys/'


class Sys(object):
    def __init__(self, bigip):
        self.interfaces = {}
        self.bigip = bigip

    @property
    def iapp(self):
        if 'iapp' in self.interfaces:
            return self.interfaces['iapp']
        else:
            iapp = IApp(self.bigip)
            self.interfaces['iapp'] = iapp
            return iapp

    @property
    def stat(self):
        if 'stat' in self.interfaces:
            return self.interfaces['stat']
        else:
            stat = Stat(self.bigip)
            self.interfaces['stat'] = stat
            return stat

    @property
    def system(self):
        if 'system' in self.interfaces:
            return self.interfaces['system']
        else:
            system = System(self.bigip)
            self.interfaces['system'] = system
            return system

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

from f5.bigip.cm.cluster import Cluster
from f5.bigip.cm.device import Device

base_uri = 'cm/'


class CM(object):
    def __init__(self, bigip):
        self.interfaces = {}
        self.bigip = bigip

    @property
    def cluster(self):
        if 'cluster' in self.interfaces:
            return self.interfaces['cluster']
        else:
            cluster = Cluster(self.bigip)
            self.interfaces['cluster'] = cluster
            return cluster

    @property
    def device(self):
        if 'device' in self.interfaces:
            return self.interfaces['device']
        else:
            device = Device(self.bigip)
            self.interfaces['device'] = device
            return device

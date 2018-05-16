# coding=utf-8
#
# Copyright 2018 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""BIG-IP® system cluster module

REST URI
    ``https://localhost/mgmt/tm/sys/cluster``

GUI Path
    ``System --> Clusters``

REST Kind
    ``tm:sys:cluster:*``
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Stats
from f5.bigip.resource import UnnamedResource


class Cluster(OrganizingCollection):
    """BIG-IP® license unnamed resource"""
    def __init__(self, sys):
        super(Cluster, self).__init__(sys)
        self._meta_data['required_json_kind'] =\
            "tm:sys:cluster:clustercollectionstate"
        self._meta_data['allowed_lazy_attributes'] = [Default, Stats]


class Default(UnnamedResource):
    """BIG-IP® Analytics settings resource"""
    def __init__(self, settings):
        super(Default, self).__init__(settings)
        self._meta_data['required_json_kind'] = \
            'tm:sys:cluster:clusterstate'
        self._meta_data['allowed_lazy_attributes'] = [Stats]

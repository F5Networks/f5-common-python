# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

"""BIG-IP® ltm default node monitor module

REST URI
    ``http://localhost/mgmt/tm/ltm/default-node-monitor``

GUI Path
    ``Local Traffic --> Nodes --> Default Monitor``

REST Kind
    ``tm:ltm:default-node-monitor:*``
"""

from f5.bigip.resource import UnnamedResource


class Default_Node_Monitor(UnnamedResource):
    """BIG-IP® ltm default node monitor resource

    The default node monitor object only supports load and update because it
    is an unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, ltm):
        super(Default_Node_Monitor, self).__init__(ltm)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:ltm:default-node-monitor:default-node-monitorstate'

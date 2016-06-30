# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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
"""BIG-IP® shared failover state module

REST URI
    ``http://localhost/mgmt/tm/shared/bigip-failover-state``

GUI Path
    N/A

REST Kind
    ``tm:shared:licensing:*``
"""

from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedMethod


class Bigip_Failover_State(UnnamedResource):
    """BIG-IP® failover state information

    Failover state objects only support the
    :meth:`~f5.bigip.resource.Resource.load` method because they cannot be
    modified via the API.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """

    def __init__(self, shared):
        super(Bigip_Failover_State, self).__init__(shared)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] = ''
        self._meta_data['minimum_version'] = '12.0.0'

    def update(self, **kwargs):
        '''Update is not supported for BIG-IP® failover state.

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )

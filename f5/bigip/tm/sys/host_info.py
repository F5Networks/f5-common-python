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

"""BIG-IP® system host-info module

REST URI
    ``http://localhost/mgmt/tm/sys/host-info``

REST Kind
    ``tm:sys:host-info:host-infostats:*``
"""

from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedMethod


class Host_Info(UnnamedResource):
    """BIG-IP® system host info unnamed resource"""
    def __init__(self, sys):
        super(Host_Info, self).__init__(sys)
        self._meta_data['object_has_stats'] = False
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:host-info:host-infostats'

    def update(self, **kwargs):
        """Update is not supported for host info

        :raises: :exc:`~f5.BIG-IP.resource.UnsupportedMethod`
        """
        raise UnsupportedMethod("{0} does not support the update method, only load and refresh".format(self.__class__.__name__))

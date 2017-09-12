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

from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedOperation


class Session_Tracking(UnnamedResource):
    """BIG-IP® ASM Session Tracking resource."""
    def __init__(self, policy):
        super(Session_Tracking, self).__init__(policy)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:session-tracking:session-awareness-settingsstate'
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'

    def update(self, **kwargs):
        """Update is not supported for Session Tracking resource

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )

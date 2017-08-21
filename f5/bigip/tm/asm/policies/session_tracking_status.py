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

from f5.sdk_exception import UnsupportedOperation
from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection


class Session_Tracking_Statuses_s(Collection):
    """BIG-IP® ASM Session Tracking Statuses sub-collection."""
    def __init__(self, policy):
        super(Session_Tracking_Statuses_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Session_Tracking_Status]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:session-tracking-statuses:session-tracking-statuscollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:session-tracking-statuses:session-tracking-statusstate': Session_Tracking_Status
        }


class Session_Tracking_Status(AsmResource):
    """BIG-IP® ASM Session TrackingStatus resource."""
    def __init__(self, session_tracking_statuses_s):
        super(Session_Tracking_Status, self).__init__(
            session_tracking_statuses_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:session-tracking-statuses:session-tracking-statusstate'
        self._meta_data['required_creation_parameters'] = {
            'action', 'scope', 'value'
        }

    def modify(self, **kwargs):
        """Modify is not supported for Session Tracking resource

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

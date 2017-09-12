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

import time

from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection
from f5.sdk_exception import UnsupportedOperation
from icontrol.exceptions import iControlUnexpectedHTTPError


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

    def refresh(self, **kwargs):
        # If delete() was called, then there is no reason to check if something
        # exists in the loop below.
        deleted = False
        if 'deleted' in self.__dict__ and self.__dict__['deleted'] is True:
            deleted = True
        if deleted:
            return self._refresh(**kwargs)

        # It is possible that even after creation, ASM will not correctly be
        # reporting creation of a Session Tracking Status. Therefore, try several
        # times before we finally fail.
        ex = iControlUnexpectedHTTPError(
            "Failed to refresh the session-tracking-status"
        )
        for _ in range(0, 30):
            try:
                return self._refresh(**kwargs)
            except iControlUnexpectedHTTPError as ex:
                if self._check_exception(ex):
                    continue
                else:
                    raise
        raise ex

    def load(self, **kwargs):
        # If delete() was called, then there is no reason to check if something
        # exists in the loop below.
        deleted = False
        if 'deleted' in self.__dict__ and self.__dict__['deleted'] is True:
            deleted = True
        if deleted:
            return self._load(**kwargs)

        # It is possible that even after creation, ASM will not correctly be
        # reporting creation of a Session Tracking Status. Therefore, try several
        # times before we finally fail.
        ex = iControlUnexpectedHTTPError(
            "Failed to load the session-tracking-status"
        )
        for _ in range(0, 30):
            try:
                return self._load(**kwargs)
            except iControlUnexpectedHTTPError as ex:
                if self._check_exception(ex):
                    continue
                else:
                    raise
        raise ex

    def delete(self, **kwargs):
        # If delete() was called, then there is no reason to check if something
        # exists in the loop below.
        deleted = False
        if 'deleted' in self.__dict__ and self.__dict__['deleted'] is True:
            deleted = True
        if deleted:
            return self._delete(**kwargs)

        # It is possible that even after creation, ASM will not correctly be
        # reporting creation of a Session Tracking Status. Therefore, try several
        # times before we finally fail.
        ex = iControlUnexpectedHTTPError(
            "Failed to delete the session-tracking-status"
        )
        for _ in range(0, 30):
            try:
                return self._delete(**kwargs)
            except iControlUnexpectedHTTPError as ex:
                if self._check_exception(ex):
                    continue
                else:
                    raise
        raise ex

    def _check_exception(self, ex):
        retryable = [
            # Retry potential failure to load due to high policy create/delete
            #
            # There is a possibility that due to a large number of successive
            # create/delete actions on the policies endpoint, that the collection
            # known to the REST API is changing repeatedly.
            #
            # A consequence of this is that the load method will invariably fail
            # intermittently with this error
            #
            # {
            #   "code":404,
            #   "message": "Could not get the Session Awareness Data Point
            #              \'Block All for Username fake2\', No matching record was found.",
            #   "referer":"10.0.2.2",
            #   "restOperationId":9272,
            #   "errorStack":[
            #     "ASMConfigException(error_message:Could not get the Session Awareness Data
            #      Point \'Block All for Username fake2\', No matching record was found.,
            #      error_code:NONEXISTENT_RECORD, internal_error:Failed get on nonexistent
            #      record for SessionAwarenessDataPoint found -- get aborted,
            #      rest_code:REST_NOT_FOUND)"
            #
            'Could not get the Session Awareness Data Point',

            'Could not delete the Session Awareness Data Point'
        ]
        if any(x in str(ex) for x in retryable):
            time.sleep(3)
            return True
        elif 'errorStack' in ex:
            stack = ' '.join(ex['errorStack'])
            if any(x in stack for x in retryable):
                time.sleep(3)
                return True
            else:
                return False
        else:
            return False

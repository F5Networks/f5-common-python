# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
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

import time

from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection
from icontrol.exceptions import iControlUnexpectedHTTPError


class Signatures_s(Collection):
    """BIG-IP® ASM Signatures collection."""
    def __init__(self, asm):
        super(Signatures_s, self).__init__(asm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Signature]
        self._meta_data['attribute_registry'] = {
            'tm:asm:signatures:signaturestate': Signature
        }


class Signature(AsmResource):
    """BIG-IP® ASM Signature resource.

    note:: Only user created signatures can be modified/deleted.
           Default signatures are READ-ONLY
    """
    def __init__(self, signatures_s):
        super(Signature, self).__init__(signatures_s)
        self._meta_data['required_json_kind'] = 'tm:asm:signatures:signaturestate'
        self._meta_data['required_creation_parameters'].update(
            ('attackTypeReference', 'rule')
        )

    def create(self, **kwargs):
        """Custom creation logic to handle edge cases

        This shouldn't be needed, but ASM has a tendency to raise various errors that
        are painful to handle from a customer point-of-view. These errors are especially
        pronounced when doing things concurrently with asm.

        The error itself are described in their exception handler

        To address these failure, we try a number of exception handling cases to catch
        and reliably deal with the error.

        :param kwargs:
        :return:
        """
        ex = iControlUnexpectedHTTPError(
            "Failed to delete the signature"
        )
        for _ in range(0, 30):
            try:
                return self._create(**kwargs)
            except iControlUnexpectedHTTPError as ex:
                if self._check_exception(ex):
                    continue
                else:
                    raise
        raise ex

    def delete(self, **kwargs):
        """Custom deletion logic to handle edge cases

        This shouldn't be needed, but ASM has a tendency to raise various errors that
        are painful to handle from a customer point-of-view. These errors are especially
        pronounced when doing things concurrently with asm.

        The error itself are described in their exception handler

        To address these failure, we try a number of exception handling cases to catch
        and reliably deal with the error.

        :param kwargs:
        :return:
        """
        ex = iControlUnexpectedHTTPError(
            "Failed to delete the signature"
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

    def modify(self, **kwargs):
        ex = iControlUnexpectedHTTPError(
            "Failed to modify the signature"
        )
        for _ in range(0, 30):
            try:
                return self._modify(**kwargs)
            except iControlUnexpectedHTTPError as ex:
                if self._check_exception(ex):
                    continue
                else:
                    raise
        raise ex

    def update(self, **kwargs):
        ex = iControlUnexpectedHTTPError(
            "Failed to delete the signature"
        )
        for _ in range(0, 30):
            try:
                return self._update(**kwargs)
            except iControlUnexpectedHTTPError as ex:
                if self._check_exception(ex):
                    continue
                else:
                    raise
        raise ex

    def _check_exception(self, ex):
        """Check for exceptions in action responses

        In versions of ASM < v12, the REST API is quite unstable and therefore
        needs some additional supporting retries to ensure that actions function
        as expected. In particular versions 11.5.4 and 11.6.0 are affected.

        This method handles checking for various exceptions and allowing the
        given command to retry itself.

        :param ex:
        :return:
        """
        retryable = [
            # iControlUnexpectedHTTPError: 500 Unexpected Error: Internal Server Error ...
            # {
            #   "code": 500,
            #   "message": "Could not add_signature the Attack Signature.  "
            #              "Failed on insert to PLC.NEGSIG_SET_SIGNATURES "
            #              "(DBD::mysql::db do failed: Lock wait timeout exceeded; "
            #              "try restarting transaction)
            #
            'Lock wait timeout exceeded',

            # {
            #   "code": 500,
            #   "message": "DBD::mysql::db do failed: Deadlock found when "
            #              "trying to get lock; try restarting transaction"
            #
            'Deadlock found when',

            # {
            #   "code": 404,
            #   "message": "Could not add_signature the Attack Signature, "
            #              "internal data inconsistency was detected.",
            'internal data inconsistency',
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

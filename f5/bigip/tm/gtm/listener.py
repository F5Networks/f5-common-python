# coding=utf-8
#
#  Copyright 2014-2017 F5 Networks Inc.
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

"""BIG-IP® Global Traffic Manager™ (GTM®) Topology Records module.

REST URI
    ``http://localhost/mgmt/tm/gtm/listener``

GUI Path
    ``DNS --> Delivery : Topology : Records``

REST Kind
    ``tm:gtm:listener:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedOperation
from icontrol.exceptions import iControlUnexpectedHTTPError


class Listeners(Collection):
    """BIG-IP® GTM Listener collection"""
    def __init__(self, gtm):
        super(Listeners, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Listener]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:listener:listenerstate': Listener}


class Listener(Resource):
    """BIG-IP® GTM Listener resource"""
    def __init__(self, listeners):
        super(Listener, self).__init__(listeners)
        self._meta_data['required_json_kind'] = 'tm:gtm:listener:listenerstate'
        self._meta_data['required_creation_parameters'].update(('address',))
        self._meta_data['attribute_registry'] = {
            'tm:gtm:listener:profiles:profilescollectionstate':
                Profiles_s
        }

    def exists(self, **kwargs):
        # This endpoint does not return status 404 if the GET request
        # does not find the resource. On one installation it returned
        # 400, and on another it returned 500
        try:
            result = super(Listener, self).exists(**kwargs)
        except iControlUnexpectedHTTPError as ex:
            if 'listener does not exist' in str(ex):
                return False
            else:
                raise
        return result


class Profiles_s(Collection):
    """BIG-IP® GTM Listener Profile sub-collection"""
    def __init__(self, server):
        super(Profiles_s, self).__init__(server)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:listener:profiles:profilescollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:listener:profiles:profilesstate':
                Profile}


class Profile(Resource):
    """BIG-IP® GTM Listener Profile sub-collection

    Since GTM listener is a wrapper for LTM virtual,
    profile removal and profile attachment should be done via the created
    LTM virtual. Only loading or refresh of profiles is supported.
    Remainder of operations(Create, Update, Modify, Delete) should be done via
    LTM Virtual Server Profiles endpoint.
    """

    def __init__(self, profiles):
        super(Profile, self).__init__(profiles)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:listener:profiles:profilesstate'
        self._meta_data['required_load_parameters'].update(('partition',))

    def create(self, **kwargs):
        """Create is not supported for profile sub-collection

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for profile sub-collection

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

    def update(self, **kwargs):
        """Update is not supported for profile sub-collection

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for profile sub-collection

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )

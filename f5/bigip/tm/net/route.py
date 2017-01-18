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

"""BIG-IP® Network route module.

REST URI
    ``http://localhost/mgmt/tm/net/route``

GUI Path
    ``Network --> Routes``

REST Kind
    ``tm:net:route:*``
"""

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


class Routes(Collection):
    """BIG-IP® network route collection"""
    def __init__(self, net):
        super(Routes, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Route]
        self._meta_data['attribute_registry'] = {
            'tm:net:route:routestate': Route
        }


class Route(Resource, ExclusiveAttributesMixin):
    """BIG-IP® network route resource"""
    def __init__(self, route_s):
        super(Route, self).__init__(route_s)
        self._meta_data['required_json_kind'] = 'tm:net:route:routestate'
        self._meta_data['read_only_attributes'].append('network')
        self._meta_data['required_creation_parameters'].update(
            ('partition', 'name', 'network'))
        self._meta_data['exclusive_attributes'].append(
            ('blackhole', 'gw', 'tmInterface', 'pool'))

    def create(self, **kwargs):
        '''Create a Route on the BIG-IP® and the associated python object.

        One of the following gateways is required when creating the route
        objects: ``blackhole``, ``gw``, ``tmInterface``, ``pool``.

        :params kwargs: keyword arguments passed in from create call
        :raises: KindTypeMismatch
        :raises: MissingRequiredCreationParameter
        :raises: HTTPError
        :returns: Python Route object
        '''
        # We need to check that we have one of the available gateways set
        # when we create.  This isn't exactly the same as
        # required_creation_parameters because it needs to be one of the
        # gateways in the list.
        gateways = ['blackhole', 'gw', 'tmInterface', 'pool']
        kwkeys = list(iterkeys(kwargs))
        if not [k for k in kwkeys if k in gateways]:
            raise MissingRequiredCreationParameter(
                "One of %s gateways is required." % gateways
            )
        return self._create(**kwargs)

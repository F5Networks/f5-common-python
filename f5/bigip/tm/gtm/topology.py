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
    ``http://localhost/mgmt/tm/gtm/topology``

GUI Path
    ``DNS --> GSLB : Topology : Records``

REST Kind
    ``tm:gtm:topology:*``
"""
from distutils.version import LooseVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import InvalidName
from f5.sdk_exception import UnsupportedOperation
from f5.sdk_exception import UnsupportedTmosVersion
from f5.sdk_exception import URICreationCollision


from requests import HTTPError


class Topology_s(Collection):
    """BIG-IP® GTM Topology collection

    Due to an bug where attempts to create/modify/load/delete etc. of this
    resource in 12.0.0 Final, we have disabled this resource for version
    12.0.0
    """
    def __init__(self, gtm):
        super(Topology_s, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Topology]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:topology:topologystate': Topology}
        self.disable_resource_for_version('12.0.0')

    def disable_resource_for_version(self, version):
        tmos_v = self._meta_data['bigip'].tmos_version
        if LooseVersion(tmos_v) == LooseVersion(version):
            error = "There was an attempt to access resource: \n{}\n which " \
                    "is disabled for the device's TMOS version: {}.".\
                format(self._meta_data['uri'], tmos_v)
            raise UnsupportedTmosVersion(error)


class Topology(Resource):
    """BIG-IP® GTM Topology resource"""

    def __init__(self, topology_s):
        super(Topology, self).__init__(topology_s)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:topology:topologystate'

    def _create(self, **kwargs):
        """This method needs to be created due to few bugs in 11.5.4 and 11.6.1


        The issue arises when you attempt to create a Topology Record resource
        and while the operation succeeds BIGIP responds with 404.
        """
        if 'uri' in self._meta_data:
            error = "There was an attempt to assign a new uri to this " \
                    "resource, the _meta_data['uri'] is %s and it should" \
                    " not be changed." % (self._meta_data['uri'])
            raise URICreationCollision(error)
        self._check_exclusive_parameters(**kwargs)
        requests_params = self._handle_requests_params(kwargs)
        self._check_create_parameters(**kwargs)

        # Reduce boolean pairs as specified by the meta_data entry below
        for key1, key2 in self._meta_data['reduction_forcing_pairs']:
            kwargs = self._reduce_boolean_pair(kwargs, key1, key2)

        # Make convenience variable with short names for this method.
        _create_uri = self._meta_data['container']._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']

        # This is a bit hacky but we need to do this so we are able to
        # create a resource inside SDK properly. We also include the
        # scenario where 20x range response occurs just in case this gets
        # fixed in later release.

        try:
            response = session.post(
                _create_uri, json=kwargs, **requests_params)

        except HTTPError as err:
            if err.response.status_code != 404:
                raise
            if err.response.status_code == 404:
                kwargs['uri_as_parts'] = True
                response = session.get(_create_uri, **kwargs)

        # Make new instance of self
        return self._produce_instance(response)

    def create(self, **kwargs):
        """Custom method to implement checking of kwarg['name'] contents.

        ::Warning:
            Be sure to format the gtm topology OID string using the
            following rules:

        1) Use only a single space between each item in the topology string.
        2) Use a fully-pathed name for datacenter, isp, region, and pool
        objects.

        For example:
        "ldns: subnet 11.11.11.0/24 server: datacenter /Common/DC"


        """
        if 'name' in kwargs:
            if 'ldns' not in kwargs['name'] or 'server' not in kwargs['name']:
                raise InvalidName("Topology record name should contain both "
                                  "'ldns', 'server' keywords with their "
                                  "proper arguments")
        return self._create(**kwargs)

    def load(self, **kwargs):
        """Custom method to implement checking of kwarg['name'] contents."""
        if 'name' in kwargs:
            if 'ldns' not in kwargs['name'] or 'server' not in kwargs['name']:
                raise InvalidName("Topology record name should contain both "
                                  "'ldns', 'server' keywords with their "
                                  "proper arguments")
        kwargs['transform_name'] = True

        return self._load(**kwargs)

    def refresh(self, **kwargs):
        """Refresh is not supported for Topology

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the refresh method" %
            self.__class__.__name__
        )

    def modify(self, **patch):
        """Modify is not supported for Topology

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" %
            self.__class__.__name__
        )

    def update(self, **kwargs):
        """Update is not supported for Topology

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" %
            self.__class__.__name__
        )

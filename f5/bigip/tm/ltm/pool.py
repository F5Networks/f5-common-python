# coding=utf-8
#
#  Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager™ (LTM®) pool module.

REST URI
    ``http://localhost/mgmt/tm/ltm/pool``

GUI Path
    ``Local Traffic --> Pools``

REST Kind
    ``tm:ltm:pools:*``
"""

from requests.exceptions import HTTPError

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import F5SDKError


class MemberStateAlwaysRequiredOnUpdate(F5SDKError):
    pass


class Pools(Collection):
    """BIG-IP® LTM pool collection"""
    def __init__(self, ltm):
        super(Pools, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:pool:poolstate': Pool}


class Pool(Resource):
    """BIG-IP® LTM pool resource"""
    def __init__(self, pool_s):
        super(Pool, self).__init__(pool_s)
        self._meta_data['required_json_kind'] = 'tm:ltm:pool:poolstate'
        self._meta_data['attribute_registry'] = {
            'tm:ltm:pool:memberscollectionstate': Members_s
        }


class Members_s(Collection):
    """BIG-IP® LTM pool members sub-collection"""
    def __init__(self, pool):
        super(Members_s, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Members]
        self._meta_data['required_json_kind'] =\
            'tm:ltm:pool:members:memberscollectionstate'
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:pool:members:membersstate': Members}


class Members(Resource):
    """BIG-IP® LTM pool members sub-collection resource"""
    def __init__(self, members_s):
        super(Members, self).__init__(members_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:pool:members:membersstate'
        self._meta_data['required_creation_parameters'].update(('partition',))

    def update(self, **kwargs):
        """Call this to change the configuration of the service on the device.

        This method uses HTTP PUT to alter the service state on the device.

        The attributes of the instance will be packaged as a dictionary.  That
        dictionary will be updated with kwargs.  It is then submitted as JSON
        to the device.  Various edge cases are handled:

        * read-only attributes that are unchangeable are removed
        * If ``fqdn`` is in the kwargs or set as an attribute, removes the
          ``autopopulate`` and ``addressFamily`` keys from it.

        :param state=: state value or :obj:`None` required.
        :param kwargs: keys and associated values to alter on the device
        """

        try:
            state = kwargs.pop('state')
        except KeyError:
            error_message = 'You must supply a value to the "state"' +\
                ' parameter if you do not wish to change the state then' +\
                ' pass "state=None".'
            raise MemberStateAlwaysRequiredOnUpdate(error_message)
        if state is None:
            self.__dict__.pop(u'state', '')
        else:
            self.state = state
        # This is an example implementation of read-only params
        self.__dict__.pop(u'ephemeral', '')
        self.__dict__.pop(u'address', '')
        self._update(**kwargs)

    def exists(self, **kwargs):
        """Check for the existence of the named object on the BigIP

        Sends an HTTP GET to the URI of the named object and if it fails with
        a :exc:~requests.HTTPError` exception it checks the exception for
        status code of 404 and returns :obj:`False` in that case.

        If the GET is successful it must then check the contents of the json
        contained in the response, this is because the "pool/... /members"
        resource provided by the server returns a status code of 200 for
        queries that do not correspond to an existing configuration.  Therefore
        this method checks for the presence of the "address" key in the
        response JSON...  of course, this means that exists depends on an
        unexpected idiosyncrancy of the server, and might break with version
        updates, edge cases, or other unpredictable changes.

        :param kwargs: Keyword arguments required to get objects, "partition"
        and "name" are required

        NOTE: If kwargs has a 'requests_params' key the corresponding dict will
        be passed to the underlying requests.session.get method where it will
        be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!
        :returns: bool -- The objects exists on BigIP or not.
        :raises: :exc:`requests.HTTPError`, Any HTTP error that was not status
                 code 404.
        """
        requests_params = self._handle_requests_params(kwargs)
        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = True
        session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['container']._meta_data['uri']
        kwargs.update(requests_params)
        try:
            response = session.get(base_uri, **kwargs)
        except HTTPError as err:
            if err.response.status_code == 404:
                return False
            else:
                raise
        rdict = response.json()
        if u"address" not in rdict:
            # We can add 'or' conditions to be more restrictive.
            return False
        # Only after all conditions are met...
        return True

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
from f5.sdk_exception import MemberStateModifyUnsupported


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

    @staticmethod
    def _format_monitor_parameter(param):
        """This is a workaround for a known issue ID645289, which affects

        all versions of TMOS at this time.
        """
        if '{' in param and '}':
            tmp = param.strip('}').split('{')
            monitor = ''.join(tmp).rstrip()
            return monitor
        else:
            return param

    def create(self, **kwargs):
        """Custom create method to implement monitor parameter formatting."""
        if 'monitor' in kwargs:
            value = self._format_monitor_parameter(kwargs['monitor'])
            kwargs['monitor'] = value
        return super(Pool, self)._create(**kwargs)

    def update(self, **kwargs):
        """Custom update method to implement monitor parameter formatting."""
        if 'monitor' in kwargs:
            value = self._format_monitor_parameter(kwargs['monitor'])
            kwargs['monitor'] = value
        elif 'monitor' in self.__dict__:
            value = self._format_monitor_parameter(self.__dict__['monitor'])
            self.__dict__['monitor'] = value
        return super(Pool, self)._update(**kwargs)

    def modify(self, **patch):
        """Custom modify method to implement monitor parameter formatting."""
        if 'monitor' in patch:
            value = self._format_monitor_parameter(patch['monitor'])
            patch['monitor'] = value
        return super(Pool, self)._modify(**patch)


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
        self._meta_data['read_only_attributes'].append('ephemeral')
        self._meta_data['read_only_attributes'].append('address')

    def _check_member_parameters(self, **kwargs):
        """See discussion in issue #985."""
        if 'fqdn' in kwargs:
            kwargs['fqdn'].pop('autopopulate', '')
            kwargs['fqdn'].pop('addressFamily', '')
        if 'fqdn' in self.__dict__:
            self.__dict__['fqdn'].pop('autopopulate', '')
            self.__dict__['fqdn'].pop('addressFamily', '')
        if 'state' in kwargs:
            if kwargs['state'] != 'user-up' and kwargs['state'] != \
                    'user-down':
                kwargs.pop('state')
        if 'state' in self.__dict__:
            if self.__dict__['state'] != 'user-up' and self.__dict__['state'] \
                    != 'user-down':
                self.__dict__.pop('state')
        if 'session' in kwargs:
            if kwargs['session'] != 'user-enabled' and kwargs['session'] != \
                    'user-disabled':
                kwargs.pop('session')
        if 'session' in self.__dict__:
            if self.__dict__['session'] != 'user-enabled' and \
                    self.__dict__['session'] != 'user-disabled':
                self.__dict__.pop('session')
        # Until we implement sanity checks for __dict__ this needs to stay here
        self.__dict__.pop('ephemeral', '')
        self.__dict__.pop('address', '')
        return kwargs

    def update(self, **kwargs):
        """Call this to change the configuration of the service on the device.

        This method uses HTTP PUT to alter the service state on the device.

        The attributes of the instance will be packaged as a dictionary.  That
        dictionary will be updated with kwargs.  It is then submitted as JSON
        to the device.  Various edge cases are handled:

        * read-only attributes that are unchangeable are removed
        * If ``fqdn`` is in the kwargs or set as an attribute, removes the
          ``autopopulate`` and ``addressFamily`` keys from it.

        :param kwargs: keys and associated values to alter on the device
        """
        checked = self._check_member_parameters(**kwargs)
        return super(Members, self)._update(**checked)

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
        if "address" not in rdict:
            # We can add 'or' conditions to be more restrictive.
            return False
        # Only after all conditions are met...
        return True

    def _modify(self, **patch):
        """Override modify to check kwargs before request sent to device."""
        if 'state' in patch:
            if patch['state'] != 'user-up' and patch['state'] != 'user-down':
                msg = "The members resource does not support a modify with " \
                      "the value of the 'state' attribute as %s. " \
                      "The accepted values are 'user-up' or " \
                      "'user-down'" % patch['state']
                raise MemberStateModifyUnsupported(msg)
        if 'session' in patch:
            if patch['session'] != 'user-enabled' and patch['session'] != \
                    'user-disabled':
                msg = "The members resource does not support a modify with " \
                      "the value of the 'session' attribute as %s. " \
                      "The accepted values are 'user-enabled' or " \
                      "'user-disabled'" % patch['session']
                raise MemberStateModifyUnsupported(msg)
        super(Members, self)._modify(**patch)

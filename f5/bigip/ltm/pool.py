# Copyright 2014-2016 F5 Networks Inc.
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

"""BigIP Local Traffic Manager (LTM) pool module.

REST URI
    ``http://localhost/mgmt/tm/ltm/pool``

GUI Path
    ``Local Traffic --> Pools``

REST Kind
    ``tm:ltm:pools:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class MemberStateAlwaysRequiredOnUpdate(Exception):
    pass


class Pools(Collection):
    """BigIP LTM pool collection"""
    def __init__(self, ltm):
        super(Pools, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:pool:poolstate': Pool}


class Pool(Resource):
    """BigIP LTM pool resource"""
    def __init__(self, pool_s):
        super(Pool, self).__init__(pool_s)
        self._meta_data['required_json_kind'] = 'tm:ltm:pool:poolstate'
        self._meta_data['attribute_registry'] = {
            'tm:ltm:pool:memberscollectionstate': Members_s
        }


class Members_s(Collection):
    """BigIP LTM pool members sub-collection"""
    def __init__(self, pool):
        super(Members_s, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Members]
        self._meta_data['required_json_kind'] =\
            'tm:ltm:pool:members:memberscollectionstate'
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:pool:members:membersstate': Members}


class Members(Resource):
    """BigIP LTM pool members sub-collection resource"""
    def __init__(self, members_s):
        super(Members, self).__init__(members_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:pool:members:membersstate'
        self._meta_data['required_creation_parameters'].update(('partition',))

    def update(self, **kwargs):
        """Call this to change the configuration of the service on the device.

        This method uses HTTP PUT alter the service state on the device.

        The attributes of the instance will be packaged as a dictionary.  That
        dictionary will be updated with kwargs.  It is then submitted as JSON
        to the device.  Various edge cases are handled:

        * read-only attributes that are unchangeable are removed
        * If ``fqdn`` is in the kwargs or set as an attribute, removes the
          ``autopopulate`` and ``addressFamily`` keys from it if there.

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

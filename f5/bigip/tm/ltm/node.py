# coding=utf-8
#
#  Copyright 2016 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager (LTM) node module.

REST URI
    ``http://localhost/mgmt/tm/ltm/node``

GUI Path
    ``Local Traffic --> Nodes``

REST Kind
    ``tm:ltm:node:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Nodes(Collection):
    """BIG-IP® LTM node collection"""
    def __init__(self, ltm):
        super(Nodes, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Node]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:node:nodestate': Node}


class Node(Resource):
    """BIG-IP® LTM node resource"""
    def __init__(self, nodes):
        super(Node, self).__init__(nodes)
        self._meta_data['required_json_kind'] = 'tm:ltm:node:nodestate'
        self._meta_data['required_creation_parameters'].update(
            ('partition', 'address',)
        )
        self._meta_data['read_only_attributes'].append('ephemeral')
        self._meta_data['read_only_attributes'].append('state')
        self._meta_data['read_only_attributes'].append('address')

    def update(self, **kwargs):
        """Call this to change the configuration of the service on the device.

        This method uses HTTP PUT alter the service state on the device.

        The attributes of the instance will be packaged as a dictionary.  That
        dictionary will be updated with kwargs.  It is then submitted as JSON
        to the device.  Various edge cases are handled:

        * read-only attributes that are unchangeable are removed
        * If ``fqdn`` is in the kwargs or set as an attribute, removes the
          ``autopopulate`` and ``addressFamily`` keys from it if there.

        :param kwargs: keys and associated values to alter on the device

        """
        # Is autopopulate in kwargs?
        if 'fqdn' in kwargs:
            kwargs['fqdn'].pop('autopopulate')
            kwargs['fqdn'].pop('addressFamily')
        if 'fqdn' in self.__dict__:
            self.__dict__['fqdn'].pop('autopopulate')
            self.__dict__['fqdn'].pop('addressFamily')
        return self._update(**kwargs)

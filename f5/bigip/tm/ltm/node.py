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
from f5.sdk_exception import NodeStateModifyUnsupported


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
        checked = self._check_node_parameters(**kwargs)
        return self._update(**checked)

    def _check_node_parameters(self, **kwargs):
        """See discussion in issue #840."""
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

    def _modify(self, **patch):
        """Override modify to check kwargs before request sent to device."""
        if 'state' in patch:
            if patch['state'] not in ['user-up', 'user-down', 'unchecked', 'fqdn-up']:
                msg = "The node resource does not support a modify with the " \
                      "value of the 'state' attribute as %s. The accepted " \
                      "values are 'user-up', 'user-down', 'unchecked', or 'fqdn-up'" \
                      % patch['state']
                raise NodeStateModifyUnsupported(msg)
        if 'session' in patch:
            if patch['session'] not in ['user-enabled', 'user-disabled']:
                msg = "The node resource does not support a modify with the " \
                      "value of the 'session' attribute as %s. " \
                      "The accepted values are 'user-enabled' or " \
                      "'user-disabled'" % patch['session']
                raise NodeStateModifyUnsupported(msg)
        super(Node, self)._modify(**patch)

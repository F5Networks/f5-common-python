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
#

"""BIG-IP® System Software Hotfix sub-module

REST URI
    ``http://localhost/mgmt/tm/sys/software/hotfix``

GUI Path
    ``System --> Software Management --> Hotfix List``

REST Kind
    ``tm:sys:software:hotfix*``
"""

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedOperation


class Hotfix_s(Collection, CommandExecutionMixin):
    """BIG-IP® system software hotfix collection."""
    def __init__(self, software):
        super(Hotfix_s, self).__init__(software)
        self._meta_data['allowed_lazy_attributes'] = [Hotfix]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:software:hotfix:hotfixstate': Hotfix}
        self._meta_data['allowed_commands'].append('install')
        self._meta_data['required_command_parameters'].update((
            'name', 'volume'))


class Hotfix(Resource):
    """BIG-IP® system software hotfix resource."""
    def __init__(self, images):
        super(Hotfix, self).__init__(images)
        self._meta_data['required_json_kind'] = \
            'tm:sys:software:hotfix:hotfixstate'

    def create(self, **kwargs):
        """Create is not supported for hotfix resource.

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method." % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for hotfix resource.

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method." % self.__class__.__name__
        )

    def update(self, **kwargs):
        """Update is not supported for hotfix resource.

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method." % self.__class__.__name__
        )

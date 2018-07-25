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

"""BIG-IP® system host-info module

REST URI
    ``http://localhost/mgmt/tm/sys/service``

GUI Path
    N/A

REST Kind
    ``tm:sys:service:*``
"""

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedMethod


class Service(OrganizingCollection):
    def __init__(self, sys):
        super(Service, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [Tmm]


class Tmm(UnnamedResource,
          CommandExecutionMixin):
    """BIG-IP® system  tmm service

    .. note::
        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, service):
        super(Tmm, self).__init__(service)
        self._meta_data['allowed_commands'].append('restart')
        self._meta_data['minimum_version'] = '13.0.0'
        self._meta_data['required_json_kind'] =\
            'tm:sys:service:servicestate'

    def update(self, **kwargs):
        """Update is not supported

        :raises: UnsupportedMethod
        """
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Update is not supported

        :raises: UnsupportedMethod
        """
        raise UnsupportedMethod(
            "%s does not support the modify method" % self.__class__.__name__
        )

# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.mixins import UnnamedResourceMixin
from f5.bigip.resource import Resource


class Add_To_Trust(UnnamedResourceMixin, ExclusiveAttributesMixin,
                   CommandExecutionMixin, Resource):
    """BIG-IP® Add-To-Trust resource

    Use this object to set or overwrite device trust

    """

    def __init__(self, cm):
        super(Add_To_Trust, self).__init__(cm)
        self._meta_data['exclusive_attributes'].append(
            ('caDevice', 'nonCaDevice'))
        self._meta_data['required_creation_parameters'].update(
            ('device', 'deviceName', 'username', 'password'))
        self._meta_data['required_json_kind'] = \
            'tm:cm:add-to-trust:runstate'


class Remove_From_Trust(UnnamedResourceMixin, CommandExecutionMixin, Resource):
    """BIG-IP®« Remove-From-Trust resource

    Use this object to remove device trust

    .. note::
        This will only remove trust setting on a single BIG-IP®.
        Full trust removal requires that the operation is
        carried out on both target devices

    """

    def __init__(self, cm):
        super(Remove_From_Trust, self).__init__(cm)
        self._meta_data['required_creation_parameters'].update(
            ('deviceName',))
        self._meta_data['required_json_kind'] = \
            'tm:cm:remove-from-trust:runstate'

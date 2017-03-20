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
"""BIG-IP® cluster device submodule

REST URI
    ``http://localhost/mgmt/tm/cm/device/``

GUI Path
    ``Device Management --> Devices``

REST Kind
    ``tm:cm:device:*``
"""


from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Devices(Collection, CommandExecutionMixin):
    """BIG-IP® cluster devices collection.

    """
    def __init__(self, cm):
        super(Devices, self).__init__(cm)
        self._meta_data['allowed_lazy_attributes'] = [Device]
        self._meta_data['attribute_registry'] =\
            {'tm:cm:device:devicestate': Device}
        self._meta_data['allowed_commands'].append('mv')


class Device(Resource):
    """BIG-IP® cluster device object.

    """
    def __init__(self, device_s):
        super(Device, self).__init__(device_s)
        self._meta_data['required_json_kind'] = 'tm:cm:device:devicestate'
        self._meta_data['required_creation_parameters'].update(('partition',))

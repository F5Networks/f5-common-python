# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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

"""iWorkflow® device info module

REST URI
    ``http://localhost/mgmt/shared/identified-devices/config/device-info``

REST Kind
    ``shared:resolver:device-groups:deviceinfostate``
"""

from f5.iworkflow.resource import UnnamedResource


class Device_Info(UnnamedResource):
    """iWorkflow® device-info unnamed resource

        .. note::

        This is an unnamed resource so it has no ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, config):
        super(Device_Info, self).__init__(config)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] = \
            'shared:resolver:device-groups:deviceinfostate'

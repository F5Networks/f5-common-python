# coding=utf-8
#
# Copyright 2015-2017 F5 Networks Inc.
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

"""BIG-IP® Advanced Firewall Manager™ (AFM®) module.

REST URI
    ``http://localhost/mgmt/tm/security/analytics``

GUI Path
    ``Security --> Network Firewall``

REST Kind
    ``tm:security:analytics:*``
"""
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import UnnamedResource


class Analytics(OrganizingCollection):
    """BIG-IP® AFM® Analytics organizing collection."""

    def __init__(self, security):
        super(Analytics, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [Settings]


class Settings(UnnamedResource):
    """BIG-IP® Analytics settings resource"""
    def __init__(self, settings):
        super(Settings, self).__init__(settings)
        self._meta_data['required_json_kind'] = \
            'tm:security:analytics:settings:settingsstate'

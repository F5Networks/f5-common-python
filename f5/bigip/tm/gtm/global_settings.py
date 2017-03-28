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

"""BIG-IP® Global Traffic Manager™ (GTM®)  global-settings submodule.

REST URI
    ``http://localhost/mgmt/tm/gtm/global-settings``

GUI Path
    ``DNS --> Settings --> GSLB``

REST Kind
    ``tm:gtm:global-settings*``
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import UnnamedResource


class Global_Settings(OrganizingCollection):
    """BIG-IP® GTM global-settings organizing collection."""
    def __init__(self, gtm):
        super(Global_Settings, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [
            General,
            Load_Balancing,
            Metrics,
        ]


class General(UnnamedResource):
    """BIG-IP® GTM global-settings general resource."""
    def __init__(self, global_settings):
        super(General, self).__init__(global_settings)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:global-settings:general:generalstate'
        self._meta_data['required_load_parameters'] = set()


class Load_Balancing(UnnamedResource):
    """BIG-IP® GTM global-settings load balancing resource."""
    def __init__(self, global_settings):
        super(Load_Balancing, self).__init__(global_settings)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:global-settings:load-balancing:load-balancingstate'
        self._meta_data['required_load_parameters'] = set()


class Metrics(UnnamedResource):
    """BIG-IP® GTM global-settings metrics resource."""
    def __init__(self, global_settings):
        super(Metrics, self).__init__(global_settings)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:global-settings:metrics:metricsstate'
        self._meta_data['required_load_parameters'] = set()

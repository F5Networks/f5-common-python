# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
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

"""BIG-IP® Global Traffic Manager™ (GTM®) module.

REST URI
    ``http://localhost/mgmt/tm/gtm/``

GUI Path
    ``DNS``

REST Kind
    ``tm:gtm:*``
"""


from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.gtm.datacenter import Datacenters
from f5.bigip.tm.gtm.rule import Rules


class Gtm(OrganizingCollection):
    """BIG-IP® Global Traffic Manager (GTM) organizing collection."""
    def __init__(self, tm):
        super(Gtm, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Datacenters,
            Rules
        ]

# coding=utf-8
#
#  Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager™ (LTM®) pool module.

REST URI
    ``http://localhost/mgmt/tm/ltm/lsn-pool``

GUI Path
    ``Carrier Grade NAT --> LSN Pools``

REST Kind
    ``tm:ltm:lsn-pool:*``
"""

from requests.exceptions import HTTPError

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import MemberStateModifyUnsupported


class LSNPools(Collection):
    """BIG-IP® LTM LSN pool collection"""
    def __init__(self, ltm):
        super(LSNPools, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [LSNPool]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:lsn-pool:lsn-poolstate': LSNPool}

    def _format_resource_name(self):
        """Formats the name of the Collection

        Returns:
            A string representation of the Resource as it should be
            represented when contructing the final URI used to reach that
            Resource.
        """
        return "lsn-pools"


class LSNPool(Resource):
    """BIG-IP® LTM LSN pool resource"""
    def __init__(self, lsnpool_s):
        super(LSNPool, self).__init__(lsnpool_s)
        self._meta_data['required_json_kind'] = 'tm:ltm:lsn-pool:lsn-poolstate'
        self._meta_data['attribute_registry'] = {
            # TODO: need to create these resource
            #       mgmt/tm/ltm/lsn-log-profile
            #
            # 'tm:ltm:lsn-log-profile:lsn-log-profilestate': LSNLogProfile_s,
            # 'tm:sys:log-config:publisher:publisherstate': LogPublisher_s,
        }

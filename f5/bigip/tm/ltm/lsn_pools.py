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

"""BIG-IP® Local Traffic Manager™ (LTM®) LSN pool module.

REST URI
    ``http://localhost/mgmt/tm/ltm/lsn-pool``
    ``http://localhost/mgmt/tm/ltm/lsn-log-profile``

GUI Path
    ``Carrier Grade NAT --> LSN Pools``
    ``Carrier Grade NAT --> Logging Profiles --> LSN``

REST Kind
    ``tm:ltm:lsn-pool:*``
    ``tm:ltm:lsn-log-profile:*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class LSN_Pools(Collection):
    """BIG-IP® LTM LSN pool collection"""
    def __init__(self, ltm):
        super(LSN_Pools, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [LSN_Pool]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:lsn-pool:lsn-poolstate': LSN_Pool}


class LSN_Pool(Resource):
    """BIG-IP® LTM LSN pool resource"""
    def __init__(self, lsnpool_s):
        super(LSN_Pool, self).__init__(lsnpool_s)
        self._meta_data['required_json_kind'] = 'tm:ltm:lsn-pool:lsn-poolstate'
        self._meta_data['allowed_lazy_attributes'] = [LSN_Log_Profile]
        self._meta_data['attribute_registry'] = {
            'tm:ltm:lsn-log-profile:lsn-log-profilestate': LSN_Log_Profile}


class LSN_Log_Profiles(Collection):
    """BIG-IP® LTM LSN pool log profile collection"""
    def __init__(self, profile):
        super(LSN_Log_Profiles, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [LSN_Log_Profile]
        self._meta_data['required_json_kind'] = (
            'tm:ltm:lsn-log-profile:lsn-log-profilecollectionstate')
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:lsn-log-profile:lsn-log-profilestate': LSN_Log_Profile}
        self._meta_data['minimum_version'] = '11.6.0'


class LSN_Log_Profile(Resource):
    """BIG-IP® LTM LSN pool log profile resource"""
    def __init__(self, LSNLogProfile_s):
        super(LSN_Log_Profile, self).__init__(LSNLogProfile_s)
        self._meta_data['required_json_kind'] = (
            'tm:ltm:lsn-log-profile:lsn-log-profilestate')

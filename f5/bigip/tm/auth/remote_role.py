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

"""BIG-IP® auth module

REST URI
    ``http://localhost/mgmt/tm/auth/remote-role``

GUI Path
    ``System --> Users --> Remote Role Groups``

REST Kind
    ``tm:auth:remote-role:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedOperation


class Remote_Role(UnnamedResource):
    """BIG-IP® auth remote role resource"""
    def __init__(self, auth):
        super(Remote_Role, self).__init__(auth)
        self._meta_data['allowed_lazy_attributes'] = [Role_Infos]
        self._meta_data['required_json_kind'] = \
            'tm:auth:remote-role:remote-rolestate'
        self._meta_data['attribute_registry'] = \
            {'tm:auth:remote-role:role-info:role-infocollectionstate': Role_Infos}


class Role_Infos(Collection):
    """BIG-IP® remote role role-info collection"""
    def __init__(self, auth):
        super(Role_Infos, self).__init__(auth)
        self._meta_data['allowed_lazy_attributes'] = [Role_Info]
        self._meta_data['required_json_kind'] = \
            'tm:auth:remote-role:role-info:role-infocollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:auth:remote-role:role-info:role-infostate': Role_Info}


class Role_Info(Resource):
    """BIG-IP® remote role role-info resource"""
    def __init__(self, role_infos):
        super(Role_Info, self).__init__(role_infos)
        self._meta_data['required_json_kind'] = \
            'tm:auth:remote-role:role-info:role-infostate'

    def update(self, **kwargs):
        '''Update is not supported for Auth Remote Role - Role Info Objects

        :raises: UnsupportedOperation
        '''
        raise UnsupportedOperation(
            "%s does not support update, use modify instead" % self.__class__.__name__
        )

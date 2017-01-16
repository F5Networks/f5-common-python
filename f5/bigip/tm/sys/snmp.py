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

"""BIG-IP® SNMP submodule.

REST URI
    ``http://localhost/mgmt/tm/sys/snmp/``

GUI Path
    ``System --> SNMP``

REST Kind
    ``tm:snmp:*``
"""
from distutils.version import LooseVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedOperation


class Snmp(UnnamedResource):
    def __init__(self, sys):
        super(Snmp, self).__init__(sys)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] = 'tm:sys:snmp:snmpstate'
        self._meta_data['allowed_lazy_attributes'] = [
            Communities_s,
            Traps_s,
            Users_s
        ]
        self._meta_data['attribute_registry'] = {
            'tm:sys:snmp:communities:communitiescollectionstate':
                Communities_s,
            'tm:sys:snmp:traps:trapscollectionstate': Traps_s,
            'tm:sys:snmp:users:userscollectionstate': Users_s
        }


class Communities_s(Collection):
    """BIG-IP® SNMP Communities collection."""
    def __init__(self, snmp):
        super(Communities_s, self).__init__(snmp)
        self._meta_data['required_json_kind'] = \
            'tm:sys:snmp:communities:communitiescollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Community]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:snmp:communities:communitiesstate': Community}


class Community(Resource):
    """BIG-IP® SNMP Community resource."""
    def __init__(self, communities_s):
        super(Community, self).__init__(communities_s)
        self._meta_data['required_json_kind'] = \
            'tm:sys:snmp:communities:communitiesstate'
        self._meta_data['required_creation_parameters']\
            .update(('communityName',))


class Traps_s(Collection):
    """BIG-IP® SNMP Traps collection."""
    def __init__(self, snmp):
        super(Traps_s, self).__init__(snmp)
        self._meta_data['required_json_kind'] = \
            'tm:sys:snmp:traps:trapscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Trap]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:snmp:traps:trapsstate': Trap}


class Trap(Resource):
    """BIG-IP® SNMP Trap resource."""
    def __init__(self, traps_s):
        super(Trap, self).__init__(traps_s)
        self._meta_data['required_json_kind'] = \
            'tm:sys:snmp:traps:trapsstate'

    def update(self, **kwargs):
        """Due to a password decryption bug

        we will disable update() method for 12.1.0 and up

        """
        tmos_version = self._meta_data['bigip'].tmos_version
        if LooseVersion(tmos_version) > LooseVersion('12.0.0'):
            msg = "Update() is unsupported for Trap on version %s. " \
                  "Utilize Modify() method instead" % tmos_version
            raise UnsupportedOperation(msg)
        else:
            self._update(**kwargs)


class Users_s(Collection):
    """BIG-IP® SNMP Users collection."""
    def __init__(self, snmp):
        super(Users_s, self).__init__(snmp)
        self._meta_data['required_json_kind'] = \
            'tm:sys:snmp:users:userscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [User]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:snmp:users:usersstate': User}


class User(Resource):
    """BIG-IP® SNMP User resource."""
    def __init__(self, users_s):
        super(User, self).__init__(users_s)
        self._meta_data['required_json_kind'] = \
            'tm:sys:snmp:users:usersstate'
        self._meta_data['required_creation_parameters'] \
            .update(('authProtocol',))

    def update(self, **kwargs):
        """Due to a password decryption bug

        we will disable update() method for 12.1.0 and up

        """
        tmos_version = self._meta_data['bigip'].tmos_version
        if LooseVersion(tmos_version) > LooseVersion('12.0.0'):
            msg = "Update() is unsupported for User on version %s. " \
                  "Utilize Modify() method instead" % tmos_version
            raise UnsupportedOperation(msg)
        else:
            self._update(**kwargs)

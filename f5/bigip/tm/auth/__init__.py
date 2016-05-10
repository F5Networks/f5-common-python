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

"""BIG-IP® auth module

REST URI
    ``http://localhost/mgmt/tm/auth/``

GUI Path
    ``System --> Users``

REST Kind
    ``tm:auth:*``
"""


from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.auth.password_policy import Password_Policy
from f5.bigip.tm.auth.user import Users


class Auth(OrganizingCollection):
    def __init__(self, tm):
        super(Auth, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Password_Policy,
            Users
        ]

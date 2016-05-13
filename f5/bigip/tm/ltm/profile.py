# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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
"""BIG-IP® system config module

REST URI
    ``http://localhost/mgmt/tm/ltm/profile``

GUI Path
    ``System``

REST Kind
    ``tm:sys:*``
"""
import logging

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Profile(OrganizingCollection):
    def __init__(self, ltm):
        super(Profile, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [
            Client_Ssls
        ]


class Client_Ssls(Collection):
    def __init__(self, profile):
        super(Client_Ssls, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [
            Client_Ssl
        ]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:profile:client-ssl:client-sslstate': Client_Ssl}


class Client_Ssl(Resource):
    def __init__(self, client_ssls):
        super(Client_Ssl, self).__init__(client_ssls)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:profile:client-ssl:client-sslstate'

    def create(self, certname, keyname):
        payload = {"name": certname[:-4],
                   "cert": certname,
                   "key": keyname}
        logging.debug(payload)
        return self._create(**payload)

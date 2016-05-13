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
    ``http://localhost/mgmt/tm/sys/config``

GUI Path
    N/A

REST Kind
    ``tm:sys:config:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Crypto(OrganizingCollection):
    def __init__(self, sys):
        super(Crypto, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Certs,
            Keys
        ]


class Keys(Collection):
    def __init__(self, crypto):
        super(Keys, self).__init__(crypto)
        self._meta_data['allowed_lazy_attributes'] = [
            Key
        ]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:crypto:key:keystate': Key}

    def install_key(self, certfilename, keyfilename):
        payload =\
            {"from-local-file": "/var/config/rest/downloads/%s" % keyfilename,
             "command": "install",
             "name": certfilename[:-4]}
        self._meta_data['icr_session'].post(self._meta_data['uri'],
                                            json=payload)


class Key(Resource):
    def __init__(self, keys):
        super(Key, self).__init__(keys)
        self._meta_data['required_json_kind'] = 'tm:sys:crypto:key:keystate'


class Certs(Collection):
    def __init__(self, crypto):
        super(Certs, self).__init__(crypto)
        self._meta_data['allowed_lazy_attributes'] = [
            Cert
        ]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:crypto:cert:certstate': Cert}

    def install_cert(self, certfilename):
        payload =\
            {"from-local-file": "/var/config/rest/downloads/%s" % certfilename,
             "command": "install",
             "name": certfilename[:-4]}
        self._meta_data['icr_session'].post(self._meta_data['uri'],
                                            json=payload)


class Cert(Resource):
    def __init__(self, certs):
        super(Cert, self).__init__(certs)
        self._meta_data['required_json_kind'] = 'tm:sys:crypto:cert:certstate'

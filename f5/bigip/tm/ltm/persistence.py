# coding=utf-8
#
#  Copyright 2016 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager (LTM) persistence module.

REST URI
    ``https://localhost/mgmt/tm/ltm/persistence/``

GUI Path
    ``Local Traffic --> Profiles --> Persistence``

REST Kind
    ``tm:ltm:persistence:*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Persistence(OrganizingCollection):
    """BIG-IP® LTM persistence collection."""
    def __init__(self, ltm):
        super(Persistence, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [
            Cookies,
            Dest_Addrs,
            Hashs,
            Msrdps,
            Sips,
            Source_Addrs,
            Ssls,
            Universals
        ]


class Source_Addrs(Collection):
    """BIG-IP® Source Address persistence collection."""
    def __init__(self, persistence):
        super(Source_Addrs, self).__init__(persistence)
        self._meta_data['allowed_lazy_attributes'] = [Source_Addr]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:persistence:source-addr:source-addrstate': Source_Addr}


class Source_Addr(Resource):
    """BIG-IP® Source Address persistence resource."""
    def __init__(self, source_addrs):
        super(Source_Addr, self).__init__(source_addrs)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:persistence:source-addr:source-addrstate'


class Hashs(Collection):
    """BIG-IP® Hash persistence collection."""
    def __init__(self, persistence):
        super(Hashs, self).__init__(persistence)
        self._meta_data['allowed_lazy_attributes'] = [Hash]
        self._meta_data['attribute_registry'] = {
            'tm:ltm:persistence:hash:hashstate': Hash}


class Hash(Resource):
    """BIG-IP® Hash persistence resource."""
    def __init__(self, hashs):
        super(Hash, self).__init__(hashs)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:persistence:hash:hashstate'


class Sips(Collection):
    """BIG-IP® Sip persistence collection."""
    def __init__(self, persistence):
        super(Sips, self).__init__(persistence)
        self._meta_data['allowed_lazy_attributes'] = [Sip]
        self._meta_data['attribute_registry'] = {
            'tm:ltm:persistence:sip:sipstate': Sip}


class Sip(Resource):
    """BIG-IP® Sip persistence resource."""
    def __init__(self, sips):
        super(Sip, self).__init__(sips)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:persistence:sip:sipstate'


class Ssls(Collection):
    """BIG-IP® SSL persistence collection."""
    def __init__(self, persistence):
        super(Ssls, self).__init__(persistence)
        self._meta_data['allowed_lazy_attributes'] = [Ssl]
        self._meta_data['attribute_registry'] = {
            'tm:ltm:persistence:ssl:sslstate': Ssl}


class Ssl(Resource):
    """BIG-IP® SSL persistence resource."""
    def __init__(self, ssls):
        super(Ssl, self).__init__(ssls)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:persistence:ssl:sslstate'


class Global_Settings(Resource):
    """BIG-IP® Global-Settings persistence resource."""
    def __init__(self, Global_Settings_s):
        super(Global_Settings, self).__init__(Global_Settings_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:persistence:global-settings:global-settingsstate'


class Dest_Addrs(Collection):
    """BIG-IP® Destination Address persistence collection."""
    def __init__(self, persistence):
        super(Dest_Addrs, self).__init__(persistence)
        self._meta_data['allowed_lazy_attributes'] = [Dest_Addr]
        self._meta_data['attribute_registry'] = {
            'tm:ltm:persistence:dest-addr:dest-addrstate': Dest_Addr}


class Dest_Addr(Resource):
    """BIG-IP® Destination Address persistence resource."""
    def __init__(self, dest_addrs):
        super(Dest_Addr, self).__init__(dest_addrs)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:persistence:dest-addr:dest-addrstate'


class Msrdps(Collection):
    """BIG-IP® MS RDP persistence collection."""
    def __init__(self, persistence):
        super(Msrdps, self).__init__(persistence)
        self._meta_data['allowed_lazy_attributes'] = [Msrdp]
        self._meta_data['attribute_registry'] = {
            'tm:ltm:persistence:msrdp:msrdpstate': Msrdp}


class Msrdp(Resource):
    """BIG-IP® MS RDP persistence resource."""
    def __init__(self, msrdps):
        super(Msrdp, self).__init__(msrdps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:persistence:msrdp:msrdpstate'


class Cookies(Collection):
    """BIG-IP® Cookie persistence collection."""
    def __init__(self, persistence):
        super(Cookies, self).__init__(persistence)
        self._meta_data['allowed_lazy_attributes'] = [Cookie]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:persistence:cookie:cookiestate': Cookie}


class Cookie(Resource):
    """BIG-IP® Cookie persistence resource."""
    def __init__(self, cookies):
        super(Cookie, self).__init__(cookies)
        self._meta_data['required_json_kind'] =\
            "tm:ltm:persistence:cookie:cookiestate"


class Universals(Collection):
    """BIG-IP® Universal persistence collection."""
    def __init__(self, persistence):
        super(Universals, self).__init__(persistence)
        self._meta_data['allowed_lazy_attributes'] = [Universal]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:persistence:universal:universalstate': Universal}


class Universal(Resource):
    """BIG-IP® Universal persistence resource."""
    def __init__(self, universals):
        super(Universal, self).__init__(universals)
        self._meta_data['required_json_kind'] =\
            "tm:ltm:persistence:universal:universalstate"

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

"""BIG-IP® Global Traffic Manager™ (GTM®) pool module.

REST URI
    ``http://localhost/mgmt/tm/gtm/wideip``

GUI Path
    ``DNS --> GSLB : Wide IPs``

REST Kind
    ``tm:gtm:pools:*``
"""

from distutils.version import LooseVersion

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Wideips(object):
    def __new__(cls, container):
        tmos_v = container._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            obj = super(Wideips, cls).__new__(Wideipc)
            obj.__init__(container)
            return obj
        else:
            obj = super(Wideips, cls).__new__(Wideipoc)
            obj.__init__(container)
            return obj


class Wideipoc(OrganizingCollection):
    """v12.x GTM WideIP is an OC."""
    def __init__(self, gtm):
        self.__class__.__name__ = 'Wideip'
        super(Wideipoc, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [
            A_s,
            Aaaas,
            Cnames,
            Mxs,
            Naptrs,
            Srvs,
            ]


class A_s(Collection):
    """v12.x BIG-IP® A wideip collection.

        Class name needed changing due to
        'as' being reserved python keyword
    """
    def __init__(self, wideip):
        super(A_s, self).__init__(wideip)
        self._meta_data['allowed_lazy_attributes'] = [A]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:a:astate': A}


class A(Resource):
    """v12.x BIG-IP®A wideip resource"""
    def __init__(self, _as):
        super(A, self).__init__(_as)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:a:astate'


class Aaaas(Collection):
    """v12.x BIG-IP® AAAA wideip collection"""
    def __init__(self, wideip):
        super(Aaaas, self).__init__(wideip)
        self._meta_data['allowed_lazy_attributes'] = [Aaaa]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:aaaa:aaaastate': Aaaa}


class Aaaa(Resource):
    """v12.x BIG-IP® AAAA wideip resource"""
    def __init__(self, aaaas):
        super(Aaaa, self).__init__(aaaas)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:aaaa:aaaastate'


class Cnames(Collection):
    """v12.x BIG-IP® CNAME wideip collection"""
    def __init__(self, wideip):
        super(Cnames, self).__init__(wideip)
        self._meta_data['allowed_lazy_attributes'] = [Cname]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:cname:cnamestate': Cname}


class Cname(Resource):
    """v12.x BIG-IP® CNAME wideip resource"""
    def __init__(self, cnames):
        super(Cname, self).__init__(cnames)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:cname:cnamestate'


class Mxs(Collection):
    """v12.x BIG-IP® MX wideip collection."""
    def __init__(self, wideip):
        super(Mxs, self).__init__(wideip)
        self._meta_data['allowed_lazy_attributes'] = [Mx]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:mx:mxstate': Mx}


class Mx(Resource):
    """v12.x BIG-IP® MX wideip resource"""
    def __init__(self, mxs):
        super(Mx, self).__init__(mxs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:mx:mxstate'


class Naptrs(Collection):
    """v12.x BIG-IP® NAPTR wideip collection"""
    def __init__(self, wideip):
        super(Naptrs, self).__init__(wideip)
        self._meta_data['allowed_lazy_attributes'] = [Naptr]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:naptr:naptrstate': Naptr}


class Naptr(Resource):
    """v12.x BIG-IP® NAPTR wideip resource"""
    def __init__(self, naptrs):
        super(Naptr, self).__init__(naptrs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:naptr:naptrstate'


class Srvs(Collection):
    """v12.x BIG-IP® SRV wideip collection"""
    def __init__(self, wideip):
        super(Srvs, self).__init__(wideip)
        self._meta_data['allowed_lazy_attributes'] = [Srv]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:naptr:srv:srvstate': Srv}


class Srv(Resource):
    """v12.x BIG-IP® SRV wideip resource"""
    def __init__(self, naptrs):
        super(Srv, self).__init__(naptrs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:naptr:srv:srvstate'


class Wideipc(Collection):
    """v11.x BIG-IP® GTM wideip collection"""
    def __init__(self, gtm):
        self.__class__.__name__ = 'Wideips'
        super(Wideipc, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Wideip]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:wideipstate': Wideip}


class Wideip(Resource):
    """v11.x BIG-IP® GTM pool resource"""
    def __init__(self, wideips):
        super(Wideip, self).__init__(wideips)
        self._meta_data['required_json_kind'] = 'tm:gtm:wideip:wideipstate'

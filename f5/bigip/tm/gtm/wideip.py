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

"""BIG-IP® Global Traffic Manager (GTM) WideIp module.

REST URI
    ``http://localhost/mgmt/tm/gtm/wideip``

GUI Path
    ``DNS --> GSLB --> Wide IPs``

REST Kind
    ``tm:gtm:wideip:*``
"""

from distutils.version import LooseVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class WideIps(object):
    """BIG-IP® GTM WideIP factory

    The GTM WideIP factory object is used to provide a consistent user
    experience across the SDK, while supporting the breaking changes in
    the BIG-IP APIs.

    Between the 11.x and 12.x releases of BIG-IP, the REST endpoint for
    WideIP changed from a Collection to an OrganizingCollection. The result
    is that breaking changes occurred in the API.

    This breakage led to a discussion on naming conventions because there
    appeared to be a conflict now. For example, depending on your version,
    only one of the following would work.

    For 11.x,

        tm.gtm.wideips.wideip(name='foo')

    For 12.x,

        tm.gtm.wideips.as.a(name='foo')

    but not both. To stick with a consistent user experience, we decided
    to override the __new__ method to support both examples above. The SDK
    automatically detects which one to use based on the BIG-IP you are
    communicating with.
    """
    def __new__(self, cls, *args, **kwargs):
        version = str(cls._meta_data['bigip']._meta_data['tmos_version'])
        version = LooseVersion(version)
        changed_to_oc = LooseVersion('12.0.0')

        if version < changed_to_oc:
            return WideIpCollection(cls)
        else:
            return WideIpOrganizingCollection(cls)


class WideIpCollection(Collection):
    """BIG-IP® GTM WideIP collection"""
    def __init__(self, gtm):
        self.__class__.__name__ = 'wideips'

        super(WideIpCollection, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [WideIpResource]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:wideipcollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:wideipstate': WideIpResource}


class WideIpResource(Resource):
    """BIG-IP® GTM WideIP sub-collection resource"""
    def __init__(self, wideip_c):
        self.__class__.__name__ = 'wideip'

        super(WideIpResource, self).__init__(wideip_c)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:wideipstate'


class WideIpOrganizingCollection(OrganizingCollection):
    """BIG-IP® GTM WideIP collection"""
    def __init__(self, gtm):
        self.__class__.__name__ = 'wideip'

        super(WideIpOrganizingCollection, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [
            A_s,
            Aaaas,
            Cnames,
            Mxs,
            Naptrs,
            Srvs
        ]


class A_s(Collection):
    """BIG-IP® GTM WideIP A sub-collection."""
    def __init__(self, wideips):
        super(A_s, self).__init__(wideips)
        self._meta_data['allowed_lazy_attributes'] = [A]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:a:astate': A}


class A(Resource):
    """BIG-IP® GTM WideIP A sub-collection resource."""
    def __init__(self, _as):
        super(A, self).__init__(_as)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:a:astate'


class Aaaas(Collection):
    """BIG-IP® GTM WideIP Aaaa sub-collection."""
    def __init__(self, wideips):
        super(Aaaas, self).__init__(wideips)
        self._meta_data['allowed_lazy_attributes'] = [Aaaa]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:aaaa:aaaastate': Aaaa}


class Aaaa(Resource):
    """BIG-IP® GTM WideIP Aaaa sub-collection resource."""
    def __init__(self, aaaas):
        super(Aaaa, self).__init__(aaaas)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:aaaa:aaaastate'


class Cnames(Collection):
    """BIG-IP® GTM WideIP Cnames sub-collection."""
    def __init__(self, wideips):
        super(Cnames, self).__init__(wideips)
        self._meta_data['allowed_lazy_attributes'] = [Cname]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:cname:cnamestate': Cname}


class Cname(Resource):
    """BIG-IP® GTM WideIP Cname sub-collection resource."""
    def __init__(self, cnames):
        super(Cname, self).__init__(cnames)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:cname:cnamestate'


class Mxs(Collection):
    """BIG-IP® GTM WideIP Mxs sub-collection."""
    def __init__(self, wideips):
        super(Mxs, self).__init__(wideips)
        self._meta_data['allowed_lazy_attributes'] = [Mx]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:mx:mxstate': Mx}


class Mx(Resource):
    """BIG-IP® GTM WideIP Mx sub-collection resource."""
    def __init__(self, mxs):
        super(Mx, self).__init__(mxs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:mx:mxstate'


class Naptrs(Collection):
    """BIG-IP® GTM WideIP Naptrs sub-collection."""
    def __init__(self, wideips):
        super(Naptrs, self).__init__(wideips)
        self._meta_data['allowed_lazy_attributes'] = [Naptr]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:naptr:naptrstate': Naptr}


class Naptr(Resource):
    """BIG-IP® GTM WideIP Naptr sub-collection resource."""
    def __init__(self, naptrs):
        super(Naptr, self).__init__(naptrs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:naptr:naptrstate'


class Srvs(Collection):
    """BIG-IP® GTM WideIP Srvs sub-collection."""
    def __init__(self, wideips):
        super(Srvs, self).__init__(wideips)
        self._meta_data['allowed_lazy_attributes'] = [Srv]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:wideip:srv:srvstate': Srv}


class Srv(Resource):
    """BIG-IP® GTM WideIP Srv sub-collection resource."""
    def __init__(self, srvs):
        super(Srv, self).__init__(srvs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:wideip:srv:srvstate'

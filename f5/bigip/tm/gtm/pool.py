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
    ``http://localhost/mgmt/tm/gtm/pool``

GUI Path
    ``DNS --> GSLB : Pools``

REST Kind
    ``tm:gtm:pools:*``
"""

from distutils.version import LooseVersion

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Pools(object):
    """We need to overload __new__ constructor in order to

       account for v12 changes to GTM pools

    """
    def __new__(cls, container):
        tmos_v = container._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            obj = super(Pools, cls).__new__(Poolc)
            obj.__init__(container)
            return obj
        else:
            obj = super(Pools, cls).__new__(Pooloc)
            obj.__init__(container)
            return obj

# Member sub-collections shared between v11.x and v12.x


class Members_s(Collection):
    """BIG-IP® GTM pool members sub-collection

        This class needs to check the instance of
        'pool' object and update relevant meta_data,
        as we are using members sub-collection in both
        v11 and v12 classes for GTM pools.

        It will also add pool type meta_data to utilize in
        Member resource.
    """

    def __init__(self, pool):
        super(Members_s, self).__init__(pool)
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        self._meta_data['allowed_lazy_attributes'] = [Members]
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            self._meta_data['required_json_kind'] = \
                'tm:gtm:pool:members:memberscollectionstate'
            self._meta_data['attribute_registry'] = \
                {'tm:gtm:pool:members:membersstate': Members}
        else:
            if isinstance(pool, A):
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:a:members:memberscollectionstate'
                self._meta_data['attribute_registry'] = \
                    {'tm:gtm:pool:a:members:membersstate': Members}
                self._meta_data['v12_gtm_pool_type'] = 'A'
            if isinstance(pool, Aaaa):
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:aaaa:members:memberscollectionstate'
                self._meta_data['attribute_registry'] = \
                    {'tm:gtm:pool:aaaa:members:membersstate': Members}
                self._meta_data['v12_gtm_pool_type'] = 'AAAA'
            if isinstance(pool, Cname):
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:cname:members:memberscollectionstate'
                self._meta_data['attribute_registry'] = \
                    {'tm:gtm:pool:cname:members:membersstate': Members}
                self._meta_data['v12_gtm_pool_type'] = 'CNAME'
            if isinstance(pool, Mx):
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:mx:members:memberscollectionstate'
                self._meta_data['attribute_registry'] = \
                    {'tm:gtm:pool:mx:members:membersstate': Members}
                self._meta_data['v12_gtm_pool_type'] = 'MX'
            if isinstance(pool, Naptr):
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:naptr:members:memberscollectionstate'
                self._meta_data['attribute_registry'] = \
                    {'tm:gtm:pool:naptr:members:membersstate': Members}
                self._meta_data['v12_gtm_pool_type'] = 'NAPTR'
            if isinstance(pool, Srv):
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:srv:members:memberscollectionstate'
                self._meta_data['attribute_registry'] = \
                    {'tm:gtm:pool:srv:members:membersstate': Members}
                self._meta_data['v12_gtm_pool_type'] = 'SRV'


class Members(Resource):
    """BIG-IP® GTM pool members sub-collection resource"""
    def __init__(self, members_s):
        super(Members, self).__init__(members_s)
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['v12_gtm_pool_type'] = ''
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            self._meta_data['required_json_kind'] = \
                'tm:gtm:pool:members:membersstate'
        else:
            if members_s._meta_data['v12_gtm_pool_type'] == 'A':
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:a:members:membersstate'
            if members_s._meta_data['v12_gtm_pool_type'] == 'AAAA':
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:aaaa:members:membersstate'
            if members_s._meta_data['v12_gtm_pool_type'] == 'CNAME':
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:cname:members:membersstate'
            if members_s._meta_data['v12_gtm_pool_type'] == 'MX':
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:mx:members:membersstate'
            if members_s._meta_data['v12_gtm_pool_type'] == 'NAPTR':
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:naptr:members:membersstate'
            if members_s._meta_data['v12_gtm_pool_type'] == 'SRV':
                self._meta_data['required_json_kind'] = \
                    'tm:gtm:pool:srv:members:membersstate'


# v11.x specific classes


class Poolc(Collection):
    """v11.x BIG-IP® GTM pool collection"""
    def __init__(self, gtm):
        self.__class__.__name__ = 'Pools'
        super(Poolc, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:poolstate': Pool}


class Pool(Resource):
    """v11.x BIG-IP® GTM pool resource"""
    def __init__(self, pool_s):
        super(Pool, self).__init__(pool_s)
        self._meta_data['required_json_kind'] = 'tm:gtm:pool:poolstate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:pool:memberscollectionstate': Members_s
        }

# v12.x specific classes


class Pooloc(OrganizingCollection):
    """v12.x GTM pool is an OC."""
    def __init__(self, gtm):
        self.__class__.__name__ = 'Pool'
        super(Pooloc, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [
            A_s,
            Aaaas,
            Cnames,
            Mxs,
            Naptrs,
            Srvs,
            ]


class A_s(Collection):
    """v12.x BIG-IP® A pool collection.

        Class name needed changing due to
        'as' being reserved python keyword
    """
    def __init__(self, pool):
        super(A_s, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [A]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:a:astate': A}


class A(Resource):
    """v12.x BIG-IP®A pool resource"""
    def __init__(self, _as):
        super(A, self).__init__(_as)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:a:astate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:pool:a:members:memberscollectionstate': Members_s
        }


class Aaaas(Collection):
    """v12.x BIG-IP® AAAA pool collection"""
    def __init__(self, pool):
        super(Aaaas, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Aaaa]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:aaaa:aaaastate': Aaaa}


class Aaaa(Resource):
    """v12.x BIG-IP® AAAA pool resource"""
    def __init__(self, aaaas):
        super(Aaaa, self).__init__(aaaas)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:aaaa:aaaastate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:pool:aaaa:members:memberscollectionstate': Members_s
        }


class Cnames(Collection):
    """v12.x BIG-IP® CNAME pool collection"""
    def __init__(self, pool):
        super(Cnames, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Cname]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:cname:cnamestate': Cname}


class Cname(Resource):
    """v12.x BIG-IP® CNAME pool resource"""
    def __init__(self, cnames):
        super(Cname, self).__init__(cnames)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:cname:cnamestate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:pool:cname:members:memberscollectionstate': Members_s
        }


class Mxs(Collection):
    """v12.x BIG-IP® MX pool collection."""
    def __init__(self, pool):
        super(Mxs, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Mx]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:mx:mxstate': Mx}


class Mx(Resource):
    """v12.x BIG-IP® MX pool resource"""
    def __init__(self, mxs):
        super(Mx, self).__init__(mxs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:mx:mxstate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:pool:mx:members:memberscollectionstate': Members_s
        }


class Naptrs(Collection):
    """v12.x BIG-IP® NAPTR pool collection"""
    def __init__(self, pool):
        super(Naptrs, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Naptr]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:naptr:naptrstate': Naptr}


class Naptr(Resource):
    """v12.x BIG-IP® NAPTR pool resource"""
    def __init__(self, naptrs):
        super(Naptr, self).__init__(naptrs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:naptr:naptrstate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:pool:naptr:members:memberscollectionstate': Members_s
        }


class Srvs(Collection):
    """v12.x BIG-IP® SRV pool collection"""
    def __init__(self, pool):
        super(Srvs, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Srv]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:srv:srvstate': Srv}


class Srv(Resource):
    """v12.x BIG-IP® SRV pool resource"""
    def __init__(self, naptrs):
        super(Srv, self).__init__(naptrs)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:srv:srvstate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:pool:srv:members:memberscollectionstate': Members_s
        }

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
from f5.bigip.resource import ResourceBase
from f5.bigip.resource import Resource


class Pools(ResourceBase):
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


class Pooloc(OrganizingCollection):
    """ v_12 pool is an OC"""
    def __init__(self, gtm):
        self.__class__.__name__ = 'Pool'
        super(Pooloc, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [
            As,
            Aaaas,
            ]


class As(Collection):
    """BIG-IP® A pool collection."""

    def __init__(self, monitor):
        super(As, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [A]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:a:acollectionstate': A}


class A(Resource):
    """BIG-IP® A pool resource."""

    def __init__(self, _as):
        super(A, self).__init__(_as)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:a:astate'


class Aaaas(Collection):
    """BIG-IP® Aaaa pool collection."""

    def __init__(self, monitor):
        super(Aaaas, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Aaaa]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:aaaa:aaaacollectionstate': Aaaa}


class Aaaa(Resource):
    """BIG-IP® Aaaa pool resource."""

    def __init__(self, aaaa):
        super(Aaaa, self).__init__(aaaa)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:aaaa:aaaastate'


class Poolc(Collection):
    """BIG-IP® GTM pool collection in v11.x"""
    def __init__(self, gtm):
        self.__class__.__name__ = 'Pools'
        super(Poolc, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:poolstate': Pool}


class Pool(Resource):
    """BIG-IP® GTM pool resource"""

    def __init__(self, pool_s):
        super(Pool, self).__init__(pool_s)
        self._meta_data['required_json_kind'] = 'tm:ltm:pool:poolstate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:pool:memberscollectionstate': Members_s
        }


class Members_s(Collection):
    """BIG-IP® GTM pool members sub-collection"""

    def __init__(self, pool):
        super(Members_s, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Members]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:members:memberscollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:members:membersstate': Members}


class Members(Resource):
    """BIG-IP® GTM pool members sub-collection resource"""

    def __init__(self, members_s):
        super(Members, self).__init__(members_s)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:members:membersstate'
        self._meta_data['required_creation_parameters'].update(('partition',))
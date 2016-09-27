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
from f5.bigip.resource import URICreationCollision
from requests.exceptions import HTTPError


class Pools(object):
    """BIG-IP® GTM Pool factory

       The GTM Pool factory object is used to provide a consistent user
       experience across the SDK, while supporting the breaking changes in
       the BIG-IP APIs.

       Between the 11.x and 12.x releases of BIG-IP, the REST endpoint for
       Pool changed from a Collection to an OrganizingCollection. The
       result is that breaking changes occurred in the API.

       This breakage led to a discussion on naming conventions because there
       appeared to be a conflict now. For example, depending on your version,
       only one of the following would work.

       For 11.x,

           tm.gtm.pools.pool.load(name='foo')

       For 12.x,

           tm.gtm.pools.a_s.a.load(name='foo')

       but not both. To stick with a consistent user experience, we decided
       to override the __new__ method to support both examples above. The SDK
       automatically detects which one to use based on the BIG-IP you are
       communicating with.
       """
    def __new__(cls, container):
        tmos_v = container._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            return PoolCollection(container)
        else:
            return PoolOrganizingCollection(container)


class Members_s(object):
    """BIG-IP® GTM Members_s factory

        The GTM Members_s factory is used here for code readability
        and maintenance purposes, to allow us to stay in conventions already
        set in this SDK, and at the same time accommodate changes between v11
        and v12 versions of Members_s sub-collection
        """
    def __new__(cls, container):
        tmos_v = container._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            return MembersCollection_v11(container)
        else:
            if isinstance(container, A):
                return MembersCollectionA(container)
            if isinstance(container, Aaaa):
                return MembersCollectionAAAA(container)
            if isinstance(container, Cname):
                return MembersCollectionCname(container)
            if isinstance(container, Mx):
                return MembersCollectionMx(container)
            if isinstance(container, Naptr):
                return MembersCollectionNaptr(container)
            if isinstance(container, Srv):
                return MembersCollectionSrv(container)


class MembersCollection_v11(Collection):
    """v11.x BIG-IP® GTM pool members sub-collection"""
    def __init__(self, pool):
        self.__class__.__name__ = 'Members_s'
        super(MembersCollection_v11, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:members:memberscollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:members:membersstate': Member}


class MembersCollectionA(Collection):
    """v12.x BIG-IP® GTM A pool members sub-collection"""
    def __init__(self, pool):
        self.__class__.__name__ = 'Members_s'
        super(MembersCollectionA, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:a:members:memberscollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:a:members:membersstate': Member}


class MembersCollectionAAAA(Collection):
    """v12.x BIG-IP® GTM AAAA pool members sub-collection"""
    def __init__(self, pool):
        self.__class__.__name__ = 'Members_s'
        super(MembersCollectionAAAA, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:aaaa:members:memberscollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:aaaa:members:membersstate': Member}


class MembersCollectionCname(Collection):
    """v12.x BIG-IP® GTM CNAME pool members sub-collection"""
    def __init__(self, pool):
        self.__class__.__name__ = 'Members_s'
        super(MembersCollectionCname, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:cname:members:memberscollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:cname:members:membersstate': Member}


class MembersCollectionMx(Collection):
    """v12.x BIG-IP® GTM MX pool members sub-collection"""
    def __init__(self, pool):
        self.__class__.__name__ = 'Members_s'
        super(MembersCollectionMx, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:mx:members:memberscollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:mx:members:membersstate': Member}


class MembersCollectionNaptr(Collection):
    """v12.x BIG-IP® GTM NAPTR pool members sub-collection"""
    def __init__(self, pool):
        self.__class__.__name__ = 'Members_s'
        super(MembersCollectionNaptr, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:naptr:members:memberscollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:naptr:members:membersstate': Member}


class MembersCollectionSrv(Collection):
    """v12.x BIG-IP® GTM SRV pool members sub-collection"""
    def __init__(self, pool):
        self.__class__.__name__ = 'Members_s'
        super(MembersCollectionSrv, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:srv:members:memberscollectionstate'
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:pool:srv:members:membersstate': Member}


class Member(object):
    """BIG-IP® GTM Members factory

        The GTM Members factory is used here for code readability
        and maintenance purposes, to allow us to stay in conventions already
        set in this SDK, and at the same time accommodate changes between v11
        and v12 versions of Members resource
        """

    def __new__(cls, container):
        if container._meta_data['required_json_kind'] == \
                'tm:gtm:pool:members:memberscollectionstate':
            return MembersResource_v11(container)
        if container._meta_data['required_json_kind'] == \
                'tm:gtm:pool:a:members:memberscollectionstate':
            return MembersResourceA(container)
        if container._meta_data['required_json_kind'] ==  \
                'tm:gtm:pool:aaaa:members:memberscollectionstate':
            return MembersResourceAAAA(container)
        if container._meta_data['required_json_kind'] == \
                'tm:gtm:pool:cname:members:memberscollectionstate':
            return MembersResourceCname(container)
        if container._meta_data['required_json_kind'] == \
                'tm:gtm:pool:mx:members:memberscollectionstate':
            return MembersResourceMx(container)
        if container._meta_data['required_json_kind'] == \
                'tm:gtm:pool:naptr:members:memberscollectionstate':
            return MembersResourceNaptr(container)
        if container._meta_data['required_json_kind'] == \
                'tm:gtm:pool:srv:members:memberscollectionstate':
            return MembersResourceSrv(container)


class MembersResource_v11(Resource):
    """v11.x BIG-IP® GTM members resource"""
    def __init__(self, members_s):
        self.__class__.__name__ = 'Member'
        super(MembersResource_v11, self).__init__(members_s)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:members:membersstate'


class MembersResourceA(Resource):
    """v12.x BIG-IP® GTM A pool members resource"""
    def __init__(self, members_s):
        self.__class__.__name__ = 'Member'
        super(MembersResourceA, self).__init__(members_s)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:a:members:membersstate'
        self._meta_data['required_creation_parameters'].update(('partition',))

    def create(self, **kwargs):
        """This method needs to be created due to a bug in 12.x

        The issue arises when you attempt to create a members sub-collection
        resource and while the operation succeeds BIGIP responds with 404.

        By requiring partition as argument we have shielded ourselves from
        this issue in 12.0.0, however in v12.1.x the problem occurs, even when
        the partition parameter is submitted. Custom create method is required
        to catch and deal with iControlUnexpectedHTTPError exception.

        Issue is tracked under: ID610441.

        note:: If version is 12.x then we use this method, otherwise we use
               _create method from Resource class as usual.
        """
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) >= LooseVersion('12.1.0'):
            if 'uri' in self._meta_data:
                error = "There was an attempt to assign a new uri to this " \
                        "resource, the _meta_data['uri'] is %s and it should" \
                        " not be changed." % (self._meta_data['uri'])
                raise URICreationCollision(error)
            self._check_exclusive_parameters(**kwargs)
            requests_params = self._handle_requests_params(kwargs)
            self._check_create_parameters(**kwargs)

            # Reduce boolean pairs as specified by the meta_data entry below
            for key1, key2 in self._meta_data['reduction_forcing_pairs']:
                kwargs = self._reduce_boolean_pair(kwargs, key1, key2)

            # Make convenience variable with short names for this method.
            _create_uri = self._meta_data['container']._meta_data['uri']
            session = self._meta_data['bigip']._meta_data['icr_session']
            # This is a bit hacky but we need to do this so we are able to
            # create a resource inside SDK properly. We also include the
            # scenario where 20x range response occurs just in case this gets
            # fixed in later 12.x release.

            try:
                response = session.post(
                    _create_uri, json=kwargs, **requests_params)

            except HTTPError as err:
                if err.response.status_code != 404:
                    raise
                if err.response.status_code == 404:
                    kwargs['uri_as_parts'] = True
                    response = session.get(_create_uri, **kwargs)
                    return self._produce_instance(response)

            # Make new instance of self
            return self._produce_instance(response)

        else:
            return self._create(**kwargs)


class MembersResourceAAAA(Resource):
    """v12.x BIG-IP® GTM AAAA pool members resource"""
    def __init__(self, members_s):
        self.__class__.__name__ = 'Member'
        super(MembersResourceAAAA, self).__init__(members_s)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:aaaa:members:membersstate'
        self._meta_data['required_creation_parameters'].update(('partition',))

    def create(self, **kwargs):
        """This method needs to be created due to a bug in 12.x

        The issue arises when you attempt to create a members sub-collection
        resource and while the operation succeeds BIGIP responds with 404.

        By requiring partition as argument we have shielded ourselves from
        this issue in 12.0.0, however in v12.1.x the problem occurs, even when
        the partition parameter is submitted. Custom create method is required
        to catch and deal with iControlUnexpectedHTTPError exception.

        Issue is tracked under: ID610441.

        note:: If version is 12.x then we use this method, otherwise we use
               _create method from Resource class as usual.
        """
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) >= LooseVersion('12.1.0'):
            if 'uri' in self._meta_data:
                error = "There was an attempt to assign a new uri to this " \
                        "resource, the _meta_data['uri'] is %s and it should" \
                        " not be changed." % (self._meta_data['uri'])
                raise URICreationCollision(error)
            self._check_exclusive_parameters(**kwargs)
            requests_params = self._handle_requests_params(kwargs)
            self._check_create_parameters(**kwargs)

            # Reduce boolean pairs as specified by the meta_data entry below
            for key1, key2 in self._meta_data['reduction_forcing_pairs']:
                kwargs = self._reduce_boolean_pair(kwargs, key1, key2)

            # Make convenience variable with short names for this method.
            _create_uri = self._meta_data['container']._meta_data['uri']
            session = self._meta_data['bigip']._meta_data['icr_session']
            # This is a bit hacky but we need to do this so we are able to
            # create a resource inside SDK properly. We also include the
            # scenario where 20x range response occurs just in case this gets
            # fixed in later 12.x release.

            try:
                response = session.post(
                    _create_uri, json=kwargs, **requests_params)

            except HTTPError as err:
                if err.response.status_code != 404:
                    raise
                if err.response.status_code == 404:
                    kwargs['uri_as_parts'] = True
                    response = session.get(_create_uri, **kwargs)
                    return self._produce_instance(response)

            # Make new instance of self
            return self._produce_instance(response)

        else:
            return self._create(**kwargs)


class MembersResourceCname(Resource):
    """v12.x BIG-IP® GTM CNAME pool members resource"""
    def __init__(self, members_s):
        self.__class__.__name__ = 'Member'
        super(MembersResourceCname, self).__init__(members_s)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:cname:members:membersstate'


class MembersResourceMx(Resource):
    """v12.x BIG-IP® GTM MX pool members resource"""
    def __init__(self, members_s):
        self.__class__.__name__ = 'Member'
        super(MembersResourceMx, self).__init__(members_s)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:mx:members:membersstate'


class MembersResourceNaptr(Resource):
    """v12.x BIG-IP® GTM NAPTR pool members resource"""
    def __init__(self, members_s):
        self.__class__.__name__ = 'Member'
        super(MembersResourceNaptr, self).__init__(members_s)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:naptr:members:membersstate'
        self._meta_data['required_creation_parameters'].update(
            ('flags', 'service'))


class MembersResourceSrv(Resource):
    """v12.x BIG-IP® GTM SRV pool members resource"""
    def __init__(self, members_s):
        self.__class__.__name__ = 'Member'
        super(MembersResourceSrv, self).__init__(members_s)
        self._meta_data['required_json_kind'] = \
            'tm:gtm:pool:srv:members:membersstate'
        self._meta_data['required_creation_parameters'].update(
            ('port',))


class PoolCollection(Collection):
    """v11.x BIG-IP® GTM pool collection"""
    def __init__(self, gtm):
        self.__class__.__name__ = 'Pools'
        super(PoolCollection, self).__init__(gtm)
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


class PoolOrganizingCollection(OrganizingCollection):
    """v12.x GTM pool is an OC."""
    def __init__(self, gtm):
        self.__class__.__name__ = 'Pool'
        super(PoolOrganizingCollection, self).__init__(gtm)
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

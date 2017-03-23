# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from f5.bigip.resource import Collection as BigIpCollection
from f5.bigip.resource import OrganizingCollection as BigIpOrganizingCollection
from f5.bigip.resource import PathElement as BigIpPathElement
from f5.bigip.resource import Resource as BigIpResource
from f5.bigip.resource import ResourceBase as BigIpResourceBase
from f5.bigip.resource import Stats as BigIpStats
from f5.bigip.resource import UnnamedResource as BigIpUnnamedResource


class PathElement(BigIpPathElement):
    """Base class to represent a URI path element that does not contain data.

    The BIG-IP® iControl REST API has URIs that are made up of path components
    that do not return data when they are queried.  This class represents
    those elements and does not support any of the CURDLE methods that
    the other objects do.
    """

    def __init__(self, container):
        super(PathElement, self).__init__(container)
        self._meta_data['minimum_version'] = '2.0.1'


class Resource(BigIpResource, PathElement):
    def __init__(self, container):
        super(Resource, self).__init__(container)
        self._meta_data['required_load_parameters'] = {'uuid', }

    def _assign_stats(self, attrs):
        if self._meta_data['object_has_stats']:
            attrs.append(Stats)
        return attrs


class ResourceBase(BigIpResourceBase, PathElement):
    pass


class OrganizingCollection(BigIpOrganizingCollection, ResourceBase):
    pass


class UnnamedResource(BigIpUnnamedResource, ResourceBase):
    pass


class Collection(BigIpCollection, ResourceBase):
    pass


class Stats(BigIpStats, UnnamedResource):
    pass

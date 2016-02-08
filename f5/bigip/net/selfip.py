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


from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class SelfIPCollection(Collection):
    '''This represents a collection of Self IPs.

    NOTE: The objects in the collection are actually called 'self' in
    iControlREST, but obviously this will cause problems in Python so we
    changed its name to SelfIP. This is why the the SelfIPCollection's uri ends
    in self/ not selfip/.  We override the object's `_meta_data['uri']` to
    account for this.
    '''
    def __init__(self, net):
        super(SelfIPCollection, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [SelfIP]
        self._meta_data['attribute_registry'] =\
            {'tm:net:self:selfstate': SelfIP}
        # Override the URI to have self instead of the constructed selfip
        self._meta_data['uri'] =\
            self._meta_data['container']._meta_data['uri'] + "self/"


class SelfIP(Resource):
    '''This represents a Self IP.

    Use this object to create, refresh, update, delete, and load self ip
    configuration on the BIGIP.  This requires that a :class:`vlan` object
    be present on the system and that object's :attrib:`fullPath` be used
    as the vlan name.

    The address that is used for create is a *<ipaddress>/<netmask>*.  For
    example `192.168.1.1/32`.

    NOTE: The object is actully called 'self' in iControlREST, but obviously
    this will cause problems in Python so we changed its name to SelfIP.
    This is why the the SelfIPCollection's uri ends in self/ not selfip/
    '''
    def __init__(self, selfip_collection):
        super(SelfIP, self).__init__(selfip_collection)
        self._meta_data['required_json_kind'] = 'tm:net:self:selfstate'
        self._meta_data['required_creation_parameters'].update(
            ('address', 'vlan'))

    def create(self, **kwargs):
        self._create(**kwargs)

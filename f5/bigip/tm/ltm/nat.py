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
"""BIG-IP® Local Traffic Manager (LTM) Nat module.

REST URI
    ``http://localhost/mgmt/tm/ltm/nat``

GUI Path
    ``Local Traffic --> Nat``

REST Kind
    ``tm:ltm:nat:*``
"""

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import MissingRequiredCreationParameter


class Nats(Collection):
    """BIG-IP® LTM Nat collection object"""
    def __init__(self, ltm):
        super(Nats, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Nat]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:nat:natstate': Nat}


class Nat(Resource, ExclusiveAttributesMixin):
    """BIG-IP® LTM Nat collection resource"""
    def __init__(self, nat_s):
        super(Nat, self).__init__(nat_s)
        self._meta_data['required_creation_parameters'].update(
            ('originatingAddress', 'translationAddress', 'partition'))
        self._meta_data['required_json_kind'] = 'tm:ltm:nat:natstate'
        self._meta_data['exclusive_attributes'].append(('enable', 'disable'))

    def create(self, **kwargs):
        """Create the resource on the BIG-IP®.

        Uses HTTP POST to the `collection` URI to create a resource associated
        with a new unique URI on the device.

        ..
            If you do a create with inheritedTrafficGroup set to 'false' you
            must also have a trafficGroup.  This pattern generalizes like so:
            If the presence of a param implies an additional required param,
            then simply
            self._meta_data['required_creation_params'].update(IMPLIED),
            before the call to self._create(**kwargs), wherein req params are
            checked.

            We refer to this property as "implied-required parameters" because
            the presence of one parameter, or parameter value (e.g.
            inheritedTrafficGroup), implies that another parameter is required.

        .. note::
            If you are creating with ``inheritedTrafficGroup` set to
            :obj:`False` you just also have a `trafficGroup`.

        :param kwargs: All the key-values needed to create the resource
        :returns: ``self`` - A python object that represents the object's
                  configuration and state on the BIG-IP®.

        """
        itg = kwargs.get('inheritedTrafficGroup', None)
        if itg and itg == 'false':
            self._meta_data['required_creation_parameters'].\
                update(('trafficGroup',))
            try:
                if not kwargs['trafficGroup']:
                    raise MissingRequiredCreationParameter(
                        "trafficGroup must not be falsey but it's: %r"
                        % kwargs['trafficGroup'])
            except KeyError:
                pass
        new_instance = self._create(**kwargs)
        return new_instance

    def update(self, **kwargs):
        # This is an example implementation of read-only params
        stash_translation_address = self.__dict__.pop('translationAddress')
        if 'enabled' in self.__dict__ and 'enabled' not in kwargs:
            kwargs['enabled'] = self.__dict__.pop('enabled')
        elif 'disabled' in self.__dict__ and 'disabled' not in kwargs:
            kwargs['disabled'] = self.__dict__.pop('disabled')
        self._update(**kwargs)
        self.__dict__['translationAddress'] = stash_translation_address

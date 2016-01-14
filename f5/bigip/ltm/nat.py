# Copyright 2014-2016 F5 Networks Inc.
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
from f5.bigip.resource import CRLUD
from f5.bigip.resource import MissingRequiredCreationParameter


class NATCollection(Collection):
    def __init__(self, ltm):
        super(NATCollection, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [NAT]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:nat:natstate': NAT}


class NAT(CRLUD):
    def __init__(self, nat_collection):
        super(NAT, self).__init__(nat_collection)
        self._meta_data['required_creation_parameters'].update(
            ('originatingAddress', 'translationAddress'))
        self._meta_data['allowed_lazy_attributes'] = []
        self._meta_data['required_json_kind'] = 'tm:ltm:nat:natstate'

    def create(self, **kwargs):
        # If you do a create with inheritedTrafficGroup set to 'false' you
        # must also have a trafficGroup.  This pattern generalizes like so:
        # If the presence of a param implies an additional required param, then
        # simply self._meta_data['required_creation_params'].update(IMPLIED),
        # before the call to self._create(**kwargs), wherein req params are
        # checked.
        # We refer to this property as "implied-required parameters" because
        # the presence of one parameter, or parameter value (e.g.
        # inheritedTrafficGroup), implies that another parameter is required.
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
        self._create(**kwargs)
        return self

    def update(self, **kwargs):
        stash_translation_address = self.__dict__.pop('translationAddress')
        try:
            self._update(**kwargs)
        except Exception:
            self.__dict__['translationAddress'] = stash_translation_address

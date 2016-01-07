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
from f5.bigip.resource import CollectionResource
from f5.bigip.resource import CRLUDResource
from f5.bigip.resource import KindTypeMismatch


class NATCollection(CollectionResource):
    def __init__(self, ltm):
        super(NATCollection, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [NAT]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:nat:natstate': NAT}


class NAT(CRLUDResource):
    def __init__(self, nat_collection):
        super(NAT, self).__init__(nat_collection)
        self._meta_data['required_creation_parameters'].update(
            ('name', 'partition', 'originatingAddress', 'translationAddress'))
        self._meta_data['allowed_lazy_attributes'] = []

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
                update('trafficGroup')

        self._create(**kwargs)
        if not self.kind == 'tm:ltm:nat:natstate':
            error_message = "For instances of type 'NAT' the corresponding" +\
                " kind must be 'tm:ltm:nat:natstate' but creation returned" +\
                " JSON with kind: %r" % self.kind
            raise KindTypeMismatch(error_message)
        return self

    def refresh(self):
        self._refresh()

    def load(self, **kwargs):
        self._load(**kwargs)
        return self

    def update(self, **kwargs):
        # Need to implement checking for valid params here.
        self._update(**kwargs)

    def delete(self):
        # Need to implement checking for ? here.
        self._delete()
        # Need to implement correct teardown here.

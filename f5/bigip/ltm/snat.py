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
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import Resource


class RequireOneOf(MissingRequiredCreationParameter):
    pass


class SNATCollection(Collection):
    def __init__(self, ltm):
        super(SNATCollection, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [SNAT]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:snat:snatstate': SNAT}


class SNAT(Resource):
    def __init__(self, snat_collection):
        '''This represents a SNAT.

        "origins" is our first example of a dict attribute, it appears to
        behave as expected.
        '''
        super(SNAT, self).__init__(snat_collection)
        self._meta_data['required_json_kind'] = 'tm:ltm:snat:snatstate'
        self._meta_data['required_creation_parameters'].update(
            ('partition', 'origins'))

    def create(self, **kwargs):
        rcp = self._meta_data['required_creation_parameters']
        required_singles = set(('automap', 'snatpool', 'translation'))
        pre_req_len = len(kwargs.keys())
        if len(rcp - required_singles) != (pre_req_len-1):
            error_message = 'Creation requires one of the provided k,v:\n'
            for req_sing in required_singles:
                try:
                    req_val = kwargs.pop(req_sing)
                except KeyError:
                    req_val = ''
                error_message = error_message + str(req_sing) + ', ' +\
                    str(req_val) + '\n'
            raise RequireOneOf(error_message)
        self._create(**kwargs)
        return self

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
"""BIG-IP® LTM ifile submodule.

REST URI
    ``http://localhost/mgmt/tm/ltm/ifile/``

GUI Path
    ``Local Traffic --> iRules --> iFiles``

REST Kind
    ``tm:ltm:ifile*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Ifiles(Collection):
    def __init__(self, ltm):
        super(Ifiles, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Ifile]
        self._meta_data['attribute_registry'] =\
            {u'tm:ltm:ifile:ifilestate': Ifile}


class Ifile(Resource):
    def __init__(self, ifile_s):
        super(Ifile, self).__init__(ifile_s)
        self._meta_data['required_json_kind'] = u'tm:ltm:ifile:ifilestate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'fileName')
        )

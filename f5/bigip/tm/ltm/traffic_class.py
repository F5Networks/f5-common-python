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

"""BIG-IP Local Traffic Manager (LTM) Traffic Class module.

REST URI
    ``https://localhost/mgmt/tm/ltm/traffic-class``

GUI Path
    ``Local Traffic --> Traffic Class``

REST Kind
    ``tm:ltm:traffic-class:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Traffic_Class_s(Collection):
    """BIG-IP® LTM Traffic Class collection"""
    def __init__(self, ltm):
        super(Traffic_Class_s, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Traffic_Class]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:traffic-class:traffic-classstate': Traffic_Class}


class Traffic_Class(Resource):
    """BIG-IP® LTM Traffic Class Resource"""
    def __init__(self, traffic_class_s):
        super(Traffic_Class, self).__init__(traffic_class_s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:traffic-class:traffic-classstate'
        self._meta_data['required_creation_parameters'].update((
            'classification',))

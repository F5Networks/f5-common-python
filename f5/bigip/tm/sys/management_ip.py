# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

"""BIG-IP® system management IP module

REST URI
    ``http://localhost/mgmt/tm/sys/management-ip``

GUI Path
    ``System --> Platform``

REST Kind
    ``tm:sys:management-ip:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Management_Ips(Collection):
    """BIG-IP® management-ip collection"""
    def __init__(self, sys):
        super(Management_Ips, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [Management_Ip]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:management-ip:management-ipstate': Management_Ip}


class Management_Ip(Resource):
    """BIG-IP® management-ip resource"""
    def __init__(self, Management_Ips):
        super(Management_Ip, self).__init__(Management_Ips)
        self._meta_data['required_json_kind'] = \
            'tm:sys:management-ip:management-ipstate'

    def load(self, **kwargs):
        kwargs['transform_name'] = True
        return self._load(**kwargs)

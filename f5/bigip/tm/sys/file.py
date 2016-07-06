# coding=utf-8
#
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
"""BIG-IP® system file module

REST URI
    ``http://localhost/mgmt/tm/sys/file``

GUI Path
    N/A

REST Kind
    ``tm:sys:file:*``
"""
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class File(OrganizingCollection):
    def __init__(self, sys):
        super(File, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Data_Groups
        ]


class Data_Groups(Collection):
    def __init__(self, File):
        super(Data_Groups, self).__init__(File)
        self._meta_data['allowed_lazy_attributes'] = [Data_Group]
        self._meta_data['required_json_kind'] = \
            u'tm:sys:file:data-group:data-groupcollectionstate'
        self._meta_data['attribute_registry'] =\
            {u'tm:sys:file:data-group:data-groupstate': Data_Group}
        self._meta_data['uri'] = self._meta_data['uri'].replace('_', '-')


class Data_Group(Resource):
    def __init__(self, data_groups):
        super(Data_Group, self).__init__(data_groups)
        self._meta_data['required_json_kind'] =\
            u'tm:sys:file:data-group:data-groupstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'sourcePath', 'type')
        )

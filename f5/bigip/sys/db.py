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

"""BIG-IP® db module

REST URI
    ``http://localhost/mgmt/sys/db/``

GUI Path
    N/A

REST Kind
    ``tm:sys:db:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.bigip.resource import UnsupportedOperation


class Dbs(Collection):
    """BIG-IP® db collection"""
    def __init__(self, sys):
        super(Dbs, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [Db]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:db:dbstate': Db}


class Db(Resource):
    """BIG-IP® db resource

    .. note::
        db objects are read-only.
    """
    def __init__(self, dbs):
        super(Db, self).__init__(dbs)
        self._meta_data['required_json_kind'] = 'tm:sys:db:dbstate'

    def create(self, **kwargs):
        '''Create is not supported for db resources.

        :raises: UnsupportedOperation
        '''
        raise UnsupportedOperation(
            "DB resources doesn't support create, only load and refresh"
        )

    def delete(self, **kwargs):
        '''Delete is not supported for db resources.

        :raises: UnsupportedOperation
        '''
        raise UnsupportedOperation(
            "DB resources doesn't support delete, only load and refresh"
        )

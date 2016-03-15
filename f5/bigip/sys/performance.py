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

"""BigIP system peformance stats module.

REST URI
    ``http://localhost/mgmt/tm/sys/performance``

GUI Path
    ``System --> Users --> Partition List``

REST Kind
    ``tm:sys:performance:*``
"""

from f5.bigip.mixins import UnnamedResourceMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.bigip.resource import UnsupportedOperation


class Performance(Collection):
    """BigIP system performace stats collection"""
    def __init__(self, sys):
        super(Performance, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [All_Stats]
        self._meta_data['uri'] =\
            self._meta_data['container']._meta_data['uri'] + "performance/"

    def get_collection(self):
        '''Performance collections are not proper BigIP collection objects.

        :raises: :exc:`~f5.bigip.resource.UnsupportedOperation`
        '''
        raise UnsupportedOperation(
            "The iControl REST URI mgmt/sys/performance/ does not respond " +
            "GET requests."
        )


class All_Stats(UnnamedResourceMixin, Resource):
    """BigIP system performace stats unnamed resource"""
    def __init__(self, performance):
        super(All_Stats, self).__init__(performance)
        self._meta_data['required_refresh_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:performance:all-stats:all-statsstats'
        self._meta_data['uri'] =\
            self._meta_data['container']._meta_data['uri'] + "all-stats/"

    def update(self, **kwargs):
        '''Update is not supported for statistics.

        :raises: :exc:`~f5.bigip.resource.UnsupportedOperation`
        '''
        raise UnsupportedOperation(
            'Stats do not support create, only load and refresh')

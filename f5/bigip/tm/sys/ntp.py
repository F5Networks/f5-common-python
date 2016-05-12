# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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

"""BIG-IP® system ntp module

REST URI
    ``http://localhost/mgmt/tm/sys/ntp``

GUI Path
    ``System --> Configuration --> Device --> NTP``

REST Kind
    ``tm:sys:ntp:*``
"""

from f5.bigip.mixins import UnnamedResourceMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Ntp(UnnamedResourceMixin, Resource):
    """BIG-IP® system NTP unnamed resource

        .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, sys):
        super(Ntp, self).__init__(sys)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] = 'tm:sys:ntp:ntpstate'
        self._meta_data['attribute_registry'] = {
            'tm:sys:ntp:restrict:restrictcollectionstate': Restricts
        }


class Restricts(Collection):
    """BIG-IP® system NTP restrict sub-collection"""
    def __init__(self, ntp):
        super(Restricts, self).__init__(ntp)
        self._meta_data['allowed_lazy_attributes'] = [Restrict]
        self._meta_data['required_json_kind'] =\
            'tm:sys:ntp:restrict:restrictcollectionstate'
        self._meta_data['attribute_registry'] =\
            {'tm:sys:ntp:restrict:restrictstate': Restrict}


class Restrict(Resource):
    """BIG-IP® system NTP restrict sub-collection resource"""
    def __init__(self, restricts):
        super(Restrict, self).__init__(restricts)
        self._meta_data['required_json_kind'] =\
            'tm:sys:ntp:restrict:restrictstate'

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

"""BIG-IP® system dns module

REST URI
    ``http://localhost/mgmt/tm/sys/dns``

GUI Path
    ``System --> Configuration --> Device --> DNS``

REST Kind
    ``tm:sys:dns:*``
"""

from f5.bigip.resource import UnnamedResource


class Dns(UnnamedResource):
    """BIG-IP® system DNS unnamed resource

        .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, sys):
        super(Dns, self).__init__(sys)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] = 'tm:sys:dns:dnsstate'

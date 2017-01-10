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

"""Directory: net module: fdb.

REST URI
    ``https://localhost/mgmt/tm/net/fdb``

GUI Path
    ``XXX``

REST Kind
    ``tm:net:fdb:*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Fdb(OrganizingCollection):
    """BIG-IP® FDB collection."""
    def __init__(self, net):
        super(Fdb, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Tunnels]
        self._meta_data['icontrol_version'] = '11.5.0'


class Tunnel(Resource):
    """BIG-IP® Tunnel resource."""
    def __init__(self, Tunnels):
        super(Tunnel, self).__init__(Tunnels)
        self._meta_data['required_json_kind'] = "tm:net:fdb:tunnel:tunnelstate"
        # Setting this here to be explicit, even though it is set via
        # the super call from its containing object.
        self._meta_data['icontrol_version'] = '11.5.0'


class Tunnels(Collection):
    """BIG-IP® Tunnels collection."""
    def __init__(self, fdb):
        super(Tunnels, self).__init__(fdb)
        self._meta_data['allowed_lazy_attributes'] = [Tunnel]
        self._meta_data['attribute_registry'] =\
            {'tm:net:fdb:tunnel:tunnelstate': Tunnel}
        # Setting this here to be explicit, even though it is set via
        # the super call from its containing object.
        self._meta_data['icontrol_version'] = '11.5.0'

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

"""BIG-IP® Network tunnels module.

REST URI
    ``http://localhost/mgmt/tm/net/tunnels``

GUI Path
    ``Network --> tunnels``

REST Kind
    ``tm:net:tunnels:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Tunnels_s(Collection):
    """BIG-IP® network tunnels collection"""
    def __init__(self, net):
        super(Tunnels_s, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [
            Gres,
            Tunnels,
            Vxlans,
        ]


class Tunnels(Collection):
    """BIG-IP® network tunnels resource (collection for GRE, Tunnel, VXLANs"""
    def __init__(self, tunnels_s):
        super(Tunnels, self).__init__(tunnels_s)
        self._meta_data['allowed_lazy_attributes'] = [Gres, Tunnel, Vxlans]
        self._meta_data['attribute_registry'] =\
            {'tm:net:tunnels:tunnel:tunnelstate': Tunnel}


class Tunnel(Resource):
    """BIG-IP® tunnels tunnel resource"""
    def __init__(self, tunnels):
        super(Tunnel, self).__init__(tunnels)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:net:tunnels:tunnel:tunnelstate'


class Gres(Collection):
    """BIG-IP® tunnels GRE sub-collection"""
    def __init__(self, tunnels_s):
        super(Gres, self).__init__(tunnels_s)
        self._meta_data['allowed_lazy_attributes'] = [Gre]
        self._meta_data['attribute_registry'] =\
            {'tm:net:tunnels:gre:grestate': Gre}


class Gre(Resource):
    """BIG-IP® tunnels GRE sub-collection resource"""
    def __init__(self, gres):
        super(Gre, self).__init__(gres)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:net:tunnels:gre:grestate'


class Vxlans(Collection):
    """BIG-IP® tunnels VXLAN sub-collection"""
    def __init__(self, tunnels_s):
        super(Vxlans, self).__init__(tunnels_s)
        self._meta_data['allowed_lazy_attributes'] = [Vxlan]
        self._meta_data['attribute_registry'] =\
            {'tm:net:tunnels:vxlan:vxlanstate': Vxlan}


class Vxlan(Resource):
    """BIG-IP® tunnels VXLAN sub-collection resource"""
    def __init__(self, vxlans):
        super(Vxlan, self).__init__(vxlans)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:net:tunnels:vxlan:vxlanstate'

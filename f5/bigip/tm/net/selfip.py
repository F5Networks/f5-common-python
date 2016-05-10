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

"""BIG-IP® Network self-ip module.

.. note::

    Self IPs path does not match their kind or URI because the string ``self``
    causes problems in Python because it is a reserved word.

REST URI
    ``http://localhost/mgmt/tm/net/self``

GUI Path
    ``Network --> Self IPs``

REST Kind
    ``tm:net:self:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Selfips(Collection):
    """BIG-IP® network Self-IP collection

    .. note::

        The objects in the collection are actually called 'self' in
        iControlREST, but obviously this will cause problems in Python so we
        changed its name to Selfip.
    """
    def __init__(self, net):
        super(Selfips, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Selfip]
        self._meta_data['attribute_registry'] =\
            {'tm:net:self:selfstate': Selfip}
        # Override the URI to have self instead of the constructed selfip
        self._meta_data['uri'] =\
            self._meta_data['container']._meta_data['uri'] + "self/"


class Selfip(Resource):
    '''BIG-IP® Self-IP resource

    Use this object to create, refresh, update, delete, and load self ip
    configuration on the BIG-IP®.  This requires that a
    :class:`~f5.BIG-IP.network.vlan.VLAN` object be present on the system and
    that object's :attrib:`fullPath` be used as the VLAN name.

    The address that is used for create is a *<ipaddress>/<netmask>*.  For
    example ``192.168.1.1/32``.

    .. note::

        The object is actually called ``self`` in iControlREST, but obviously
        this will cause problems in Python so we changed its name to
        ``Selfip``.
    '''
    def __init__(self, selfip_s):
        super(Selfip, self).__init__(selfip_s)
        self._meta_data['required_json_kind'] = 'tm:net:self:selfstate'
        self._meta_data['required_creation_parameters'].update(
            ('address', 'vlan'))

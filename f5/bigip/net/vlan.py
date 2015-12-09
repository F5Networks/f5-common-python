"""Classes and functions for configuring vlans on BIG-IP """
# Copyright 2014 F5 Networks Inc.
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

from f5.bigip.rest_collection import log
from f5.bigip.rest_collection import RESTInterfaceCollection
from f5.common import constants as const
from f5.common.logger import Log

from requests.exceptions import HTTPError


class Vlan(RESTInterfaceCollection):
    def __init__(self, bigip):
        self.bigip = bigip
        self.base_uri = bigip.icr_uri + 'net/vlan/'

    @log
    def create(self, name=None, vlanid=None, interface=None,
               folder='Common', description=None, route_domain_id=0):
        """Create a new VLAN.

        Use to create a VLAN configuration for a BIG-IP. By default, the
        VLAN will be configured for the Common folder. Include a folder
        name if the VLAN is for a specific tenant

        :param string name: Name for VLAN object.
        :param int vlanid: ID for VLAN.
        :param interface:
        :param string folder: Optional Folder name.
        :param string description: Optional description for VLAN.
        :param int route_domain_id: Route domain ID as an int.
        :rtype: bool
        :returns: True if VLAN successfully created.
        :raises: HTTPError
        """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if vlanid:
                payload['tag'] = vlanid
                if interface:
                    payload['interfaces'] = [{'name': interface,
                                              'tagged': True}]
            else:
                payload['tag'] = 0
                if interface:
                    payload['interfaces'] = [{'name': interface,
                                              'untagged': True}]
            if description:
                payload['description'] = description

            try:
                self.bigip.icr_session.post(
                    self.base_uri, data=payload,
                    timeout=const.CONNECTION_TIMEOUT)

            except HTTPError as exp:
                if exp.response.status_code == 409:
                    return True
                Log.error('VLAN', exp.response.text)
                raise

            if not folder == 'Common':
                self.bigip.route.add_vlan_to_domain_by_id(
                    name=name, folder=folder,
                    route_domain_id=route_domain_id)

            return True
        return False

    @log
    def get_vlans(self, folder='Common'):
        """Get a list of all VLANs configured for the BIG-IP.

        Use to get a list of all VLANs configured for the BIG-IP.
        VLANs in the Common folder are returned by default. If you pass
        in a folder name, VLANs configured for that folder are returned.

        :param string folder: Optional name of folder. Defaults to Common.
        :return: List of zero or more VLAN objects.
        :raises: HTTPError
        """
        return self._get_items(folder=folder)

    @log
    def get_id(self, name=None, folder='Common'):
        """Get the VLAN ID of a VLAN object.

        Use to get the VLAN ID. VLAN IDs are stored as the 'tag'
        attribute.

        :param string name: Name of VLAN object.
        :param string folder: Optional name of folder. Defaults to Common.
        :return: List of zero or more VLAN objects.
        :raises: HTTPError
        """
        if name:
            return self._get_named_object(name, folder=folder, select='tag')

        return 0

    @log
    def set_id(self, name=None, vlanid=0, folder='Common'):
        """Set VLAN ID

        Sets VLAN ID in tag attribute.

        :param string name: Name of VLAN object.
        :param string folder: Optional name of folder. Defaults to Common.
        :return: List of zero or more VLAN objects.
        :raises: HTTPError
        """
        if name:
            payload = dict()
            payload['tag'] = vlanid
            return self._set_named_object(name, folder=folder, data=payload)

        return False

    @log
    def get_interface(self, name=None, folder='Common'):
        """Get VLAN interface.

        Returns VLAN interface object.

        :param string name: Name of VLAN object.
        :param string folder: Optional name of folder. Defaults to Common.
        :return: VLAN interface or None if not found.
        :raises: HTTPError
        """
        if name:
            interfaces = self._get_items(name, folder, suffix='/interfaces')
            for interface in interfaces:
                return interface['name']

        return None

    @log
    def set_interface(self, name=None, interface='1.1', folder='Common'):
        """Set interface string for VLAN.

        Returns VLAN interface name for a VLAN object.

        :param string name: Name of VLAN object.
        :param string interface: Interface string to set. Defaults to 1.1.
        :param string folder: Optional name of folder. Defaults to Common.
        :return: VLAN interface or None if not found.
        :raises: HTTPError
        """
        if name:
            payload = dict()
            payload['interfaces'] = [{'name': interface, 'untagged': True}]

            return self._set_named_object(name, folder=folder, data=payload)

        return False

    @log
    def get_vlan_name_by_description(self, description=None, folder='Common'):
        """Find a VLAN object that has a given description.

        Returns first VLAN object found with matching description.

        :param string folder: Optional name of folder. Defaults to Common.
        :return: VLAN object, or None if no object is found.
        :raises: HTTPError
        """
        if description:
            vlans = self._get_items(folder, select=None)
            for vlan in vlans:
                if "description" in vlan and \
                        vlan["description"] == description:
                    return vlan

        return None

    @log
    def set_description(self, name=None, description=None, folder='Common'):
        """Get VLAN descritpon

        Returns description defined for a VLAN object.

        :param string name: Name of VLAN object.
        :param string description: Description to set.
        :param string folder: Optional name of folder. Defaults to Common.
        :return bool: True if successful.
        :raises: HTTPError
        """
        if name:
            payload = dict()
            payload['description'] = description
            return self._set_named_object(name, folder=folder, data=payload)

        return False

    @log
    def get_description(self, name=None, folder='Common'):
        """Get description of a VLAN.

        Use this method to get the description of a VLAN object.

        :param string name: Name of VLAN object.
        :param string folder: Optional name of folder. Defaults to Common.
        :return string: Description attribute of the VLAN object.
        :raises: HTTPError
        """
        if name:
            return self._get_named_object(name, folder=folder,
                                          select='description')
        return ""

    @log
    def _in_use(self, name=None, folder=None):
        """Does selfip use vlan? """
        if name:
            selfips = self.bigip.selfip.get_selfips(folder=folder, vlan=name)
            return selfips.length > 0

        return False

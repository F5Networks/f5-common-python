# Copyright 2014-2015 F5 Networks Inc.
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
from f5.bigip.rest_collection import strip_folder_and_prefix
from f5.common import constants as const
from f5.common.logger import Log
from requests.exceptions import HTTPError


class Rule(RESTInterfaceCollection):
    def __init__(self, bigip):
        self.bigip = bigip
        self.base_uri = self.bigip.icr_uri + 'ltm/rule/'

    @log
    def create(self, name='', rule_definition=None, folder='Common'):
        """Create an LTM iRule.

        :param string name: Name for iRule object.
        :param string rule_definition: iRule definition.
        :param string folder: Optional Folder name.
        :rtype: bool
        :returns: True if iRule successfully created.
        :raises: HTTPError
        """
        if name and rule_definition:
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            payload['apiAnonymous'] = rule_definition

            try:
                self.bigip.icr_session.post(
                    self.base_uri, '', '', json=payload,
                    timeout=const.CONNECTION_TIMEOUT)
            except HTTPError as exp:
                if exp.response.status_code == 409:
                    return True
                Log.error(__name__, exp.response.text)
                raise
            return True
        return False

    @log
    def update(self, name=None, rule_definition=None, folder='Common'):
        """Update an LTM iRule.

        :param string name: Name for iRule object.
        :param string rule_definition: iRule definition.
        :param string folder: Optional Folder name.
        :rtype: bool
        :returns: True if iRule successfully updated.
        :raises: HTTPError
        """
        if name and rule_definition:
            payload = dict()
            payload['apiAnonymous'] = rule_definition

            self.bigip.icr_session.put(
                self.base_uri, folder, name, json=payload,
                timeout=const.CONNECTION_TIMEOUT)
            return True
        return False

    # DE note: the generic _get_items in rest_collection presumes that folder
    # needs to be used in both $filter AND passed to icr_session.get.  At least
    # this lib, it must be used ONLY in $filter.  TBD: collapse this API
    @log
    def _get_items(self, folder='Common', name='', suffix='/members',
                   select='name', timeout=const.CONNECTION_TIMEOUT, **kwargs):
        items = []
        params = {
            '$select': select,
            '$filter': 'partition eq ' + folder
        }
        try:
            response = self.bigip.icr_session.get(
                self.base_uri, '', name, params=params,  # set folder to ''
                timeout=timeout, **kwargs)
        except HTTPError as exp:
            if exp.response.status_code == 404:
                return items
            raise

        items = response.json().get('items', [])
        if select:
            for item in items:
                if select in item:
                    items.append(strip_folder_and_prefix(item[select]))

        return items

    @log
    def delete_like(self, match=None, folder='Common'):
        """Delete an LTM iRule matching a string.

        :param string match: Substring to match in iRule name.
        :param string folder: Optional Folder name.
        :rtype: bool
        :returns: True if one or more iRules were deleted.
        :raises: HTTPError
        """
        if not match:
            return False
        items = self._get_items(folder='', name='', select='name,selfLink')
        if items:
            for item in items:
                if item['name'].find(match) > -1:
                    self.delete(item['name'], folder)
            return True
        return False

    @log
    def get_rule(self, name=None, folder='Common'):
        """Get an LTM iRule by name.

        :param string match: Name of iRule to get.
        :param string folder: Optional Folder name.
        :rtype: json
        :returns: JSON representation of iRule if found, otherwise None.
        :raises: HTTPError
        """
        if name:
            return self._get_named_object(name,
                                          folder=folder,
                                          select='apiAnonymous')
        return None

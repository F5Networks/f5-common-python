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

from f5.bigip import exceptions
from f5.bigip.interfaces import icontrol_rest_folder
from f5.bigip.interfaces import log
from f5.common import constants as const
from f5.common.logger import Log

import json


class Rule(object):
    """Class for managing iRules on bigip """
    def __init__(self, bigip):
        self.bigip = bigip

    @icontrol_rest_folder
    @log
    def create(self, name=None, rule_definition=None, folder='Common'):
        """Create rule """
        if name and rule_definition:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            payload['apiAnonymous'] = rule_definition
            request_url = self.bigip.icr_url + '/ltm/rule/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('rule', response.text)
                raise exceptions.RuleCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def update(self, name=None, rule_definition=None, folder='Common'):
        """Update rule """
        if name and rule_definition:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/rule/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['apiAnonymous'] = rule_definition
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('rule', response.text)
                raise exceptions.RuleUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete(self, name=None, folder='Common'):
        """Delete rule """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/rule/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('rule', response.text)
                raise exceptions.RouteDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_like(self, match=None, folder='Common'):
        """Delete rule matching name """
        if not match:
            return False
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/rule/'
        request_url += '?$select=name,selfLink'
        request_filter = 'partition eq ' + folder
        request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for item in response_obj['items']:
                    if item['name'].find(match) > -1:
                        response = self.bigip.icr_session.delete(
                            self.bigip.icr_link(item['selfLink']),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code > 400 and \
                           response.status_code != 404:
                            Log.error('rule', response.text)
                            raise exceptions.RuleDeleteException(
                                response.text)
            return True
        elif response.status_code != 404:
            Log.error('rule', response.text)
            raise exceptions.RuleQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        """Delete rules """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/rule/'
        request_url += '?$select=name,selfLink'
        request_filter = 'partition eq ' + folder
        request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for item in response_obj['items']:
                    if item['name'].startswith(self.OBJ_PREFIX):
                        response = self.bigip.icr_session.delete(
                            self.bigip.icr_link(item['selfLink']),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code > 400 and \
                           response.status_code != 404:
                            Log.error('rule', response.text)
                            raise exceptions.RuleDeleteException(response.text)
            return True
        elif response.status_code != 404:
            Log.error('rule', response.text)
            raise exceptions.RuleQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_rule(self, name=None, folder='Common'):
        """Get rule """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/rule/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=apiAnonymous'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'apiAnonymous' in response_obj:
                    return response_obj['apiAnonymous']
            elif response.status_code != 404:
                Log.error('rule', response.text)
                raise exceptions.RuleQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def exists(self, name=None, folder='Common'):
        """Does rule exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/rule/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('rule', response.text)
            raise exceptions.RuleQueryException(response.text)
        return False

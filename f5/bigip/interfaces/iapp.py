"""Manage application services on BIG-IP using REST interface """
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


class IApp(object):
    """Manage iApps """

    OBJ_PREFIX = 'uuid_'

    def __init__(self, bigip):
        self.bigip = bigip

    @icontrol_rest_folder
    @log
    def service_exists(self, name=None, folder='Common'):
        """Does iApp exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/sys/application/service/'
        request_url += '~' + folder + '~' + name + '.app~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('IAPP', response.text)
        return False

    @icontrol_rest_folder
    @log
    def create_service(self, name=None, folder='Common', service=None):
        """Create iApp """
        service['partition'] = folder
        folder = str(folder).replace('/', '')
        if not self.service_exists(name=name, folder=folder):
            request_url = self.bigip.icr_url + '/sys/application/service/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(service),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 409 or response.status_code == 404:
                return True
            else:
                Log.error('IAPP', response.text)
                raise exceptions.IAppCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_service(self, name=None, folder='Common'):
        """Get application service """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/sys/application/service/'
        request_url += '~' + folder + '~' + name + '.app~' + name

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return json.loads(response.text)
        elif response.status_code != 404:
            Log.error('IAPP', response.text)
            raise exceptions.IAppQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def update_service(self, name, folder='Common', service=None):
        """Update application service """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/sys/application/service/'
        request_url += '~' + folder + '~' + name + '.app~' + name
        response = self.bigip.icr_session.put(
            request_url, data=json.dumps(service),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            # ignore this anomaly for now
            if 'The monitor rule  was not found' in response.text:
                Log.error('IAPP', response.text)
                return True
            Log.error('IAPP', response.text)
            raise exceptions.IAppUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_service(self, name, folder='Common'):
        """Delete application service """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/sys/application/service/'
        request_url += '~' + folder + '~' + name + '.app~' + name
        response = self.bigip.icr_session.delete(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return True
        else:
            Log.error('IAPP', response.text)
            raise exceptions.IAppDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def template_exists(self, name=None, folder='Common'):
        """Does iApp exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/sys/application/template/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('IAPP', response.text)
        return False

    @icontrol_rest_folder
    @log
    def create_template(self, name=None, folder='Common', template=None):
        """Create iApp """
        template['partition'] = folder
        folder = str(folder).replace('/', '')
        if not self.template_exists(name=name, folder=folder):
            request_url = self.bigip.icr_url + '/sys/application/template/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(template),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 409 or response.status_code == 404:
                return True
            else:
                Log.error('IAPP', response.text)
                raise exceptions.IAppCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_template(self, name=None, folder='Common'):
        """Get application template """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/sys/application/template/'
        request_url += '~' + folder + '~' + name

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return json.loads(response.text)
        elif response.status_code != 404:
            Log.error('IAPP', response.text)
            raise exceptions.IAppQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def update_template(self, name, folder='Common', template=None):
        """Update application template """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/sys/application/template/'
        request_url += '~' + folder + '~' + name
        response = self.bigip.icr_session.put(
            request_url, data=json.dumps(template),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('IAPP', response.text)
            raise exceptions.IAppUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_template(self, name, folder='Common'):
        """Delete application template """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/sys/application/template/'
        request_url += '~' + folder + '~' + name
        response = self.bigip.icr_session.delete(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return True
        else:
            Log.error('IAPP', response.text)
            raise exceptions.IAppDeleteException(response.text)
        return False

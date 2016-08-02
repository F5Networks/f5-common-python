# coding=utf-8
#
# Copyright 2015 F5 Networks Inc.
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

"""BIG-IP® Util (util) module

REST URI
    ``http://localhost/mgmt/tm/util/``

GUI Path
    ``Util``

REST Kind
    ``tm:util:*``
"""
import json

from f5.bigip.resource import OrganizingCollection
from f5.bigip.mixins import CommandExecutionMixin


class UtilExecutionException(Exception):
    def __init__(self, error_message):
        self.message = error_message


class Util(OrganizingCollection, CommandExecutionMixin):
    def __init__(self, tm):
        super(Util, self).__init__(tm)

    def bash(self, command):
        payload = {"command": "run", "utilCmdArgs": "-c '%s'" % command}
        response = self._meta_data['icr_session'].post(
            "%s%s" % (self._meta_data['uri'], 'bash'),
            json=payload
        )
        if response.status_code < 400:
            if 'commandResult' in response.content:
                return json.loads(response.content)['commandResult']
            else:
                return response.content
        elif response.status_code < 500:
            raise UtilExecutionException(
                'Client Error: %d %s'
                % (response.status_code, response.content)
            )
        else:
            raise UtilExecutionException(
                'Server Error: %d %s'
                % (response.status_code, response.content)
            )

    def imish(self, command, route_domain=0):
        payload = {
            "command": "run",
            "utilCmdArgs": "-r %d -e '%s'" % (route_domain, command)
        }
        response = self._meta_data['icr_session'].post(
            "%s%s" % (self._meta_data['uri'], 'bash'),
            json=payload
        )
        if response.status_code < 400:
            if 'commandResult' in response.content:
                return json.loads(response.content)['commandResult']
            else:
                return response.content
        elif response.status_code < 500:
            raise UtilExecutionException(
                'Client Error: %d %s'
                % (response.status_code, response.content)
            )
        else:
            raise UtilExecutionException(
                'Server Error: %d %s'
                % (response.status_code, response.content)
            )

    def reboot(self):
        payload = {"command": "run"}
        response = self._meta_data['icr_session'].post(
            "%s%s" % (self._meta_data['uri'], 'reboot'),
            json=payload
        )
        if response.status_code < 400:
            return json.loads(response.content)['commandResult']
        elif response.status_code < 500:
            raise UtilExecutionException(
                'Client Error: %d %s'
                % (response.status_code, response.content)
            )
        else:
            raise UtilExecutionException(
                'Server Error: %d %s'
                % (response.status_code, response.content)
            )

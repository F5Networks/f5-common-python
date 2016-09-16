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
"""BIG-IP® utility module

REST URI
    ``http://localhost/mgmt/tm/util/dig``

GUI Path
    N/A

REST Kind
    ``tm:util:dig:*``
"""

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.resource import UnnamedResource
from f5.utils.util_exceptions import UtilError


class Dig(UnnamedResource, CommandExecutionMixin):
    """BIG-IP® utility command

    .. note::

        This is an unnamed resource so it has no ~Partition~Name pattern
        at the end of its URI.
    """

    def __init__(self, util):
        super(Dig, self).__init__(util)
        self._meta_data['required_command_parameters'].update(('utilCmdArgs',))
        self._meta_data['required_json_kind'] = 'tm:util:dig:runstate'
        self._meta_data['allowed_commands'].append('run')

    def _exec_cmd(self, command, **kwargs):
        kwargs['command'] = command
        self._check_exclusive_parameters(**kwargs)
        requests_params = self._handle_requests_params(kwargs)
        self._check_command_parameters(**kwargs)

        session = self._meta_data['bigip']._meta_data['icr_session']
        response = session.post(
            self._meta_data['uri'], json=kwargs, **requests_params)
        self._local_update(response.json())

        if 'commandResult' in self.__dict__:
            if 'Invalid option' in self.commandResult:
                raise UtilError('%s' % self.commandResult)
            else:
                return self
        else:
            return self

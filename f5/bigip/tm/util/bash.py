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
    ``http://localhost/mgmt/tm/util/bash``

GUI Path
    N/A

REST Kind
    ``tm:util:bash:*``
"""

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UtilError


class Bash(UnnamedResource, CommandExecutionMixin):
    """BIG-IP® utility command

    .. note::

        This is an unnamed resource so it has no ~Partition~Name pattern
        at the end of its URI.
    """

    def __init__(self, util):
        super(Bash, self).__init__(util)
        self._meta_data['required_command_parameters'].update(('utilCmdArgs',))
        self._meta_data['required_json_kind'] = 'tm:util:bash:runstate'
        self._meta_data['allowed_commands'].append('run')

    def exec_cmd(self, command, **kwargs):
        self._is_allowed_command(command)
        self._check_command_parameters(**kwargs)
        if not kwargs['utilCmdArgs'].startswith("-c"):
            raise UtilError(
                'Required format is "-c <bash command and arguments>"')
        return self._exec_cmd(command, **kwargs)

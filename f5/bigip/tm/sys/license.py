# coding=utf-8
#
# Copyright 2018 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""BIG-IP® system license module

REST URI
    ``http://localhost/mgmt/tm/sys/license``

GUI Path
    ``System --> License``

REST Kind
    ``tm:sys:license:*``
"""

from distutils.version import LooseVersion

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.resource import UnnamedResource

from f5.sdk_exception import UnsupportedTmosVersion


class License(UnnamedResource, CommandExecutionMixin):
    """BIG-IP® license unnamed resource"""
    def __init__(self, sys):
        super(License, self).__init__(sys)
        self._meta_data['required_json_kind'] =\
            "tm:sys:license:licensestats"
        self._meta_data['allowed_commands'].append('revoke')

    def exec_cmd(self, command, **kwargs):
        self._is_allowed_command(command)
        self._check_command_parameters(**kwargs)
        if LooseVersion(self._meta_data['bigip']._meta_data['tmos_version']) < LooseVersion('13.1.0'):
            raise UnsupportedTmosVersion('%s is not supported until version 13.1' % command)
        return self._exec_cmd(command, **kwargs)

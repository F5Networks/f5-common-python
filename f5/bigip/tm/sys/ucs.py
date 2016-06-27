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
"""BIG-IP® system config module

REST URI
    ``http://localhost/mgmt/tm/sys/ucs`

GUI Path
    N/A

REST Kind
    ``tm:sys:ucs:*``
"""

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.mixins import UnnamedResourceMixin
from f5.bigip.mixins import InvalidCommand
from f5.bigip.resource import Collection
from f5.bigip.resource import ResourceBase
from requests.exceptions import HTTPError


class Ucs_s(Collection, CommandExecutionMixin):
    """BIG-IP® system UCS collection

        .. note::

    """
    def __init__(self, sys):
        super(Ucs_s, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [Ucs]
        self._meta_data['allowed_commands'].extend(['load', 'save'])
        self._meta_data['attribute_registry'] = \
            {'tm:sys:ucs:ucsstate': Ucs}
        self._meta_data['minimum_version'] = '12.0.0'

    def exec_cmd(self, command, **kwargs):

        cmds = self._meta_data['allowed_commands']

        if command not in self._meta_data['allowed_commands']:
            error_message = "The command value {0} does not exist" \
                            "Valid commands are {1}".format(command, cmds)
            raise InvalidCommand(error_message)

        if command == 'load':
            kwargs['command'] = command
            self._check_exclusive_parameters(**kwargs)
            requests_params = self._handle_requests_params(kwargs)
            self._check_command_parameters(**kwargs)
            session = self._meta_data['bigip']._meta_data['icr_session']
            try:

                session.post(
                    self._meta_data['uri'], json=kwargs, **requests_params)

            except HTTPError as err:
                if err.response.status_code != 502:
                    raise
                return

        else:
            return self._exec_cmd(command, **kwargs)


class Ucs(UnnamedResourceMixin, ResourceBase):
    def __init__(self, Ucs_s):
        super(Ucs, self).__init__(Ucs_s)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] = 'tm:sys:ucs:ucsstate'
        self._meta_data['minimum_version'] = '12.1.0'

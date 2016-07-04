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
from f5.bigip.mixins import InvalidCommand
from f5.bigip.resource import UnnamedResource
from requests.exceptions import HTTPError


class Ucs(UnnamedResource, CommandExecutionMixin):
    """BIG-IP® system UCS resource

        .. note::
        Given the fact that 11.6.0 UCS via rest is
        broken, this feature will be supported in 12.0.0 and above.
        Listing of installed UCS has been fixed in 12.1.0.
        This resource is a collection which does not allow listing
        of each ucs as a resource. 'Items' attribute of the loaded object
        is used to access the list of installed UCS files.

        Caveat:
        Loading UCS will result in ICRD restarting, therefore
        due to ID476518 502 Bad Gateway is generated, this is
        working as intended, at least until some architecture
        changes have been made.


    """
    def __init__(self, sys):
        super(Ucs, self).__init__(sys)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['allowed_commands'].extend(['load', 'save'])
        self._meta_data['required_json_kind'] = ''
        self._meta_data['minimum_version'] = '12.0.0'

    def exec_cmd(self, command, **kwargs):
        """Due to ID476518 the load command need special treatment"""
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

    def load(self, **kwargs):
        """Method to list the UCS on the system

        Since this is only fixed in 12.1.0 and up
        we implemented version check here
        """

        # Check if we are using 12.1.0 version or above when using this method
        self._is_version_supported_method('12.1.0')
        newinst = self._stamp_out_core()
        newinst._refresh(**kwargs)

        return newinst

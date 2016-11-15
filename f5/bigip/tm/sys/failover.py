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
"""BIG-IP® system failover module

REST URI
    ``http://localhost/mgmt/tm/sys/failover``

GUI Path
    ``System --> Failover``

REST Kind
    ``tm:sys:failover:*``
"""

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.resource import UnnamedResource


class Failover(UnnamedResource, CommandExecutionMixin):
    '''BIG-IP® Failover stats and state change.

    The failover object only supports load, update, and refresh because it is
     an unnamed resource.

    To force the unit to standby call the ``update()`` method as follows:

    .. code-block:: python
        f.update(command='run', standby=None, trafficGroup='mytrafficgroup')

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    '''
    def __init__(self, sys):
        super(Failover, self).__init__(sys)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:failover:failoverstats'
        self._meta_data['allowed_commands'].append('run')

    def update(self, **kwargs):
        """Update is not supported for Failover

        :raises: UnsupportedOperation
        """
        raise self.UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )

    def exec_cmd(self, command, **kwargs):
        """Defining custom method to append 'exclusive_attributes'.

        WARNING: Some parameters are hyphenated therefore the function
                 will need to utilize variable keyword argument syntax.
                 This only applies when utilCmdArgs method is not in use.

                 eg.

                 param_set ={'standby':True 'traffic-group': 'traffic-group-1'}
                 bigip.tm.sys.failover.exec_cmd('run', **param_set

        The 'standby' attribute cannot be present with either 'offline'
        or 'online' attribute, whichever is present. Additionally
        we check for existence of same attribute values in
        'offline' and 'online' if both present.


        note:: There is also another way of using failover endpoint,
               by the means of 'utilCmdArgs' attribute, here the syntax
               will resemble more that of the 'tmsh run sys failover...'
               command.
                    eg. exec_cmd('run', utilCmdArgs='standby traffic-group
                    traffic-group-1')

        :: raises InvalidParameterValue
        """

        kwargs = self._reduce_boolean_pair(kwargs, 'online', 'offline')
        if 'offline' in kwargs:
            self._meta_data['exclusive_attributes'].append(
                ('offline', 'standby'))

        if 'online' in kwargs:
            self._meta_data['exclusive_attributes'].append(
                ('online', 'standby'))
        self._is_allowed_command(command)
        self._check_command_parameters(**kwargs)
        return self._exec_cmd(command, **kwargs)

    def toggle_standby(self, **kwargs):
        """Toggle the standby status of a traffic group.

         WARNING: This method which used POST obtains json keys from the device
         that are not available in the response to a GET against the same URI.

         NOTE: This method method is deprecated and probably will be removed,
               usage of exec_cmd is encouraged.
        """

        trafficgroup = kwargs.pop('trafficgroup')
        state = kwargs.pop('state')
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        arguments = {'standby': state, 'traffic-group': trafficgroup}
        return self.exec_cmd('run', **arguments)

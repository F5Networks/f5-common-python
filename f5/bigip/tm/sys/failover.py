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

from f5.bigip.mixins import UnnamedResourceMixin
from f5.bigip.resource import ResourceBase


class Failover(UnnamedResourceMixin, ResourceBase):
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

    def update(self, **kwargs):
        '''Update is not supported for Failover

        :raises: UnsupportedOperation
        '''
        raise self.UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )

    def toggle_standby(self, **kwargs):
        '''Toggle the standby status of a traffic group.

        WARNING: This method which used POST obtains json keys from the device
        that are not available in the response to a GET against the same URI.

        Unique to refresh/GET:
        u"apiRawValues"
        u"selfLink"
        Unique to toggle_standby/POST:
        u"command"
        u"standby"
        u"traffic-group"
        '''
        state = kwargs.pop('state')
        trafficgroup = kwargs.pop('trafficgroup')
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        payload = {u"command": u"run",
                   u"standby": state,
                   u"traffic-group": trafficgroup}
        standby_session = self._meta_data["bigip"]._meta_data["icr_session"]
        uri = self._meta_data['uri']
        response = standby_session.post(uri, json=payload)
        self._local_update(response.json())

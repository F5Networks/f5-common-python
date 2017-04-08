# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

"""
BIG-IP® system daemon log settings module

REST URI
    ``http://localhost/mgmt/tm/sys/daemon-log-settings``

tmsh Path
    ``sys --> daemon-log-settings --> all-properties``

GUI Path
    ``system --> logs --> configuration --> options``

REST Kind
    ``tm:sys:daemon-log-settings:*``
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import UnnamedResource


class Daemon_Log_Settings(OrganizingCollection):
    def __init__(self, sys):
        super(Daemon_Log_Settings, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Clusterd,
            Csyncd,
            Icrd,
            Lind,
            Mcpd,
            Tmm
        ]


class Clusterd(UnnamedResource):
    """BIG-IP® system daemon log settings clusterd resource

    The object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, daemon_log_settings):
        super(Clusterd, self).__init__(daemon_log_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:daemon-log-settings:clusterd:clusterdstate'


class Csyncd(UnnamedResource):
    """BIG-IP® system daemon log settings csyncd resource

    The object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, daemon_log_settings):
        super(Csyncd, self).__init__(daemon_log_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:daemon-log-settings:csyncd:csyncdstate'


class Icrd(UnnamedResource):
    """BIG-IP® system daemon log settings icrd resource

    The object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, daemon_log_settings):
        super(Icrd, self).__init__(daemon_log_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:daemon-log-settings:icrd:icrdstate'


class Lind(UnnamedResource):
    """BIG-IP® system daemon log settings lind resource

    The object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, daemon_log_settings):
        super(Lind, self).__init__(daemon_log_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:daemon-log-settings:lind:lindstate'


class Mcpd(UnnamedResource):
    """BIG-IP® system daemon log settings mcpd resource

    The object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, daemon_log_settings):
        super(Mcpd, self).__init__(daemon_log_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:daemon-log-settings:mcpd:mcpdstate'


class Tmm(UnnamedResource):
    """BIG-IP® system daemon log settings clusterd resource

    The object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, daemon_log_settings):
        super(Tmm, self).__init__(daemon_log_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:daemon-log-settings:tmm:tmmstate'

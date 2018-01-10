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
"""BIG-IP® system log-config module

REST URI
    ``http://localhost/mgmt/tm/sys/log-config``

GUI Path
    N/A

REST Kind
    ``tm:sys:log-config:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedMethod


class Log_Config(OrganizingCollection):
    def __init__(self, sys):
        super(Log_Config, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Destination,
            Filters,
            Publishers]


class Destination(OrganizingCollection):
    def __init__(self, Log_Config):
        super(Destination, self).__init__(Log_Config)
        self._meta_data['allowed_lazy_attributes'] = [
            Alertds,
            Arcsights,
            Ipfixs,
            Local_Databases,
            Local_Syslogs,
            Management_Ports,
            Remote_High_Speed_Logs,
            Remote_Syslogs,
            Splunks]


class Alertds(Collection):
    def __init__(self, Destination):
        super(Alertds, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Alertd]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:log-config:destination:alertd:alertdstate': Alertd}


class Alertd(Resource):
    def __init__(self, alertds):
        super(Alertd, self).__init__(alertds)
        self._meta_data['required_json_kind'] =\
            'tm:sys:log-config:destination:alertd:alertdstate'

    def create(self, **kwargs):
        '''Create is not supported for Alertd

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__)

    def delete(self, **kwargs):
        '''Delete is not supported for Alertd

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the delete method" % self.__class__.__name__)


class Arcsights(Collection):
    def __init__(self, Destination):
        super(Arcsights, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Arcsight]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:log-config:destination:arcsight:arcsightstate': Arcsight}


class Arcsight(Resource):
    def __init__(self, arcsights):
        super(Arcsight, self).__init__(arcsights)
        self._meta_data['required_json_kind'] =\
            'tm:sys:log-config:destination:arcsight:arcsightstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'forwardTo'))


class Ipfixs(Collection):
    def __init__(self, Destination):
        super(Ipfixs, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Ipfix]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:log-config:destination:ipfix:ipfixstate': Ipfix}


class Ipfix(Resource):
    def __init__(self, ipfixs):
        super(Ipfix, self).__init__(ipfixs)
        self._meta_data['required_json_kind'] =\
            'tm:sys:log-config:destination:ipfix:ipfixstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'poolName'))


class Local_Databases(Collection):
    def __init__(self, Destination):
        super(Local_Databases, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Local_Database]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:log-config:destination:local-database:local-databasestate': Local_Database}


class Local_Database(Resource):
    def __init__(self, local_databases):
        super(Local_Database, self).__init__(local_databases)
        self._meta_data['required_json_kind'] =\
            'tm:sys:log-config:destination:local-database:local-databasestate'

    def create(self, **kwargs):
        '''Create is not supported for Local_Database

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__)

    def delete(self, **kwargs):
        '''Delete is not supported for Local_Database

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the delete method" % self.__class__.__name__)


class Local_Syslogs(Collection):
    def __init__(self, Destination):
        super(Local_Syslogs, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Local_Syslog]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:log-config:destination:local-syslog:local-syslogstate': Local_Syslog}


class Local_Syslog(Resource):
    def __init__(self, local_syslogs):
        super(Local_Syslog, self).__init__(local_syslogs)
        self._meta_data['required_json_kind'] = \
            'tm:sys:log-config:destination:local-syslog:local-syslogstate'

    def create(self, **kwargs):
        '''Create is not supported for Local_Syslog

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__)

    def delete(self, **kwargs):
        '''Delete is not supported for Local_Syslog

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the delete method" % self.__class__.__name__)


class Management_Ports(Collection):
    def __init__(self, Destination):
        super(Management_Ports, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Management_Port]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:log-config:destination:management-port:management-portstate': Management_Port}


class Management_Port(Resource):
    def __init__(self, management_ports):
        super(Management_Port, self).__init__(management_ports)
        self._meta_data['required_json_kind'] =\
            'tm:sys:log-config:destination:management-port:management-portstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'ipAddress', 'port'))


class Remote_High_Speed_Logs(Collection):
    def __init__(self, Destination):
        super(Remote_High_Speed_Logs, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Remote_High_Speed_Log]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:log-config:destination:remote-high-speed-log:remote-high-speed-logstate': Remote_High_Speed_Log}


class Remote_High_Speed_Log(Resource):
    def __init__(self, remote_high_speed_logs):
        super(Remote_High_Speed_Log, self).__init__(remote_high_speed_logs)
        self._meta_data['required_json_kind'] = \
            'tm:sys:log-config:destination:remote-high-speed-log:remote-high-speed-logstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'poolName'))


class Remote_Syslogs(Collection):
    def __init__(self, Destination):
        super(Remote_Syslogs, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Remote_Syslog]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:log-config:destination:remote-syslog:remote-syslogstate': Remote_Syslog}


class Remote_Syslog(Resource):
    def __init__(self, remote_syslogs):
        super(Remote_Syslog, self).__init__(remote_syslogs)
        self._meta_data['required_json_kind'] = \
            'tm:sys:log-config:destination:remote-syslog:remote-syslogstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'remoteHighSpeedLog'))


class Splunks(Collection):
    def __init__(self, Destination):
        super(Splunks, self).__init__(Destination)
        self._meta_data['allowed_lazy_attributes'] = [Splunk]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:log-config:destination:splunk:splunkstate': Splunk}


class Splunk(Resource):
    def __init__(self, splunks):
        super(Splunk, self).__init__(splunks)
        self._meta_data['required_json_kind'] = \
            'tm:sys:log-config:destination:splunk:splunkstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'forwardTo'))


class Filters(Collection):
    def __init__(self, Log_Config):
        super(Filters, self).__init__(Log_Config)
        self._meta_data['allowed_lazy_attributes'] = [Filter]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:log-config:filter:filterstate': Filter}


class Filter(Resource):
    def __init__(self, filters):
        super(Filter, self).__init__(filters)
        self._meta_data['required_json_kind'] =\
            'tm:sys:log-config:filter:filterstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'publisher'))


class Publishers(Collection):
    def __init__(self, Log_Config):
        super(Publishers, self).__init__(Log_Config)
        self._meta_data['allowed_lazy_attributes'] = [Publisher]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:log-config:publisher:publisherstate': Publisher}


class Publisher(Resource):
    def __init__(self, publishers):
        super(Publisher, self).__init__(publishers)
        self._meta_data['required_json_kind'] =\
            'tm:sys:log-config:publisher:publisherstate'
        self._meta_data['required_creation_parameters'].update(
            ('name',))

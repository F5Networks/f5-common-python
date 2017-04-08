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
"""BIG-IP® system icall module

REST URI
    ``http://localhost/mgmt/tm/sys/icall``

GUI Path
    N/A

REST Kind
    ``tm:sys:icall:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Icall(OrganizingCollection):
    def __init__(self, sys):
        super(Icall, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Handler,
            Istats_Triggers,
            Scripts]


class Handler(OrganizingCollection):
    def __init__(self, Icall):
        super(Handler, self).__init__(Icall)
        self._meta_data['allowed_lazy_attributes'] = [
            Periodics,
            Perpetuals,
            Triggered_s]


class Periodics(Collection):
    def __init__(self, Handler):
        super(Periodics, self).__init__(Handler)
        self._meta_data['allowed_lazy_attributes'] = [Periodic]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:icall:handler:periodic:periodicstate': Periodic}


class Periodic(Resource):
    def __init__(self, Periodics):
        super(Periodic, self).__init__(Periodics)
        self._meta_data['required_json_kind'] = \
            'tm:sys:icall:handler:periodic:periodicstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'script', 'interval'))


class Perpetuals(Collection):
    def __init__(self, Handler):
        super(Perpetuals, self).__init__(Handler)
        self._meta_data['allowed_lazy_attributes'] = [Perpetual]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:icall:handler:perpetual:perpetualstate': Perpetual}


class Perpetual(Resource):
    def __init__(self, Perpetuals):
        super(Perpetual, self).__init__(Perpetuals)
        self._meta_data['required_json_kind'] = \
            'tm:sys:icall:handler:perpetual:perpetualstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'script'))


class Triggered_s(Collection):
    def __init__(self, Handler):
        super(Triggered_s, self).__init__(Handler)
        self._meta_data['allowed_lazy_attributes'] = [Triggered]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:icall:handler:triggered:triggeredstate': Triggered}


class Triggered(Resource):
    def __init__(self, Triggered_s):
        super(Triggered, self).__init__(Triggered_s)
        self._meta_data['required_json_kind'] = \
            'tm:sys:icall:handler:triggered:triggeredstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'script'))


class Scripts(Collection):
    def __init__(self, Icall):
        super(Scripts, self).__init__(Icall)
        self._meta_data['allowed_lazy_attributes'] = [Script]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:icall:script:scriptstate': Script}


class Script(Resource):
    def __init__(self, Scripts):
        super(Script, self).__init__(Scripts)
        self._meta_data['required_json_kind'] = \
            'tm:sys:icall:script:scriptstate'
        self._meta_data['required_creation_parameters'].update(
            ('name',))


class Istats_Triggers(Collection):
    def __init__(self, Icall):
        super(Istats_Triggers, self).__init__(Icall)
        self._meta_data['allowed_lazy_attributes'] = [Istats_Trigger]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:icall:istats-trigger:istats-triggerstate': Istats_Trigger}


class Istats_Trigger(Resource):
    def __init__(self, Istats_Triggers):
        super(Istats_Trigger, self).__init__(Istats_Triggers)
        self._meta_data['required_json_kind'] = \
            'tm:sys:icall:istats-trigger:istats-triggerstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'eventName', 'istatsKey'))

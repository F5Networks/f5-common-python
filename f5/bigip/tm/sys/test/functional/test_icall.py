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

import pytest

from f5.sdk_exception import MissingRequiredCreationParameter
from icontrol.exceptions import iControlUnexpectedHTTPError

from requests.exceptions import HTTPError

ICALLSCRIPT1 = '''puts "hello world."'''
ICALLSCRIPT2 = '''puts "goodbye world."'''


def delete_script(mgmt_root, name, partition):
    try:
        s = mgmt_root.tm.sys.icall.scripts.script.load(name=name,
                                                       partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    s.delete()


def setup_create_script_test(request, mgmt_root, name, partition):
    def teardown():
        delete_script(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_script_test(request, mgmt_root, name, partition):
    def teardown():
        delete_script(mgmt_root, name, partition)
    script1 = mgmt_root.tm.sys.icall.scripts.script.create(
        name=name,
        partition=partition,
        definition=ICALLSCRIPT1)
    request.addfinalizer(teardown)
    return script1


def delete_istats_trigger(mgmt_root, name, partition):
    try:
        s = mgmt_root.tm.sys.icall.istats_triggers.istats_trigger.load(
            name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    s.delete()


def setup_create_istats_trigger_test(request, mgmt_root, name, partition):
    def teardown():
        delete_istats_trigger(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_istats_trigger_test(request, mgmt_root, name, partition):
    def teardown():
        delete_istats_trigger(mgmt_root, name, partition)
    ist1 = mgmt_root.tm.sys.icall.istats_triggers.istats_trigger.create(
        name=name,
        partition=partition,
        eventName='myevent',
        istatsKey='my key')
    request.addfinalizer(teardown)
    return ist1


def delete_periodic_handler(mgmt_root, name, partition):
    try:
        h = mgmt_root.tm.sys.icall.handler.periodics.periodic.load(
            name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    h.delete()


def setup_create_periodic_handler_test(request, mgmt_root, name, partition):
    def teardown():
        delete_periodic_handler(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_periodic_handler_test(request, mgmt_root, name, partition):
    def teardown():
        delete_periodic_handler(mgmt_root, name, partition)
    s1 = setup_basic_script_test(request, mgmt_root, 'myicallscript', 'Common')
    p1 = mgmt_root.tm.sys.icall.handler.periodics.periodic.create(
        name=name,
        partition=partition,
        script=s1.name,
        interval=300)
    request.addfinalizer(teardown)
    return p1, s1


def delete_perpetual_handler(mgmt_root, name, partition):
    try:
        h = mgmt_root.tm.sys.icall.handler.perpetuals.perpetual.load(
            name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    h.delete()


def setup_create_perpetual_handler_test(request, mgmt_root, name, partition):
    def teardown():
        delete_perpetual_handler(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_perpetual_handler_test(request, mgmt_root, name, partition):
    def teardown():
        delete_perpetual_handler(mgmt_root, name, partition)
    s1 = setup_basic_script_test(request, mgmt_root, 'myicallscript', 'Common')
    p1 = mgmt_root.tm.sys.icall.handler.perpetuals.perpetual.create(
        name=name,
        partition=partition,
        script=s1.name)
    request.addfinalizer(teardown)
    return p1, s1


def delete_triggered_handler(mgmt_root, name, partition):
    try:
        h = mgmt_root.tm.sys.icall.handler.triggered_s.triggered.load(
            name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    h.delete()


def setup_create_triggered_handler_test(request, mgmt_root, name, partition):
    def teardown():
        delete_triggered_handler(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_triggered_handler_test(request, mgmt_root, name, partition):
    def teardown():
        delete_triggered_handler(mgmt_root, name, partition)
    s1 = setup_basic_script_test(request, mgmt_root, 'myicallscript', 'Common')
    p1 = mgmt_root.tm.sys.icall.handler.triggered_s.triggered.create(
        name=name,
        partition=partition,
        script=s1.name)
    request.addfinalizer(teardown)
    return p1, s1


class Test_CULD_Script(object):
    def test_create_script_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.icall.scripts.script.create()

    def test_create(self, request, mgmt_root):
        setup_create_script_test(request, mgmt_root, 'myicallscript', 'Common')
        script1 = mgmt_root.tm.sys.icall.scripts.script.create(
            name='myicallscript', partition='Common', definition=ICALLSCRIPT1)
        assert script1.name == 'myicallscript'
        assert script1.partition == 'Common'
        assert script1.kind == 'tm:sys:icall:script:scriptstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.scripts.script.load(
                name='myicallscript', partition='Common')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_script_test(request, mgmt_root, 'myicallscript', 'Common')
        script1 = mgmt_root.tm.sys.icall.scripts.script.load(
            name='myicallscript', partition='Common')
        assert script1.name == 'myicallscript'
        assert script1.partition == 'Common'

    def test_delete(self, request, mgmt_root):
        s1 = setup_basic_script_test(request, mgmt_root, 'myicallscript',
                                     'Common')
        s1.delete()
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.scripts.script.load(
                name='myicallscript', partition='Common')
        assert err.value.response.status_code == 404

    def test_update(self, request, mgmt_root):
        s1 = setup_basic_script_test(request, mgmt_root, 'myicallscript',
                                     'Common')
        assert 'hello' in s1.definition

        s1.definition = ICALLSCRIPT2
        s1.update()

        assert 'hello' not in s1.definition
        assert 'goodbye' in s1.definition


class Test_CULD_Istats_Trigger(object):
    def test_create_script_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.icall.istats_triggers.istats_trigger.create()

    def test_create(self, request, mgmt_root):
        setup_create_istats_trigger_test(request, mgmt_root, 'myistatstrigger',
                                         'Common')
        ist1 = mgmt_root.tm.sys.icall.istats_triggers.istats_trigger.create(
            name='myistatstrigger', partition='Common', eventName='myevent',
            istatsKey='my key'
        )
        assert ist1.name == 'myistatstrigger'
        assert ist1.partition == 'Common'
        assert ist1.kind == 'tm:sys:icall:istats-trigger:istats-triggerstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.istats_triggers.istats_trigger.load(
                name='myistatstrigger', partition='Common')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_istats_trigger_test(request, mgmt_root, 'myistatstrigger',
                                        'Common')
        ist1 = mgmt_root.tm.sys.icall.istats_triggers.istats_trigger.load(
            name='myistatstrigger', partition='Common')
        assert ist1.name == 'myistatstrigger'
        assert ist1.partition == 'Common'

    def test_delete(self, request, mgmt_root):
        ist1 = setup_basic_istats_trigger_test(request, mgmt_root,
                                               'myistatstrigger', 'Common')
        ist1.delete()
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.istats_triggers.istats_trigger.load(
                name='myistatstrigger', partition='Common')
        assert err.value.response.status_code == 404

    def test_update(self, request, mgmt_root):
        ist1 = setup_basic_istats_trigger_test(request, mgmt_root,
                                               'myistatstrigger', 'Common')
        assert 'my key' in ist1.istatsKey

        ist1.istatsKey = 'my newkey'
        ist1.update()

        assert 'my key' not in ist1.istatsKey
        assert 'my newkey' in ist1.istatsKey


class Test_CULD_Periodic_Handler(object):
    def test_create_periodic_handler_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.icall.handler.periodics.periodic.create()

    def test_create(self, request, mgmt_root):
        h1, s1 = setup_basic_periodic_handler_test(
            request, mgmt_root, 'myhandler', 'Common'
        )
        assert h1.name == 'myhandler'
        assert h1.partition == 'Common'
        assert h1.kind == 'tm:sys:icall:handler:periodic:periodicstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.handler.periodics.periodic.load(
                name='myhandler', partition='Common')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        h1, s1 = setup_basic_periodic_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        h2 = mgmt_root.tm.sys.icall.handler.periodics.periodic.load(
            name='myhandler', partition='Common')
        assert h2.name == 'myhandler'

    def test_delete(self, request, mgmt_root):
        h1, s1 = setup_basic_periodic_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        h1.delete()
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.handler.periodics.periodic.load(
                name='myhandler', partition='Common')
        assert err.value.response.status_code == 404

    def test_update(self, request, mgmt_root):
        h1, s1 = setup_basic_periodic_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        assert h1.interval == 300
        h1.interval = 600
        h1.update()
        assert h1.interval == 600


class Test_CULD_Perpetual_Handler(object):
    def test_create_perpetual_handler_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.icall.handler.perpetuals.perpetual.create()

    def test_create(self, request, mgmt_root):
        h1, s1 = setup_basic_perpetual_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        assert h1.name == 'myhandler'
        assert h1.partition == 'Common'
        assert h1.kind == 'tm:sys:icall:handler:perpetual:perpetualstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.handler.perpetuals.perpetual.load(
                name='myhandler', partition='Common')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        h1, s1 = setup_basic_perpetual_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        h2 = mgmt_root.tm.sys.icall.handler.perpetuals.perpetual.load(
            name='myhandler', partition='Common')
        assert h2.name == 'myhandler'

    def test_delete(self, request, mgmt_root):
        h1, s1 = setup_basic_perpetual_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        h1.delete()
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.handler.perpetuals.perpetual.load(
                name='myhandler', partition='Common')
        assert err.value.response.status_code == 404

    def test_update(self, request, mgmt_root):
        h1, s1 = setup_basic_perpetual_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        assert h1.status == 'active'
        h1.status = 'inactive'
        h1.update()
        assert h1.status == 'inactive'


class Test_CULD_Triggered_Handler(object):
    def test_create_triggered_handler_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.icall.handler.triggered_s.triggered.create()

    def test_create(self, request, mgmt_root):
        h1, s1 = setup_basic_triggered_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        assert h1.name == 'myhandler'
        assert h1.partition == 'Common'
        assert h1.kind == 'tm:sys:icall:handler:triggered:triggeredstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.handler.triggered_s.triggered.load(
                name='myhandler', partition='Common')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        h1, s1 = setup_basic_triggered_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        h2 = mgmt_root.tm.sys.icall.handler.triggered_s.triggered.load(
            name='myhandler', partition='Common')
        assert h2.name == 'myhandler'

    def test_delete(self, request, mgmt_root):
        h1, s1 = setup_basic_triggered_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        h1.delete()
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.sys.icall.handler.triggered_s.triggered.load(
                name='myhandler', partition='Common')
        assert err.value.response.status_code == 404

    def test_update(self, request, mgmt_root):
        h1, s1 = setup_basic_triggered_handler_test(
            request, mgmt_root, 'myhandler', 'Common')
        assert h1.status == 'active'
        h1.status = 'inactive'
        h1.update()
        assert h1.status == 'inactive'

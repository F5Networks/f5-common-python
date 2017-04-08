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

import mock
import pytest

from f5.bigip import ManagementRoot

from f5.bigip.tm.sys.icall import Istats_Trigger
from f5.bigip.tm.sys.icall import Periodic
from f5.bigip.tm.sys.icall import Perpetual
from f5.bigip.tm.sys.icall import Script
from f5.bigip.tm.sys.icall import Triggered

from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeSysPeriodicHandler():
    fake_periodichandler_s = mock.MagicMock()
    fake_periodichandler = Periodic(fake_periodichandler_s)
    return fake_periodichandler


@pytest.fixture
def FakeSysPerpetualHandler():
    fake_perpetualhandler_s = mock.MagicMock()
    fake_perpetualhandler = Perpetual(fake_perpetualhandler_s)
    return fake_perpetualhandler


@pytest.fixture
def FakeSysTriggeredHandler():
    fake_triggeredhandler_s = mock.MagicMock()
    fake_triggeredhandler = Triggered(fake_triggeredhandler_s)
    return fake_triggeredhandler


@pytest.fixture
def FakeSysIstatsTrigger():
    fake_istatstrigger_s = mock.MagicMock()
    fake_istatstrigger = Istats_Trigger(fake_istatstrigger_s)
    return fake_istatstrigger


@pytest.fixture
def FakeSysScript():
    fake_script_s = mock.MagicMock()
    fake_script = Script(fake_script_s)
    return fake_script


class TestHandlers(object):
    def test_create_periodic_handler_no_args(self, FakeSysPeriodicHandler):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysPeriodicHandler.create()
        assert 'name' in ex.value.message

    def test_create_periodic_handler_missing_args(self,
                                                  FakeSysPeriodicHandler):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysPeriodicHandler.create(name='myperiodichandler',
                                               script='myscript')
        assert 'interval' in ex.value.message

        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysPeriodicHandler.create(name='myperiodichandler',
                                               interval='5')
        assert 'script' in ex.value.message

    def test_create_two_periodic_handler(self, fakeicontrolsession):
        b = ManagementRoot('10.0.2.15', 'admin', 'admin')
        ph1 = b.tm.sys.icall.handler.periodics.periodic
        ph2 = b.tm.sys.icall.handler.periodics.periodic
        assert ph1 is not ph2

    def test_create_perpetual_handler_no_args(self, FakeSysPerpetualHandler):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysPerpetualHandler.create()
        assert 'name' in ex.value.message

    def test_create_perpetual_handler_missing_args(self,
                                                   FakeSysPerpetualHandler):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysPerpetualHandler.create(name='myperpetualhandler')
        assert 'script' in ex.value.message

    def test_create_two_perpetual_handler(self, fakeicontrolsession):
        b = ManagementRoot('10.0.2.15', 'admin', 'admin')
        ph1 = b.tm.sys.icall.handler.perpetuals.perpetual
        ph2 = b.tm.sys.icall.handler.perpetuals.perpetual
        assert ph1 is not ph2

    def test_create_triggered_handler_no_args(self, FakeSysTriggeredHandler):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysTriggeredHandler.create()
        assert 'name' in ex.value.message

    def test_create_triggered_handler_missing_args(self,
                                                   FakeSysTriggeredHandler):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysTriggeredHandler.create(name='mytriggeredhandler')
        assert 'script' in ex.value.message

    def test_create_two_triggered_handler(self, fakeicontrolsession):
        b = ManagementRoot('10.0.2.15', 'admin', 'admin')
        th1 = b.tm.sys.icall.handler.triggered_s.triggered
        th2 = b.tm.sys.icall.handler.triggered_s.triggered
        assert th1 is not th2


class TestScripts(object):
    def test_create_script_no_args(self, FakeSysScript):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysScript.create()
        assert 'name' in ex.value.message

    def test_create_two_script(self, fakeicontrolsession):
        b = ManagementRoot('10.0.2.15', 'admin', 'admin')
        s1 = b.tm.sys.icall.scripts.script
        s2 = b.tm.sys.icall.scripts.script
        assert s1 is not s2


class TestIstatsTrigger(object):
    def test_create_istats_trigger_no_args(self, FakeSysIstatsTrigger):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysIstatsTrigger.create()
        assert 'name' in ex.value.message

    def test_create_istats_trigger_missing_args(self, FakeSysIstatsTrigger):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysIstatsTrigger.create(name='myistatstrigger',
                                        eventName='myevent')
        assert 'istatsKey' in ex.value.message

        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeSysIstatsTrigger.create(name='myistatstrigger',
                                        istatsKey='my key')
        assert 'eventName' in ex.value.message

    def test_create_two_istats_trigger(self, fakeicontrolsession):
        b = ManagementRoot('10.0.2.15', 'admin', 'admin')
        ist1 = b.tm.sys.icall.istats_triggers.istats_trigger
        ist2 = b.tm.sys.icall.istats_triggers.istats_trigger
        assert ist1 is not ist2

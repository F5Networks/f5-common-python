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

from distutils.version import LooseVersion
from f5.sdk_exception import UnsupportedOperation
from f5.sdk_exception import UnsupportedMethod
from requests.exceptions import HTTPError
from f5.bigip.tm.asm.policies.blocking_settings import Evasion
from f5.bigip.tm.asm.policies.blocking_settings import Evasions_s
from f5.bigip.tm.asm.policies.blocking_settings import Violation
from f5.bigip.tm.asm.policies.blocking_settings import Violations_s
from f5.bigip.tm.asm.policies.blocking_settings import Http_Protocol
from f5.bigip.tm.asm.policies.blocking_settings import Http_Protocols_s
from f5.bigip.tm.asm.policies.blocking_settings import Web_Services_Security
from f5.bigip.tm.asm.policies.blocking_settings import Web_Services_Securities_s


class TestBlockingSettings(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedMethod):
            policy.blocking_settings.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedMethod):
            policy.blocking_settings.delete()

    def test_load(self, policy):
        block = policy.blocking_settings.load()
        attributes = block._meta_data['attribute_registry']
        obj_class = [
            Evasions_s, Http_Protocols_s, Violations_s,
            Web_Services_Securities_s
        ]
        v12kind = 'tm:asm:policies:blocking-settings:blocking-settingcollectionstate'
        v11kind = 'tm:asm:policies:blocking-settings'
        if LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'):
            assert block.kind == v11kind
        else:
            assert block.kind == v12kind
        assert hasattr(block, 'httpProtocolReference')
        assert hasattr(block, 'webServicesSecurityReference')
        assert hasattr(block, 'evasionReference')
        assert hasattr(block, 'violationReference')
        assert set(obj_class) == set(attributes.values())


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('13.0.0'),
    reason='Needs TMOS version less than v13.0.0 to pass.'
)
class TestEvasions(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.evasions_s.evasion.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.evasions_s.evasion.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        hashid = str(coll[0].id)
        eva1 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        eva2 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        assert eva1.kind == eva2.kind
        assert eva1.description == eva2.description
        assert eva1.enabled == eva2.enabled
        eva2.modify(enabled=False)
        assert eva1.enabled is True
        assert eva2.enabled is False
        eva1.refresh()
        assert eva1.enabled is False

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.blocking_settings.evasions_s.evasion.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        hashid = str(coll[0].id)
        eva1 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        assert eva1.kind == 'tm:asm:policies:blocking-settings:evasions:evasionstate'
        assert eva1.enabled is True
        eva1.modify(enabled=False)
        assert eva1.enabled is False
        eva2 = policy.blocking_settings.evasions_s.evasion.load(id=eva1.id)
        assert eva1.selfLink == eva2.selfLink
        assert eva1.kind == eva2.kind
        assert eva1.enabled == eva2.enabled

    def test_evasions_subcollection(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Evasion)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='Needs TMOS version greater than or equal to v13.0.0 to pass.'
)
class TestEvasionsV13(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.evasions_s.evasion.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.evasions_s.evasion.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        hashid = str(coll[0].id)
        eva1 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        eva2 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        assert eva1.kind == eva2.kind
        assert eva1.description == eva2.description
        assert eva1.enabled == eva2.enabled
        eva2.modify(enabled=True)
        assert eva1.enabled is False
        assert eva2.enabled is True
        eva1.refresh()
        assert eva1.enabled is True

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.blocking_settings.evasions_s.evasion.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        hashid = str(coll[0].id)
        eva1 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        assert eva1.kind == 'tm:asm:policies:blocking-settings:evasions:evasionstate'
        assert eva1.enabled is False
        eva1.modify(enabled=True)
        assert eva1.enabled is True
        eva2 = policy.blocking_settings.evasions_s.evasion.load(id=eva1.id)
        assert eva1.selfLink == eva2.selfLink
        assert eva1.kind == eva2.kind
        assert eva1.enabled == eva2.enabled

    def test_evasions_subcollection(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Evasion)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('13.0.0'),
    reason='Needs TMOS version less than v13.0.0 to pass.'
)
class TestViolations(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.violations_s.violation.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.violations_s.violation.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        hashid = str(coll[0].id)
        vio1 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        vio2 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        assert vio1.kind == vio2.kind
        assert vio1.description == vio2.description
        assert vio1.learn == vio2.learn
        vio2.modify(learn=False)
        assert vio1.learn is True
        assert vio2.learn is False
        vio1.refresh()
        assert vio1.learn is False

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.blocking_settings.violations_s.violation.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        hashid = str(coll[0].id)
        vio1 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        assert vio1.kind == 'tm:asm:policies:blocking-settings:violations:violationstate'
        assert vio1.learn is True
        vio1.modify(learn=False)
        assert vio1.learn is False
        vio2 = policy.blocking_settings.violations_s.violation.load(id=vio1.id)
        assert vio1.selfLink == vio2.selfLink
        assert vio1.kind == vio2.kind
        assert vio1.learn == vio2.learn

    def test_violations_subcollection(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Violation)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='Needs TMOS version greater than or equal to v13.0.0 to pass.'
)
class TestViolationsV13(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.violations_s.violation.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.violations_s.violation.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        hashid = str(coll[0].id)
        vio1 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        vio2 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        assert vio1.kind == vio2.kind
        assert vio1.description == vio2.description
        assert vio1.learn == vio2.learn
        vio2.modify(learn=True)
        assert vio1.learn is False
        assert vio2.learn is True
        vio1.refresh()
        assert vio1.learn is True

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.blocking_settings.violations_s.violation.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        hashid = str(coll[0].id)
        vio1 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        assert vio1.kind == 'tm:asm:policies:blocking-settings:violations:violationstate'
        assert vio1.learn is False
        vio1.modify(learn=True)
        assert vio1.learn is True
        vio2 = policy.blocking_settings.violations_s.violation.load(id=vio1.id)
        assert vio1.selfLink == vio2.selfLink
        assert vio1.kind == vio2.kind
        assert vio1.learn == vio2.learn

    def test_violations_subcollection(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Violation)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('13.0.0'),
    reason='Needs TMOS version less than v13.0.0 to pass.'
)
class TestHTTPProtocols(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.http_protocols_s.http_protocol.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.http_protocols_s.http_protocol.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        hashid = str(coll[1].id)
        http1 = policy.blocking_settings.http_protocols_s.http_protocol.load(id=hashid)
        http2 = policy.blocking_settings.http_protocols_s.http_protocol.load(id=hashid)
        assert http1.kind == http2.kind
        assert http1.description == http2.description
        assert http1.enabled == http2.enabled
        http2.modify(enabled=False)
        assert http1.enabled is True
        assert http2.enabled is False
        http1.refresh()
        assert http1.enabled is False

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.blocking_settings.http_protocols_s.http_protocol.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        hashid = str(coll[1].id)
        http1 = policy.blocking_settings.http_protocols_s.http_protocol.load(
            id=hashid)
        assert http1.kind == 'tm:asm:policies:blocking-settings:http-protocols:http-protocolstate'
        assert http1.enabled is True
        http1.modify(enabled=False)
        assert http1.enabled is False
        http2 = policy.blocking_settings.http_protocols_s.http_protocol.load(id=http1.id)
        assert http1.selfLink == http2.selfLink
        assert http1.kind == http2.kind
        assert http1.enabled == http2.enabled

    def test_httpprotocols_subcollection(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Http_Protocol)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='Needs TMOS version greater than or equal to v13.0.0 to pass.'
)
class TestHTTPProtocolsV13(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.http_protocols_s.http_protocol.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.http_protocols_s.http_protocol.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        hashid = str(coll[1].id)
        http1 = policy.blocking_settings.http_protocols_s.http_protocol.load(id=hashid)
        http2 = policy.blocking_settings.http_protocols_s.http_protocol.load(id=hashid)
        assert http1.kind == http2.kind
        assert http1.description == http2.description
        assert http1.enabled == http2.enabled
        http2.modify(enabled=True)
        assert http1.enabled is False
        assert http2.enabled is True
        http1.refresh()
        assert http1.enabled is True

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            protocols = policy.blocking_settings.http_protocols_s
            protocols.http_protocol.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        hashid = str(coll[1].id)
        http1 = policy.blocking_settings.http_protocols_s.http_protocol.load(
            id=hashid
        )
        assert http1.kind == 'tm:asm:policies:blocking-settings:http-protocols:http-protocolstate'
        assert http1.enabled is False
        http1.modify(enabled=True)
        assert http1.enabled is True
        http2 = policy.blocking_settings.http_protocols_s. \
            http_protocol.load(id=http1.id)
        assert http1.selfLink == http2.selfLink
        assert http1.kind == http2.kind
        assert http1.enabled == http2.enabled

    def test_httpprotocols_subcollection(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Http_Protocol)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('13.0.0'),
    reason='Needs TMOS version less than v13.0.0 to pass.'
)
class TestWebServicesSecurities(object):
    def test_create_raises(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(UnsupportedOperation):
            wsc.web_services_security.create()

    def test_delete_raises(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(UnsupportedOperation):
            wsc.web_services_security.delete()

    def test_refresh(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        hashid = str(coll[1].id)
        ws1 = wsc.web_services_security.load(id=hashid)
        ws2 = wsc.web_services_security.load(id=hashid)
        assert ws1.kind == ws2.kind
        assert ws1.description == ws2.description
        assert ws1.enabled == ws2.enabled
        ws2.modify(enabled=False)
        assert ws1.enabled is True
        assert ws2.enabled is False
        ws1.refresh()
        assert ws1.enabled is False

    def test_load_no_object(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(HTTPError) as err:
            wsc.web_services_security.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        hashid = str(coll[1].id)
        ws1 = wsc.web_services_security.load(id=hashid)
        assert ws1.kind == 'tm:asm:policies:blocking-settings:web-services-securities:web-services-securitystate'
        assert ws1.enabled is True
        ws1.modify(enabled=False)
        assert ws1.enabled is False
        ws2 = wsc.web_services_security.load(id=ws1.id)
        assert ws1.selfLink == ws2.selfLink
        assert ws1.kind == ws2.kind
        assert ws1.enabled == ws2.enabled

    def test_webservicessecurities_subcollection(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Web_Services_Security)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='Needs TMOS version greater than or equal to v13.0.0 to pass.'
)
class TestWebServicesSecuritiesV13(object):
    def test_create_raises(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(UnsupportedOperation):
            wsc.web_services_security.create()

    def test_delete_raises(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(UnsupportedOperation):
            wsc.web_services_security.delete()

    def test_refresh(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        hashid = str(coll[1].id)
        ws1 = wsc.web_services_security.load(id=hashid)
        ws2 = wsc.web_services_security.load(id=hashid)
        assert ws1.kind == ws2.kind
        assert ws1.description == ws2.description
        assert ws1.enabled == ws2.enabled
        ws2.modify(enabled=True)
        assert ws1.enabled is False
        assert ws2.enabled is True
        ws1.refresh()
        assert ws1.enabled is True

    def test_load_no_object(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(HTTPError) as err:
            wsc.web_services_security.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        hash_id = coll[0].id
        ws1 = wsc.web_services_security.load(id=hash_id)
        assert ws1.kind == 'tm:asm:policies:blocking-settings:web-services-securities:web-services-securitystate'
        assert ws1.enabled is False

    def test_webservicessecurities_subcollection(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Web_Services_Security)

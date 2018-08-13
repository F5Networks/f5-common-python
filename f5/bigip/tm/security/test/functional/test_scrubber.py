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
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.security.scrubber import Profile
from f5.bigip.tm.security.scrubber import Scrubber_Categories
from f5.bigip.tm.security.scrubber import Scrubber_Netflow_Protected_Server
from f5.bigip.tm.security.scrubber import Scrubber_Rd_Network_Prefix
from f5.bigip.tm.security.scrubber import Scrubber_Rt_Domain
from f5.bigip.tm.security.scrubber import Scrubber_Virtual_Server
from requests.exceptions import HTTPError

DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def scrubber_categories(mgmt_root):
    p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
    cat_lst = p1.scrubber_categories_s
    params_set = {'name': 'fake_categories_profile', 'blacklistCategory': '/Common/proxy', 'routeDomainName': '/Common/0', 'nextHop': '1.1.1.1'}
    c1 = cat_lst.scrubber_categories.create(**params_set)
    yield c1
    c1.delete()


@pytest.fixture(scope='function')
def traffic_matching_criteria(mgmt_root):
    tmc1 = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s.traffic_matching_criteria.create(
        name='fake_tmc', destinationAddressInline='1.1.1.1', sourceAddressInline='2.2.2.2', partition='Common')
    yield tmc1
    tmc1.delete()


@pytest.fixture(scope='function')
def netflow_protected_server(mgmt_root, traffic_matching_criteria):
    tmc = traffic_matching_criteria
    nps1 = mgmt_root.tm.security.protected_servers.netflow_protected_server_s.netflow_protected_server.create(
        name='fake_nps', trafficMatchingCriteria=tmc.fullPath, partition='Common')
    yield nps1
    nps1.delete()


@pytest.fixture(scope='function')
def scrubber_netflow_protected_server(mgmt_root, netflow_protected_server):
    nps = netflow_protected_server
    p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
    nps_lst = p1.scrubber_netflow_protected_server_s
    params_set = {'name': 'fake_netflow_protected_server_profile', 'npsName': nps.fullPath, 'nextHop': '1.1.1.1'}
    nps1 = nps_lst.scrubber_netflow_protected_server.create(**params_set)
    yield nps1
    nps1.delete()


@pytest.fixture(scope='function')
def virtual(mgmt_root):
    vs = mgmt_root.tm.ltm.virtuals.virtual.create(
        name='fake_virtual', partition='Common', protocol='tcp')
    yield vs
    vs.delete()


@pytest.fixture(scope='function')
def scrubber_virtual_server(mgmt_root, virtual):
    vs = virtual
    p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
    cat_lst = p1.scrubber_virtual_server_s
    params_set = {'name': 'fake_virtual_server_profile', 'vsName': vs.fullPath, 'nextHop': '1.1.1.1'}
    v1 = cat_lst.scrubber_virtual_server.create(**params_set)
    yield v1
    v1.delete()


@pytest.fixture(scope='function')
def scrubber_rt_domain(mgmt_root):
    p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
    rd_lst = p1.scrubber_rt_domain_s
    params_set = {'name': 'fake_rt_domain_profile', 'routeDomain': '/Common/0', 'nextHop': '1.1.1.1'}
    rd1 = rd_lst.scrubber_rt_domain.create(**params_set)
    yield rd1
    rd1.delete()


@pytest.fixture(scope='function')
def scrubber_rd_network_prefix(mgmt_root):
    p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
    rd_lst = p1.scrubber_rt_domain_s
    params_set = {'name': 'fake_rt_domain_profile', 'routeDomain': '/Common/0', 'nextHop': '1.1.1.1'}
    rd1 = rd_lst.scrubber_rt_domain.create(**params_set)
    rd_net_lst = rd1.scrubber_rd_network_prefix_s
    net_params_set = {'name': 'fake_rd_network_prefix_profile', 'dstIp': '1.1.1.0', 'mask': '24', 'nextHop': '2.2.2.2'}
    rd_net1 = rd_net_lst.scrubber_rd_network_prefix.create(**net_params_set)
    yield rd_net1
    rd_net1.delete()
    rd1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='This collection is fully implemented on 13.0.0 or greater.'
)
class TestProfile(object):
    def test_load_no_object(self, mgmt_root):
        p = mgmt_root.tm.security.scrubber.profile_s.profile
        with pytest.raises(HTTPError) as err:
            p.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root):
        p = mgmt_root.tm.security.scrubber.profile_s.profile
        p1 = p.load(name='scrubber-profile-default', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default'
        assert p1.name == 'scrubber-profile-default'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        p1.advertisementTtl = 500
        p1.update()
        p2 = p.load(name='scrubber-profile-default', partition='Common')
        assert p1.name == p2.name
        assert p1.partition == p2.partition
        assert p1.selfLink == p2.selfLink
        assert p2.advertisementTtl == '500'

    def test_profile_collection(self, mgmt_root):
        pc = mgmt_root.tm.security.scrubber.profile_s.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Profile)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='This collection is fully implemented on 13.0.0 or greater.'
)
class TestScrubberCategories(object):
    def test_mandatory_attribute_missing(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        cat_lst = p1.scrubber_categories_s
        ERR = "Missing required params"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            cat_lst.scrubber_categories.create(name='botnets')
        assert str(err.value).startswith(ERR)

    def test_create_req_arg(self, scrubber_categories):
        c1 = scrubber_categories
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-categories/fake_categories_profile'
        assert c1.name == 'fake_categories_profile'
        assert c1.selfLink.startswith(URI)

    def test_create_optional_args(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        cat_lst = p1.scrubber_categories_s
        params_set = {'name': 'fake_categories_profile', 'blacklistCategory': '/Common/proxy', 'routeDomainName': '/Common/0',
                      'nextHop': '1.1.1.1', 'advertisementMethod': 'bgp-flowspec-method'}
        c1 = cat_lst.scrubber_categories.create(**params_set)
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-categories/fake_categories_profile'
        assert c1.name == 'fake_categories_profile'
        assert c1.selfLink.startswith(URI)
        assert c1.advertisementMethod == 'bgp-flowspec-method'
        c1.delete()

    def test_refresh(self, scrubber_categories, mgmt_root):
        c1 = scrubber_categories
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        cat_lst = p1.scrubber_categories_s
        c2 = cat_lst.scrubber_categories.load(name='fake_categories_profile')
        assert c1.name == c2.name
        assert c1.selfLink == c2.selfLink
        assert c1.kind == c2.kind
        c2.modify(advertisementMethod='bgp-flowspec-method')
        assert c2.advertisementMethod == 'bgp-flowspec-method'
        c1.refresh()
        assert c1.advertisementMethod == 'bgp-flowspec-method'

    def test_delete(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        cat_lst = p1.scrubber_categories_s
        params_set = {'name': 'fake_categories_profile', 'blacklistCategory': '/Common/proxy',
                      'routeDomainName': '/Common/0', 'nextHop': '1.1.1.1', 'advertisementMethod': 'bgp-flowspec-method'}
        c1 = cat_lst.scrubber_categories.create(**params_set)
        c1.delete()
        with pytest.raises(HTTPError) as err:
            cat_lst.scrubber_categories.load(name='fake_categories_profile')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        cat_lst = p1.scrubber_categories_s
        with pytest.raises(HTTPError) as err:
            cat_lst.scrubber_categories.load(name='fake_categories_profile')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, scrubber_categories, mgmt_root):
        c1 = scrubber_categories
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-categories/fake_categories_profile'
        assert c1.name == 'fake_categories_profile'
        assert c1.selfLink.startswith(URI)
        c1.advertisementMethod = 'bgp-flowspec-method'
        c1.update()
        assert c1.advertisementMethod == 'bgp-flowspec-method'
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        cat_lst = p1.scrubber_categories_s
        c2 = cat_lst.scrubber_categories.load(name='fake_categories_profile')
        assert c1.name == c2.name
        assert c1.selfLink == c2.selfLink
        assert c1.kind == c2.kind
        assert c2.advertisementMethod == 'bgp-flowspec-method'

    def test_scrubber_categories_subcollection(self, scrubber_categories, mgmt_root):
        c1 = scrubber_categories
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-categories/fake_categories_profile'
        assert c1.name == 'fake_categories_profile'
        assert c1.selfLink.startswith(URI)
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        cat_lst = p1.scrubber_categories_s
        cat_col = cat_lst.get_collection()
        assert isinstance(cat_col, list)
        assert len(cat_col)
        assert isinstance(cat_col[0], Scrubber_Categories)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='This collection is fully implemented on 13.0.0 or greater.'
)
class TestScrubberVS(object):
    def test_mandatory_attribute_missing(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        vs_lst = p1.scrubber_virtual_server_s
        ERR = "Missing required params"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            vs_lst.scrubber_virtual_server.create(name='fake')
        assert str(err.value).startswith(ERR)

    def test_create_req_arg(self, scrubber_virtual_server):
        v1 = scrubber_virtual_server
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-virtual-server/fake_virtual_server_profile'
        assert v1.name == 'fake_virtual_server_profile'
        assert v1.selfLink.startswith(URI)

    def test_create_optional_args(self, mgmt_root, virtual):
        vs = virtual
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        vs_lst = p1.scrubber_virtual_server_s
        params_set = {'name': 'fake_virtual_server_profile', 'vsName': vs.fullPath, 'nextHop': '1.1.1.1',
                      'advertisementMethod': 'bgp-flowspec-method'}
        v1 = vs_lst.scrubber_virtual_server.create(**params_set)
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-virtual-server/fake_virtual_server_profile'
        assert v1.name == 'fake_virtual_server_profile'
        assert v1.selfLink.startswith(URI)
        assert v1.advertisementMethod == 'bgp-flowspec-method'
        v1.delete()

    def test_refresh(self, scrubber_virtual_server, mgmt_root):
        v1 = scrubber_virtual_server
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        vs_lst = p1.scrubber_virtual_server_s
        v2 = vs_lst.scrubber_virtual_server.load(name='fake_virtual_server_profile')
        assert v1.name == v2.name
        assert v1.selfLink == v2.selfLink
        assert v1.kind == v2.kind
        v2.modify(advertisementMethod='bgp-flowspec-method')
        assert v2.advertisementMethod == 'bgp-flowspec-method'
        v1.refresh()
        assert v1.advertisementMethod == 'bgp-flowspec-method'

    def test_delete(self, mgmt_root, virtual):
        vs = virtual
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        vs_lst = p1.scrubber_virtual_server_s
        params_set = {'name': 'fake_virtual_server_profile', 'vsName': vs.fullPath, 'nextHop': '1.1.1.1',
                      'advertisementMethod': 'bgp-flowspec-method'}
        v1 = vs_lst.scrubber_virtual_server.create(**params_set)
        v1.delete()
        with pytest.raises(HTTPError) as err:
            vs_lst.scrubber_virtual_server.load(name='fake_virtual_server_profile')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        vs_lst = p1.scrubber_virtual_server_s
        with pytest.raises(HTTPError) as err:
            vs_lst.scrubber_virtual_server.load(name='fake_virtual_server_profile')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, scrubber_virtual_server, mgmt_root):
        v1 = scrubber_virtual_server
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-virtual-server/fake_virtual_server_profile'
        assert v1.name == 'fake_virtual_server_profile'
        assert v1.selfLink.startswith(URI)
        v1.advertisementMethod = 'bgp-flowspec-method'
        v1.update()
        assert v1.advertisementMethod == 'bgp-flowspec-method'
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        vs_lst = p1.scrubber_virtual_server_s
        v2 = vs_lst.scrubber_virtual_server.load(name='fake_virtual_server_profile')
        assert v1.name == v2.name
        assert v1.selfLink == v2.selfLink
        assert v1.kind == v2.kind
        assert v2.advertisementMethod == 'bgp-flowspec-method'

    def test_scrubber_vs_subcollection(self, scrubber_virtual_server, mgmt_root):
        v1 = scrubber_virtual_server
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-virtual-server/fake_virtual_server_profile'
        assert v1.name == 'fake_virtual_server_profile'
        assert v1.selfLink.startswith(URI)
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        vs_lst = p1.scrubber_virtual_server_s
        vs_col = vs_lst.get_collection()
        assert isinstance(vs_col, list)
        assert len(vs_col)
        assert isinstance(vs_col[0], Scrubber_Virtual_Server)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='This collection is fully implemented on 13.0.0 or greater.'
)
class TestScrubberNPS(object):
    def test_mandatory_attribute_missing(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        nps_lst = p1.scrubber_netflow_protected_server_s
        ERR = "Missing required params"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            nps_lst.scrubber_netflow_protected_server.create(name='botnets')
        assert str(err.value).startswith(ERR)

    def test_create_req_arg(self, scrubber_netflow_protected_server):
        nps1 = scrubber_netflow_protected_server
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-netflow-protected-server/fake_netflow_protected_server_profile'
        assert nps1.name == 'fake_netflow_protected_server_profile'
        assert nps1.selfLink.startswith(URI)

    def test_create_optional_args(self, mgmt_root, netflow_protected_server):
        nps = netflow_protected_server
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        nps_lst = p1.scrubber_netflow_protected_server_s
        params_set = {'name': 'fake_netflow_protected_server_profile', 'npsName': nps.fullPath, 'nextHop': '1.1.1.1',
                      'advertisementMethod': 'bgp-flowspec-method'}
        nps1 = nps_lst.scrubber_netflow_protected_server.create(**params_set)
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-netflow-protected-server/fake_netflow_protected_server_profile'
        assert nps1.name == 'fake_netflow_protected_server_profile'
        assert nps1.selfLink.startswith(URI)
        assert nps1.advertisementMethod == 'bgp-flowspec-method'
        nps1.delete()

    def test_refresh(self, scrubber_netflow_protected_server, mgmt_root):
        nps1 = scrubber_netflow_protected_server
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        nps_lst = p1.scrubber_netflow_protected_server_s
        c2 = nps_lst.scrubber_netflow_protected_server.load(name='fake_netflow_protected_server_profile')
        assert nps1.name == c2.name
        assert nps1.selfLink == c2.selfLink
        assert nps1.kind == c2.kind
        c2.modify(advertisementMethod='bgp-flowspec-method')
        assert c2.advertisementMethod == 'bgp-flowspec-method'
        nps1.refresh()
        assert nps1.advertisementMethod == 'bgp-flowspec-method'

    def test_delete(self, mgmt_root, netflow_protected_server):
        nps = netflow_protected_server
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        nps_lst = p1.scrubber_netflow_protected_server_s
        params_set = {'name': 'fake_netflow_protected_server_profile', 'npsName': nps.fullPath, 'nextHop': '1.1.1.1',
                      'advertisementMethod': 'bgp-flowspec-method'}
        nps1 = nps_lst.scrubber_netflow_protected_server.create(**params_set)
        nps1.delete()
        with pytest.raises(HTTPError) as err:
            nps_lst.scrubber_netflow_protected_server.load(name='fake_netflow_protected_server_profile')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        nps_lst = p1.scrubber_netflow_protected_server_s
        with pytest.raises(HTTPError) as err:
            nps_lst.scrubber_netflow_protected_server.load(name='fake_netflow_protected_server_profile')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, scrubber_netflow_protected_server, mgmt_root):
        nps1 = scrubber_netflow_protected_server
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-netflow-protected-server/fake_netflow_protected_server_profile'
        assert nps1.name == 'fake_netflow_protected_server_profile'
        assert nps1.selfLink.startswith(URI)
        nps1.advertisementMethod = 'bgp-flowspec-method'
        nps1.update()
        assert nps1.advertisementMethod == 'bgp-flowspec-method'
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        nps_lst = p1.scrubber_netflow_protected_server_s
        c2 = nps_lst.scrubber_netflow_protected_server.load(name='fake_netflow_protected_server_profile')
        assert nps1.name == c2.name
        assert nps1.selfLink == c2.selfLink
        assert nps1.kind == c2.kind
        assert c2.advertisementMethod == 'bgp-flowspec-method'

    def test_scrubber_netflow_protected_server_subcollection(self, scrubber_netflow_protected_server, mgmt_root):
        nps1 = scrubber_netflow_protected_server
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-netflow-protected-server/fake_netflow_protected_server_profile'
        assert nps1.name == 'fake_netflow_protected_server_profile'
        assert nps1.selfLink.startswith(URI)
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        nps_lst = p1.scrubber_netflow_protected_server_s
        nps_col = nps_lst.get_collection()
        assert isinstance(nps_col, list)
        assert len(nps_col)
        assert isinstance(nps_col[0], Scrubber_Netflow_Protected_Server)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='This collection is fully implemented on 13.0.0 or greater.'
)
class TestScrubberRtDomain(object):
    def test_mandatory_attribute_missing(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        ERR = "Missing required params"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            rd_lst.scrubber_rt_domain.create(name='fake_rt_domain_profile')
        assert str(err.value).startswith(ERR)

    def test_create_req_arg(self, scrubber_rt_domain):
        rd1 = scrubber_rt_domain
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-rt-domain/fake_rt_domain_profile'
        assert rd1.name == 'fake_rt_domain_profile'
        assert rd1.selfLink.startswith(URI)

    def test_create_optional_args(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        params_set = {'name': 'fake_rt_domain_profile', 'routeDomain': '/Common/0', 'nextHop': '1.1.1.1', 'advertisementMethod': 'bgp-flowspec-method'}
        rd1 = rd_lst.scrubber_rt_domain.create(**params_set)
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-rt-domain/fake_rt_domain_profile'
        assert rd1.name == 'fake_rt_domain_profile'
        assert rd1.selfLink.startswith(URI)
        assert rd1.advertisementMethod == 'bgp-flowspec-method'
        rd1.delete()

    def test_refresh(self, scrubber_rt_domain, mgmt_root):
        rd1 = scrubber_rt_domain
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        rd2 = rd_lst.scrubber_rt_domain.load(name='fake_rt_domain_profile')
        assert rd1.name == rd2.name
        assert rd1.selfLink == rd2.selfLink
        assert rd1.kind == rd2.kind
        rd2.modify(advertisementMethod='bgp-flowspec-method')
        assert rd2.advertisementMethod == 'bgp-flowspec-method'
        rd1.refresh()
        assert rd1.advertisementMethod == 'bgp-flowspec-method'

    def test_delete(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        params_set = {'name': 'fake_rt_domain_profile', 'routeDomain': '/Common/0', 'nextHop': '1.1.1.1', 'advertisementMethod': 'bgp-flowspec-method'}
        rd1 = rd_lst.scrubber_rt_domain.create(**params_set)
        rd1.delete()
        with pytest.raises(HTTPError) as err:
            rd_lst.scrubber_rt_domain.load(name='fake_rt_domain_profile')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        with pytest.raises(HTTPError) as err:
            rd_lst.scrubber_rt_domain.load(name='fake_rt_domain_profile')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, scrubber_rt_domain, mgmt_root):
        rd1 = scrubber_rt_domain
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-rt-domain/fake_rt_domain_profile'
        assert rd1.name == 'fake_rt_domain_profile'
        assert rd1.selfLink.startswith(URI)
        rd1.advertisementMethod = 'bgp-flowspec-method'
        rd1.update()
        assert rd1.advertisementMethod == 'bgp-flowspec-method'
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        rd2 = rd_lst.scrubber_rt_domain.load(name='fake_rt_domain_profile')
        assert rd1.name == rd2.name
        assert rd1.selfLink == rd2.selfLink
        assert rd1.kind == rd2.kind
        assert rd2.advertisementMethod == 'bgp-flowspec-method'

    def test_scrubber_rt_domain_subcollection(self, scrubber_rt_domain, mgmt_root):
        rd1 = scrubber_rt_domain
        URI = 'https://localhost/mgmt/tm/security/' \
            'scrubber/profile/~Common~scrubber-profile-default/scrubber-rt-domain/fake_rt_domain_profile'
        assert rd1.name == 'fake_rt_domain_profile'
        assert rd1.selfLink.startswith(URI)
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        rd_col = rd_lst.get_collection()
        assert isinstance(rd_col, list)
        assert len(rd_col)
        assert isinstance(rd_col[0], Scrubber_Rt_Domain)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='This collection is fully implemented on 13.0.0 or greater.'
)
class TestScrubberRdNetworkPrefix(object):
    def test_mandatory_attribute_missing(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        params_set = {'name': 'fake_rt_domain_profile', 'routeDomain': '/Common/0', 'nextHop': '1.1.1.1'}
        rd1 = rd_lst.scrubber_rt_domain.create(**params_set)
        rd_net_lst = rd1.scrubber_rd_network_prefix_s
        ERR = "Missing required params"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            rd_net_lst.scrubber_rd_network_prefix.create(name='fake_rd_network_prefix_profile')
        assert str(err.value).startswith(ERR)
        rd1.delete()

    def test_create_req_arg(self, scrubber_rd_network_prefix):
        rd_net1 = scrubber_rd_network_prefix
        URI = 'https://localhost/mgmt/tm/security/scrubber/profile/' \
              '~Common~scrubber-profile-default/scrubber-rt-domain/fake_rt_domain_profile/scrubber-rd-network-prefix/fake_rd_network_prefix_profile'
        assert rd_net1.name == 'fake_rd_network_prefix_profile'
        assert rd_net1.selfLink.startswith(URI)

    def test_refresh(self, scrubber_rd_network_prefix, mgmt_root):
        rd_net1 = scrubber_rd_network_prefix
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        rd1 = rd_lst.scrubber_rt_domain.load(name='fake_rt_domain_profile')
        rd_net_lst = rd1.scrubber_rd_network_prefix_s
        rd_net2 = rd_net_lst.scrubber_rd_network_prefix.load(name='fake_rd_network_prefix_profile')
        assert rd_net1.name == rd_net2.name
        assert rd_net1.selfLink == rd_net2.selfLink
        assert rd_net1.kind == rd_net2.kind
        rd_net2.modify(nextHop='3.3.3.3')
        assert rd_net2.nextHop == '3.3.3.3'
        rd_net1.refresh()
        assert rd_net1.nextHop == '3.3.3.3'

    def test_delete(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        params_set = {'name': 'fake_rt_domain_profile', 'routeDomain': '/Common/0', 'nextHop': '1.1.1.1'}
        rd1 = rd_lst.scrubber_rt_domain.create(**params_set)
        rd_net_lst = rd1.scrubber_rd_network_prefix_s
        net_params_set = {'name': 'fake_rd_network_prefix_profile', 'dstIp': '1.1.1.0', 'mask': '24', 'nextHop': '2.2.2.2'}
        rd_net1 = rd_net_lst.scrubber_rd_network_prefix.create(**net_params_set)
        rd_net1.delete()
        with pytest.raises(HTTPError) as err:
            rd_net_lst.scrubber_rd_network_prefix.load(name='fake_rd_network_prefix_profile')
        assert err.value.response.status_code == 404
        rd1.delete()

    def test_load_no_object(self, mgmt_root):
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        params_set = {'name': 'fake_rt_domain_profile', 'routeDomain': '/Common/0', 'nextHop': '1.1.1.1'}
        rd1 = rd_lst.scrubber_rt_domain.create(**params_set)
        rd_net_lst = rd1.scrubber_rd_network_prefix_s
        with pytest.raises(HTTPError) as err:
            rd_net_lst.scrubber_rd_network_prefix.load(name='fake_rd_network_prefix_profile')
        assert err.value.response.status_code == 404
        rd1.delete()

    def test_load_and_update(self, scrubber_rd_network_prefix, mgmt_root):
        rd_net1 = scrubber_rd_network_prefix
        URI = 'https://localhost/mgmt/tm/security/scrubber/profile/' \
            '~Common~scrubber-profile-default/scrubber-rt-domain/fake_rt_domain_profile/scrubber-rd-network-prefix/fake_rd_network_prefix_profile'
        assert rd_net1.name == 'fake_rd_network_prefix_profile'
        assert rd_net1.selfLink.startswith(URI)
        rd_net1.nextHop = '3.3.3.3'
        rd_net1.update()
        assert rd_net1.nextHop == '3.3.3.3'
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        rd1 = rd_lst.scrubber_rt_domain.load(name='fake_rt_domain_profile')
        rd_net_lst = rd1.scrubber_rd_network_prefix_s
        rd_net2 = rd_net_lst.scrubber_rd_network_prefix.load(name='fake_rd_network_prefix_profile')
        assert rd_net1.name == rd_net2.name
        assert rd_net1.selfLink == rd_net2.selfLink
        assert rd_net1.kind == rd_net2.kind
        assert rd_net2.nextHop == '3.3.3.3'

    def test_scrubber_rd_network_prefix_subcollection(self, scrubber_rd_network_prefix, mgmt_root):
        rd_net1 = scrubber_rd_network_prefix
        URI = 'https://localhost/mgmt/tm/security/scrubber/profile/' \
            '~Common~scrubber-profile-default/scrubber-rt-domain/fake_rt_domain_profile/scrubber-rd-network-prefix/fake_rd_network_prefix_profile'
        assert rd_net1.name == 'fake_rd_network_prefix_profile'
        assert rd_net1.selfLink.startswith(URI)
        p1 = mgmt_root.tm.security.scrubber.profile_s.profile.load(name='scrubber-profile-default', partition='Common')
        rd_lst = p1.scrubber_rt_domain_s
        rd1 = rd_lst.scrubber_rt_domain.load(name='fake_rt_domain_profile')
        rd_net_lst = rd1.scrubber_rd_network_prefix_s
        rd_net_col = rd_net_lst.get_collection()
        assert isinstance(rd_net_col, list)
        assert len(rd_net_col)
        assert isinstance(rd_net_col[0], Scrubber_Rd_Network_Prefix)

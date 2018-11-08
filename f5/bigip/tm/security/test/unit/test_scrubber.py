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

from f5.bigip import ManagementRoot
from f5.bigip.tm.security.scrubber import Scrubber_Categories
from f5.bigip.tm.security.scrubber import Scrubber_Categories_s
from f5.bigip.tm.security.scrubber import Scrubber_Netflow_Protected_Server
from f5.bigip.tm.security.scrubber import Scrubber_Netflow_Protected_Server_s
from f5.bigip.tm.security.scrubber import Scrubber_Rt_Domain
from f5.bigip.tm.security.scrubber import Scrubber_Rt_Domain_s
from f5.bigip.tm.security.scrubber import Scrubber_Virtual_Server
from f5.bigip.tm.security.scrubber import Scrubber_Virtual_Server_s

from six import iterkeys


def MakeScrubberProfile(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.scrubber.profile_s.profile
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/scrubber/profile/' \
        '~Common~scrubber-profile-default/'
    return p


class TestProfile(object):
    def test_scrubber_profile(self, fakeicontrolsession):
        a = ManagementRoot('192.168.1.1', 'admin', 'admin')
        prof1 = a.tm.security.scrubber.profile_s.profile
        prof1._meta_data['uri'] = \
            'https://192.168.1.1:443/mgmt/tm/security/scrubber/profile/~Common~scrubber-profile-default'


class TestScrubberRtDomainSubCollection(object):
    def test_scrubber_rt_domain_subcollection(self, fakeicontrolsession):
        pc = Scrubber_Rt_Domain_s(MakeScrubberProfile(fakeicontrolsession))
        kind = 'tm:security:scrubber:profile:scrubber-rt-domain:scrubber-rt-domainstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Scrubber_Rt_Domain_s)
        assert kind in list(iterkeys(test_meta))
        assert Scrubber_Rt_Domain in test_meta2


class TestScrubberVirtualServerSubCollection(object):
    def test_scrubber_virtual_server_subcollection(self, fakeicontrolsession):
        pc = Scrubber_Virtual_Server_s(MakeScrubberProfile(fakeicontrolsession))
        kind = 'tm:security:scrubber:profile:scrubber-virtual-server:scrubber-virtual-serverstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Scrubber_Virtual_Server_s)
        assert kind in list(iterkeys(test_meta))
        assert Scrubber_Virtual_Server in test_meta2


class TestScrubberCategoriesSubCollection(object):
    def test_scrubber_categories_subcollection(self, fakeicontrolsession):
        pc = Scrubber_Categories_s(MakeScrubberProfile(fakeicontrolsession))
        kind = 'tm:security:scrubber:profile:scrubber-categories:scrubber-categoriesstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Scrubber_Categories_s)
        assert kind in list(iterkeys(test_meta))
        assert Scrubber_Categories in test_meta2


class TestScrubberNetflowProtectedServerSubCollection(object):
    def test_scrubber_netflow_protected_server_subcollection(self, fakeicontrolsession):
        pc = Scrubber_Netflow_Protected_Server_s(MakeScrubberProfile(fakeicontrolsession))
        kind = 'tm:security:scrubber:profile:scrubber-netflow-protected-server:scrubber-netflow-protected-serverstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Scrubber_Netflow_Protected_Server_s)
        assert kind in list(iterkeys(test_meta))
        assert Scrubber_Netflow_Protected_Server in test_meta2

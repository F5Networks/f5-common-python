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
import pytest

from f5.bigip.resource import UnsupportedOperation


# Obtaining device name for tests to work
def check_device(request, mgmt_root):
    dvcs = mgmt_root.tm.cm.devices.get_collection()
    devname = str(dvcs[0].fullPath)
    return devname


class TestTrustDomain(object):
    def test_curld(self, request, mgmt_root):

        # Load the Root trust domain into two variables for testing
        td1 = mgmt_root.tm.cm.trust_domains.trust_domain.load(
            name='Root', partition='Common')
        td2 = mgmt_root.tm.cm.trust_domains.trust_domain.load(
            name='Root', partition='Common')

        devname = check_device(request, mgmt_root)
        assert td1.caDevices == [devname, ]

        # Update - Add self device
        td2.caDevices = []
        td2.update()
        assert not hasattr(td2, 'caDevices')
        assert td2.generation > td1.generation

        # Refresh
        td1.refresh()
        assert not hasattr(td1, 'caDevices')
        assert td1.generation == td2.generation

        # Add self back to trust domain
        td2.caDevices = [devname, ]
        td2.update()

        # Create
        with pytest.raises(UnsupportedOperation) as err:
            mgmt_root.tm.cm.trust_domains.trust_domain.create(
                name='test_trust_domain',
                partition='Common'
            )
            assert 'BIG-IP trust domains cannot be created by users'\
                   in err.value.text

        # Delete
        with pytest.raises(UnsupportedOperation) as err:
            td2.delete()
            assert 'BIG-IP trust domains cannot be deleted by users'\
                   in err.value.text

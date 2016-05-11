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

from requests import HTTPError


def setup_trust_domain_test(request, bigip, name, partition, **kwargs):
    def teardown():
        try:
            td.delete()
        except HTTPError as err:
            if err.response.status_code is not 404:
                raise
    request.addfinalizer(teardown)
    td = bigip.cm.trust_domains.trust_domain.create(
        name=name, partition=partition, **kwargs)
    return td


# Obtaining device name for tests to work
def check_device(request, bigip):
    dvcs = bigip.cm.devices.get_collection()
    devname = str(dvcs[0].fullPath)
    return devname


class TestTrustDomain(object):
    def test_curdl(self, request, bigip):

        # Create and delete are done with teardown
        td1 = setup_trust_domain_test(request, bigip,
                                      'test_trust', 'Common')
        assert td1.name == 'test_trust'

        # Load
        td2 = bigip.cm.trust_domains.trust_domain.load(name=td1.name,
                                                       partition=td1.partition)
        assert td1.generation == td2.generation

        # Update
        devname = check_device(request, bigip)
        td1.caDevices = [devname, ]
        td1.update()
        assert td1.caDevices == [devname, ]
        assert not hasattr(td2, 'caDevices')
        assert td1.generation > td2.generation

        # Refresh
        td2.refresh()
        assert td2.caDevices == [devname, ]
        assert td1.generation == td2.generation

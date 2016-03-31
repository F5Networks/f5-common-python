# Copyright 2015-2016 F5 Networks Inc.
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

from collections import namedtuple
PoolConfig = namedtuple('PoolConfig', 'partition name memberconfigs')
MemberConfig = namedtuple('MemberConfig', 'mempartition memname')


def test_get_collection(request, bigip, pool_factory, opt_release):
    Pool1MemberConfigs = (MemberConfig('Common', '192.168.15.15:80'),
                          MemberConfig('Common', '192.168.16.16:8080'),)
    Pool1Config = PoolConfig('Common', 'TEST', Pool1MemberConfigs)
    test_pools = (Pool1Config,)
    pool_registry, member_registry =\
        pool_factory(bigip, request, test_pools)
    selfLinks = []
    for pool_inst in pool_registry.values():
        for mem in pool_inst.members_s.get_collection():
            selfLinks.append(mem.selfLink)
    assert selfLinks[0] == u'https://localhost/mgmt/tm/ltm/pool/' +\
        '~Common~TEST/members/~Common~192.168.15.15:80' +\
        '?ver='+opt_release
    assert selfLinks[1] == u'https://localhost/mgmt/tm/ltm/pool/' +\
        '~Common~TEST/members/~Common~192.168.16.16:8080' +\
        '?ver='+opt_release


def test_get_dollar_filtered_collection(request, bigip, pool_factory):
    hostname = bigip._meta_data['hostname']
    if bigip.sys.folders.folder.exists(name='za', partition=''):
        bigip.sys.folders.folder.load(name='za', partition='')
    else:
        bigip.sys.folders.folder.create(name='za', subPath='/')
    Pool1Config = PoolConfig('Common', 'TEST', ((),))
    Pool2Config = PoolConfig('za', 'TEST', ((),))
    test_pools = (Pool1Config, Pool2Config)
    pool_registry, member_registry =\
        pool_factory(bigip, request, test_pools)
    rp = {'params': {'$filter': 'partition eq za'}}
    pools_in_za = bigip.ltm.pools.get_collection(requests_params=rp)
    muri = pools_in_za[0]._meta_data['uri']
    assert muri == 'https://'+hostname+'/mgmt/tm/ltm/pool/~za~TEST/'

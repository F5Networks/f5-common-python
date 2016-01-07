# Copyright 2014 F5 Networks Inc.
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
from f5.bigip import BigIP
from f5.bigip.mixins import LazyAttributesRequired

bigip = BigIP('10.190.5.7', 'admin', 'admin')
nat1 = bigip.ltm.natcollection.nat
nat2 = bigip.ltm.natcollection.nat
try:
    nat1.create(name='za_test_001', partition='Common',
                originatingAddress='192.168.3.1',
                translationAddress='192.168.3.2')
except LazyAttributesRequired as LAR:
    raise
nat2.load(partition='Common', name='za_test_001')
nat2.update(arp=u'disabled')
nc = bigip.ltm.natcollection
# print(nc.__dict__)
print('******')
CRLUDs = nc.get_collection()
print('******')
# print(nc.__dict__['items'])
nat2.refresh()
print(CRLUDs)
nat1.delete()
CRLUDs2 = nc.get_collection()
print('!!!!!!!!!!')
print(CRLUDs2)
lc = bigip.ltm
print('lc.__dict__: %r' % lc.__dict__)
lc.get_collection()
print('lc.__dict__: %r' % lc.__dict__)
print(lc.get_collection())

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
try:
    nat1.create(name='aaa59', partition='Common',
                originatingAddress='192.168.2.59',
                translationAddress='192.168.1.59')
except LazyAttributesRequired as LAR:
    print("Inside LAR exception.")
    print(LAR)
    print(nat1.__dict__)
    raise
print("No LAR!!")
nat1._read()
print(nat1.__dict__)

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
from pprint import pprint as pp

from f5.bigip import BigIP
from f5.bigip.shared import Shared


def test_shared(request, bigip):
    s = bigip.shared
    pp(s.raw)
    assert isinstance(s._meta_data['container'], BigIP)
    assert s._meta_data['allowed_lazy_attributes'][0].__name__ == "Licensing"
    l = bigip.shared.licensing
    pp(l.raw)
    assert isinstance(l._meta_data['container'], Shared)

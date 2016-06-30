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

from pprint import pprint as pp
pp('')


def test_persist_universal_CURDLE(bigip, opt_release):
    u1 = bigip.ltm.persistence.universals.universal.create(
        partition="Common", name="UniversalTest")
    assert u1.selfLink ==\
        u"https://localhost/mgmt/tm/ltm/persistence/universal/"\
        "~Common~UniversalTest?ver="+opt_release
    assert u1.timeout == u"180"
    u1.timeout = 179
    u1.update()
    assert u1.timeout == u"179"
    u2 = bigip.ltm.persistence.universals.universal.load(
        partition="Common", name="UniversalTest")
    u2.timeout = u"180"
    u2.update()
    u1.refresh()
    assert u1.timeout == u"180"
    u1.delete()
    assert u1.raw == {u"deleted": True}
    assert u2.exists(partition="Common", name="UniversalTest") is False


def test_persist_cookie_CURDLE(bigip, opt_release):
    c1 = bigip.ltm.persistence.cookies.cookie.create(
        partition="Common", name="CookieTest")
    assert c1.selfLink ==\
        u"https://localhost/mgmt/tm/ltm/persistence/cookie/"\
        "~Common~CookieTest?ver="+opt_release
    assert c1.timeout == u"180"
    c1.timeout = 179
    c1.update()
    assert c1.timeout == u"179"
    c2 = bigip.ltm.persistence.cookies.cookie.load(
        partition="Common", name="CookieTest")
    c2.timeout = u"180"
    c2.update()
    c1.refresh()
    assert c1.timeout == u"180"
    c1.delete()
    assert c1.raw == {u"deleted": True}
    assert c2.exists(partition="Common", name="CookieTest") is False

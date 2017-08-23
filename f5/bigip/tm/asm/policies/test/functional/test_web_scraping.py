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


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
    reason='This collection is fully implemented on 12.0.0 or greater.'
)
@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('13.0.0'),
    reason='Needs TMOS version greater than or equal to v13.0.0 to pass.'
)
class TestWebScraping(object):
    def test_update_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.web_scraping.update()

    def test_load(self, policy):
        r1 = policy.web_scraping.load()
        assert r1.kind == 'tm:asm:policies:web-scraping:web-scrapingstate'
        assert r1.enableFingerprinting is False
        r1.modify(enableFingerprinting=True)
        assert r1.enableFingerprinting is True
        r2 = policy.web_scraping.load()
        assert r1.kind == r2.kind
        assert r1.enableFingerprinting == r2.enableFingerprinting

    def test_refresh(self, policy):
        r1 = policy.web_scraping.load()
        assert r1.kind == 'tm:asm:policies:web-scraping:web-scrapingstate'
        assert r1.enableFingerprinting is False
        r2 = policy.web_scraping.load()
        assert r1.kind == r2.kind
        assert r1.enableFingerprinting == r2.enableFingerprinting
        r2.modify(enableFingerprinting=True)
        assert r2.enableFingerprinting is True
        r1.refresh()
        assert r1.enableFingerprinting is True


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='Needs TMOS version greater than or equal to v13.0.0 to pass.'
)
class TestWebScrapingV13(object):
    def test_update_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.web_scraping.update()

    def test_load(self, policy):
        r1 = policy.web_scraping.load()
        assert r1.kind == 'tm:asm:policies:web-scraping:web-scrapingstate'
        assert r1.enableFingerprinting is True
        r1.modify(enableFingerprinting=False)
        assert r1.enableFingerprinting is False
        r2 = policy.web_scraping.load()
        assert r1.kind == r2.kind
        assert r1.enableFingerprinting == r2.enableFingerprinting

    def test_refresh(self, policy):
        r1 = policy.web_scraping.load()
        assert r1.kind == 'tm:asm:policies:web-scraping:web-scrapingstate'
        assert r1.enableFingerprinting is True
        r2 = policy.web_scraping.load()
        assert r1.kind == r2.kind
        assert r1.enableFingerprinting == r2.enableFingerprinting
        r2.modify(enableFingerprinting=False)
        assert r2.enableFingerprinting is False
        r1.refresh()
        assert r1.enableFingerprinting is False

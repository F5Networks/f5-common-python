# Copyright 2018 F5 Networks Inc.
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
from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.analytics.dos_vis_common import Generate_Report
from f5.bigip.tm.analytics.dos_vis_common import Report_Results
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedOperation


import mock
import pytest
from six import iterkeys


@pytest.fixture
def FakeGenerateReport():
    fake_analytics = mock.MagicMock()
    fake_genrep = Generate_Report(fake_analytics)
    fake_genrep._meta_data['bigip'].tmos_version = '13.1.0'
    return fake_genrep


@pytest.fixture
def FakeReportResults():
    fake_analytics = mock.MagicMock()
    fake_repres = Report_Results(fake_analytics)
    return fake_repres


class TestDosVisCommonOC(object):
    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.analytics.dos_vis_common
        assert isinstance(t1, OrganizingCollection)
        assert hasattr(t1, 'generate_reports')
        assert hasattr(t1, 'report_results_s')


class TestGenerateReport(object):
    def test_modify_raises(self, FakeGenerateReport):
        with pytest.raises(UnsupportedOperation):
            FakeGenerateReport.modify()

    def test_create_no_args(self, FakeGenerateReport):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeGenerateReport.create()

    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.analytics.dos_vis_common.generate_reports.generate_report
        t2 = b.tm.analytics.dos_vis_common.generate_reports.generate_report
        assert t1 is t2

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.analytics.dos_vis_common.generate_reports
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:analytics:dos-vis-common:generate-report:avrgeneratereporttaskitemstate'
        assert kind in list(iterkeys(test_meta))
        assert Generate_Report in test_meta2
        assert t._meta_data['object_has_stats'] is False


class TestReportResults(object):
    def test_create_raises(self, FakeReportResults):
        with pytest.raises(UnsupportedOperation):
            FakeReportResults.create()

    def test_modify_raises(self, FakeReportResults):
        with pytest.raises(UnsupportedOperation):
            FakeReportResults.modify()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.analytics.dos_vis_common.report_results_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:analytics:dos-vis-common:report-results:avrreportresultitemstate'
        assert kind in list(iterkeys(test_meta))
        assert Report_Results in test_meta2
        assert t._meta_data['object_has_stats'] is False

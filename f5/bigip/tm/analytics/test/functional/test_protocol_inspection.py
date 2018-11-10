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

import pytest
import time

from distutils.version import LooseVersion
from f5.bigip.tm.analytics.protocol_inspection import Generate_Report
from f5.bigip.tm.analytics.protocol_inspection import Report_Results


@pytest.fixture(scope='function')
def generate_report(mgmt_root):
    task = mgmt_root.tm.analytics.protocol_inspection.generate_reports.generate_report.create(
        reportFeatures=['entities-count'],
        viewDimensions=[{'dimensionName': 'profile'}],
    )
    while True:
        task.refresh()
        if task.status in ['FINISHED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def get_reports(mgmt_root):
    task = mgmt_root.tm.analytics.protocol_inspection.generate_reports.load()
    while True:
        task.refresh()
        if task.status in ['FINISHED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='Generating a report returns an unexpected error in 13.0.0.'
)
class TestGenerateReport(object):
    def test_create_rep_arg(self, generate_report):
        rep1 = generate_report
        endpoint = str(rep1.id)
        base_uri = 'https://localhost/mgmt/tm/analytics/protocol-inspection/generate-report/'
        final_uri = base_uri + endpoint
        assert rep1.selfLink.startswith(final_uri)
        assert rep1.kind == 'tm:analytics:protocol-inspection:generate-report:avrgeneratereporttaskitemstate'


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='Generating a report returns an unexpected error in 13.0.0.'
)
class TestGenerateReportCollection(object):
    def test_collection_gen_rep(self, generate_report, mgmt_root):
        rep1 = generate_report
        reports = mgmt_root.tm.analytics.protocol_inspection.generate_reports.get_collection()
        assert isinstance(reports[0], Generate_Report)
        assert rep1.id in [report.id for report in reports]


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='Generating a report returns an unexpected error in 13.0.0.'
)
class TestReportResults(object):
    def test_create_rep(self, generate_report, mgmt_root):
        rep = generate_report
        result_id = rep.reportResultsLink.split('/')[-1]
        result = mgmt_root.tm.analytics.protocol_inspection.report_results_s.report_results.load(id=result_id)
        assert result.kind == 'tm:analytics:protocol-inspection:report-results:avrreportresultitemstate'


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='Generating a report returns an unexpected error in 13.0.0.'
)
class TestReportResultsCollection(object):
    def test_collection_rep_res(self, generate_report, mgmt_root):
        rep = generate_report
        result_id = rep.reportResultsLink.split('/')[-1]
        results = mgmt_root.tm.analytics.protocol_inspection.report_results_s.get_collection()
        assert isinstance(results[0], Report_Results)
        assert result_id in [result.id for result in results]

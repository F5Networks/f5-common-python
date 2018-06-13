# coding=utf-8
#
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

""" BIG-IP® Application Visibility and Reporting™ (AVR®) DoS Visibility sub-module.

REST URI
    ``http://localhost/mgmt/tm/analytics/dos-vis-common/``

GUI Path
    ``Security --> Reporting --> DoS``

REST Kind
    ``tm:analytics:dos-vis-common:``
"""
from f5.bigip.resource import AsmResource as AvrResource
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.sdk_exception import UnsupportedOperation


class Dos_Vis_Common(OrganizingCollection):
    """BIG-IP® AVR DoS Visibility organizing collection."""
    def __init__(self, analytics):
        super(Dos_Vis_Common, self).__init__(analytics)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Generate_Reports,
            Report_Results_s,
        ]


class Generate_Reports(Collection):
    """BIG-IP® AVR Generate Report Collection."""
    def __init__(self, dos_vis_common):
        super(Generate_Reports, self).__init__(dos_vis_common)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Generate_Report]
        self._meta_data['attribute_registry'] = {
            'tm:analytics:dos-vis-common:generate-report:avrgeneratereporttaskitemstate': Generate_Report}


class Generate_Report(AvrResource):
    """BIG-IP® AVR Generate Report Resource."""
    def __init__(self, generate_reports):
        super(Generate_Report, self).__init__(generate_reports)
        self._meta_data['required_json_kind'] =\
            'tm:analytics:dos-vis-common:generate-report:avrgeneratereporttaskitemstate'
        self._meta_data['required_creation_parameters'] = {'viewDimensions',
                                                           'reportFeatures',
                                                           }

    def modify(self, **kwargs):
        """Modify is not supported for Generate Report resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )


class Report_Results_s(Collection):
    """BIG-IP® AVR Report Results Collection."""
    def __init__(self, dos_vis_common):
        super(Report_Results_s, self).__init__(dos_vis_common)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Report_Results]
        self._meta_data['attribute_registry'] = {
            'tm:analytics:dos-vis-common:report-results:avrreportresultitemstate':
                Report_Results}


class Report_Results(AvrResource):
    """BIG-IP® AVR Report Results Resource."""
    def __init__(self, report_results_s):
        super(Report_Results, self).__init__(report_results_s)
        self._meta_data['required_json_kind'] =\
            'tm:analytics:dos-vis-common:report-results:avrreportresultitemstate'

    def create(self, **kwargs):
        """Create is not supported for Report Results resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for Report Results resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

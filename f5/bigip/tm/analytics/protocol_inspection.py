
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

""" BIG-IP® Application Visibility and Reporting™ (AVR®) Protocol Inspection sub-module.
REST URI
    ``http://localhost/mgmt/tm/analytics/protocol-inspection/``
GUI Path
    ``Security --> Reporting --> Protocol Inspection``
REST Kind
    ``tm:analytics:protocol-inspection:``
"""
from f5.bigip.resource import AsmResource as AvrResource
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.sdk_exception import UnsupportedOperation


class Protocol_Inspection(OrganizingCollection):
    """BIG-IP® AVR protocol inspection organizing collection."""
    def __init__(self, analytics):
        super(Protocol_Inspection, self).__init__(analytics)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Generate_Reports,
            Report_Results_s,
        ]


class Generate_Reports(Collection):
    """BIG-IP® AVR Generate Report Collection."""
    def __init__(self, protocol_inspection):
        super(Generate_Reports, self).__init__(protocol_inspection)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Generate_Report]
        self._meta_data['attribute_registry'] = {
            'tm:analytics:protocol-inspection:generate-report:avrgeneratereporttaskitemstate': Generate_Report}


class Generate_Report(AvrResource):
    """BIG-IP® AVR Generate Report Resource."""
    def __init__(self, generate_reports):
        super(Generate_Report, self).__init__(generate_reports)
        self._meta_data['required_json_kind'] =\
            'tm:analytics:protocol-inspection:generate-report:avrgeneratereporttaskitemstate'
        self._meta_data['required_creation_parameters'] = {'viewDimensions',
                                                           'reportFeatures',
                                                           }

    def modify(self, **kwargs):
        """Modify is not supported for Generate Report resource :raises: UnsupportedOperation"""
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )


class Report_Results_s(Collection):
    """BIG-IP® AVR Report Results Collection."""
    def __init__(self, protocol_inspection):
        super(Report_Results_s, self).__init__(protocol_inspection)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Report_Results]
        self._meta_data['attribute_registry'] = {
            'tm:analytics:protocol-inspection:report-results:avrreportresultitemstate':
                Report_Results}


class Report_Results(AvrResource):
    """BIG-IP® AVR Report Results Resource."""
    def __init__(self, report_results_s):
        super(Report_Results, self).__init__(report_results_s)
        self._meta_data['required_json_kind'] =\
            'tm:analytics:protocol-inspection:report-results:avrreportresultitemstate'

    def create(self, **kwargs):
        """Create is not supported for Report Results resource :raises: UnsupportedOperation"""
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for Report Results resource :raises: UnsupportedOperation"""
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

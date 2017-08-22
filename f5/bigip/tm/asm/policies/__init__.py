# coding=utf-8
#
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

import time

from distutils.version import LooseVersion
from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection
from icontrol.exceptions import iControlUnexpectedHTTPError


from . methods import Methods_s
from . filetypes import Filetypes_s
from . cookies import Cookies_s
from . host_names import Host_Names_s
from . urls import Urls_s
from . parameters import Parameters_s
from . data_guard import Data_Guard
from . blocking_settings import Blocking_Settings
from . whitelist_ips import Whitelist_Ips_s
from . gwt_profiles import Gwt_Profiles_s
from . json_profiles import Json_Profiles_s
from . xml_profiles import Xml_Profiles_s
from . signatures import Signatures_s
from . signature_sets import Signature_Sets_s
from . headers import Headers_s
from . response_pages import Response_Pages_s
from . policy_builder import Policy_Builder
from . history_revisions import History_Revisions_s
from . vulnerability_assessment import Vulnerability_Assessment
from . geolocation_enforcement import Geolocation_Enforcement
from . session_tracking import Session_Tracking
from . session_tracking_status import Session_Tracking_Statuses_s
from . login_pages import Login_Pages_s
from . ip_intelligence import Ip_Intelligence
from . csrf_protection import Csrf_Protection
from . redirection_protection import Redirection_Protection
from . login_enforcement import Login_Enforcement
from . sensitive_parameters import Sensitive_Parameters_s
from . brute_force import Brute_Force_Attack_Preventions_s
from . xml_validation import Xml_Validation_Files_s
from . extractions import Extractions_s
from . vulnerabilities import Vulnerabilities_s
from . navigation_parameters import Navigation_Parameters_s
from . character_sets import Character_Sets_s
from . web_scraping import Web_Scraping
from . audit_logs import Audit_Logs_s
from . suggestions import Suggestions_s
from . plain_text_profiles import Plain_Text_Profiles_s
from . websocket_urls import Websocket_Urls_s
from . general import General


class Policies_s(Collection):
    """BIG-IP® ASM Policies collection."""
    def __init__(self, asm):
        super(Policies_s, self).__init__(asm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Policy]
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:policystate': Policy
        }


class Policy(AsmResource):
    """BIG-IP® ASM Policies resource."""
    def __init__(self, policies_s):
        super(Policy, self).__init__(policies_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:policystate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:methods:methodcollectionstate': Methods_s,
            'tm:asm:policies:filetypes:filetypecollectionstate': Filetypes_s,
            'tm:asm:policies:cookies:cookiecollectionstate': Cookies_s,
            'tm:asm:policies:host-names:host-namecollectionstate': Host_Names_s,
            'tm:asm:policies:urls:urlcollectionstate': Urls_s,
            'tm:asm:policies:parameters:parametercollectionstate': Parameters_s,
            'tm:asm:policies:whitelist-ips:whitelist-ipcollectionstate': Whitelist_Ips_s,
            'tm:asm:policies:gwt-profiles:gwt-profilecollectionstate': Gwt_Profiles_s,
            'tm:asm:policies:json-profiles:json-profilecollectionstate': Json_Profiles_s,
            'tm:asm:policies:xml-profiles:xml-profilecollectionstate': Xml_Profiles_s,
            'tm:asm:policies:signatures:signaturecollectionstate': Signatures_s,
            'tm:asm:policies:signature-sets:signature-setcollectionstate': Signature_Sets_s,
            'tm:asm:policies:headers:headercollectionstate': Headers_s,
            'tm:asm:policies:response-pages:response-pagecollectionstate': Response_Pages_s,
            'tm:asm:policies:history-revisions:history-revisioncollectionstate': History_Revisions_s,
            'tm:asm:policies:vulnerability-assessment:vulnerability-assessmentstate': Vulnerability_Assessment,
            'tm:asm:policies:data-guard:data-guardstate': Data_Guard,
            'tm:asm:policies:geolocation-enforcement:geolocation-enforcementstate': Geolocation_Enforcement,
            'tm:asm:policies:session-tracking:session-awareness-settingsstate': Session_Tracking,
            'tm:asm:policies:session-tracking-statuses:session-tracking-statuscollectionstate': Session_Tracking_Statuses_s,
            'tm:asm:policies:login-pages:login-pagecollectionstate': Login_Pages_s,
            'tm:asm:policies:ip-intelligence:ip-intelligencestate': Ip_Intelligence,
            'tm:asm:policies:csrf-protection:csrf-protectionstate': Csrf_Protection,
            'tm:asm:policies:redirection-protection:redirection-protectionstate': Redirection_Protection,
            'tm:asm:policies:login-enforcement:login-enforcementstate': Login_Enforcement,
            'tm:asm:policies:sensitive-parameters:sensitive-parametercollectionstate': Sensitive_Parameters_s,
            'tm:asm:policies:brute-force-attack-preventions:brute-force-attack-preventioncollectionstate': Brute_Force_Attack_Preventions_s,
            'tm:asm:policies:xml-validation-files:xml-validation-filecollectionstate': Xml_Validation_Files_s,
            'tm:asm:policies:extractions:extractioncollectionstate': Extractions_s,
            'tm:asm:policies:vulnerabilities:vulnerabilitycollectionstate': Vulnerabilities_s,
            'tm:asm:policies:navigation-parameters:navigation-parametercollectionstate': Navigation_Parameters_s,
            'tm:asm:policies:character-sets:character-setcollectionstate': Character_Sets_s,
            'tm:asm:policies:web-scraping:web-scrapingstate': Web_Scraping,
            'tm:asm:policies:audit-logs:audit-logcollectionstate': Audit_Logs_s,
            'tm:asm:policies:suggestions:suggestioncollectionstate': Suggestions_s,
            'tm:asm:policies:plain-text-profiles:plain-text-profilecollectionstate': Plain_Text_Profiles_s,
            'tm:asm:policies:websocket-urls:websocket-urlcollectionstate': Websocket_Urls_s
        }

        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) >= LooseVersion('13.0.0'):
            self._meta_data['attribute_registry'].update({
                'tm:asm:policies:general:generalstate': General
            })

        self._set_attr_reg()

    def _set_attr_reg(self):
        """Helper method.

        Appends correct attribute registry, depending on TMOS version

        """
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        attributes = self._meta_data['attribute_registry']
        v12kind = 'tm:asm:policies:blocking-settings:blocking-settingcollectionstate'
        v11kind = 'tm:asm:policies:blocking-settings'
        builderv11 = 'tm:asm:policies:policy-builder:pbconfigstate'
        builderv12 = 'tm:asm:policies:policy-builder:policy-builderstate'
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            attributes[v11kind] = Blocking_Settings
            attributes[builderv11] = Policy_Builder
        else:
            attributes[v12kind] = Blocking_Settings
            attributes[builderv12] = Policy_Builder

    def create(self, **kwargs):
        """Custom creation logic to handle edge cases

        This shouldn't be needed, but ASM has a tendency to raise various errors that
        are painful to handle from a customer point-of-view

        The error itself are described in their exception handler

        To address these failure, we try a number of exception handling cases to catch
        and reliably deal with the error.

        :param kwargs:
        :return:
        """
        for x in range(0, 30):
            try:
                return self._create(**kwargs)
            except iControlUnexpectedHTTPError as ex:
                if self._check_exception(ex):
                    continue
                else:
                    raise

    def delete(self, **kwargs):
        """Custom deletion logic to handle edge cases

        This shouldn't be needed, but ASM has a tendency to raise various errors that
        are painful to handle from a customer point-of-view

        The error itself are described in their exception handler

        To address these failure, we try a number of exception handling cases to catch
        and reliably deal with the error.

        :param kwargs:
        :return:
        """
        for x in range(0, 30):
            try:
                return self._delete(**kwargs)
            except iControlUnexpectedHTTPError as ex:
                if self._check_exception(ex):
                    continue
                else:
                    raise

    def _check_exception(self, ex):
        retryable = [
            # iControlUnexpectedHTTPError: 400 Unexpected Error: Bad Request for uri: ...
            # {
            #     "code":400,
            #     "message": "remoteSender:10.0.2.2,method:DELETE ",
            #     "referer":"10.0.2.2",
            #     "restOperationId":103685,
            #     "errorStack":[
            #         "java.util.concurrent.TimeoutException: remoteSender:10.0.2.2, method:DELETE ",
            #         "at com.f5.rest.common.RestWorker.logAndFailExpiredOperation(RestWorker.java:3035)",
            #         "at com.f5.reent.TimeoutException: remoteSender:10.0.2.2, method:DELETE ",
            #         "at com.f5.rest.common.RestWorker.logAndFailExpiredOperation(RestWorker.java:3035)",
            #         "at com.f5.rest.common.RestWorker.checkForExpiredOperations(RestWorker.java:3024)",
            #         "at com.f5.rest.common.RestServer.checkAndExpirePendingWorkerOperations(RestServer.java:1416)",
            #         "at com.f5.rest.common.RestServer.access$400(RestServer.java:45)",
            #         "at com.f5.rest.common.RestServer$4.run(RestServer.java:1389)",
            #         "at com.f5.rest.common.ScheduleTaskManager$2$1.run(ScheduleTaskManager.java:123)",
            #         "at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:471)",
            #         "at java.util.concurrent.FutureTask.run(FutureTask.java:262)",
            #         "at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$201(ScheduledThreadPoolExecutor.java:178)",
            #         "at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:292)",
            #         "at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1145)",
            #         "at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:615)",
            #         "at java.lang.Thread.run(Thread.java:745)\\n"
            #     ],
            #     "kind":":resterrorresponse"
            # }'
            'TimeoutException',

            # {
            #   "code":400,
            #   "message":"Failed on insert to DCC.FILE_REFERENCES_FOR_DELETION
            #              (DBD::mysql::db do failed: Duplicate entry
            #              \'/ts/var/xml/defense_config/xml_profile_2312\' for key \'filename\')",
            #   "referer":"10.0.2.2",
            #   "restOperationId":142433,
            #   "kind":":resterrorresponse"
            # }
            'Failed on insert to DCC.FILE_REFERENCES_FOR_DELETION',

            # iControlUnexpectedHTTPError: 500 Unexpected Error: Internal Server Error ...
            # {
            #   "code": 500,
            #   "message": "Could not add_signature the Attack Signature.  "
            #              "Failed on insert to PLC.NEGSIG_SET_SIGNATURES "
            #              "(DBD::mysql::db do failed: Lock wait timeout exceeded; "
            #              "try restarting transaction)
            #
            'Lock wait timeout exceeded',
        ]
        if any(x in str(ex) for x in retryable):
            time.sleep(3)
            return True
        elif 'errorStack' in ex:
            stack = ' '.join(ex['errorStack'])
            if any(x in stack for x in retryable):
                time.sleep(3)
                return True
            else:
                return False
        else:
            return False

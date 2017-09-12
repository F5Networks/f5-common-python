# coding=utf-8
#
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

from distutils.version import LooseVersion
from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection
from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedOperation


class Blocking_Settings(UnnamedResource):
    """BIG-IP® ASM Blocking-Settings Unnamed Resource."""
    def __init__(self, policy):
        super(Blocking_Settings, self).__init__(policy)
        tmos_v = policy._meta_data['bigip']._meta_data['tmos_version']
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Evasions_s, Http_Protocols_s, Violations_s,
            Web_Services_Securities_s
        ]

        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            # kind has changed in v12, hence we need the below
            self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings:blocking-settingcollectionstate'
        else:
            self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings'

        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:evasions:evasioncollectionstate': Evasions_s,
            'tm:asm:policies:blocking-settings:violations:violationcollectionstate': Violations_s,
            'tm:asm:policies:blocking-settings:http-protocols:http-protocolcollectionstate': Http_Protocols_s,
            'tm:asm:policies:blocking-settings:web-services-securities:web-services-securitycollectionstate': Web_Services_Securities_s
        }


class Evasions_s(Collection):
    """BIG-IP® ASM Evasions sub-collection."""
    def __init__(self, blocking_settings):
        super(Evasions_s, self).__init__(blocking_settings)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Evasion]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings:evasions:evasioncollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:evasions:evasionstate': Evasion
        }


class Evasion(AsmResource):
    """BIG-IP® ASM Evasions resource."""
    def __init__(self, evasions_s):
        super(Evasion, self).__init__(evasions_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings:evasions:evasionstate'
        self._meta_data['reduction_forcing_pairs'] = []

    def create(self, **kwargs):
        """Create is not supported for Evasion resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Evasion resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Violations_s(Collection):
    """BIG-IP® ASM Violations sub-collection"""
    def __init__(self, blocking_settings):
        super(Violations_s, self).__init__(blocking_settings)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Violation]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:blocking-settings:violations:violationcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:violations:violationstate':
                Violation
        }


class Violation(AsmResource):
    """BIG-IP® ASM Violations resource."""
    def __init__(self, violations_s):
        super(Violation, self).__init__(violations_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings:violations:violationstate'
        self._meta_data['reduction_forcing_pairs'] = []

    def create(self, **kwargs):
        """Create is not supported for Violation resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Violation resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Http_Protocols_s(Collection):
    """BIG-IP® ASM Http-Protocols sub-collection"""
    def __init__(self, blocking_settings):
        super(Http_Protocols_s, self).__init__(blocking_settings)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Http_Protocol]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings:http-protocols:http-protocolcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:http-protocols:http-protocolstate': Http_Protocol
        }


class Http_Protocol(AsmResource):
    """BIG-IP® ASM Http-Protocols  resource."""
    def __init__(self, http_protocols_s):
        super(Http_Protocol, self).__init__(http_protocols_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings:http-protocols:http-protocolstate'
        self._meta_data['reduction_forcing_pairs'] = []

    def create(self, **kwargs):
        """Create is not supported for Http Protocol resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Http Protocol resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Web_Services_Securities_s(Collection):
    """BIG-IP® ASM Web-Services-Securities sub-collection"""
    def __init__(self, blocking_settings):
        super(Web_Services_Securities_s, self).__init__(blocking_settings)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = \
            [Web_Services_Security]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings:web-services-securities:web-services-securitycollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:web-services-securities:web-services-securitystate': Web_Services_Security
        }


class Web_Services_Security(AsmResource):
    """BIG-IP® ASM Web-Services-Securities resource."""
    def __init__(self, web_serices_securities_s):
        super(Web_Services_Security, self).__init__(
            web_serices_securities_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:blocking-settings:web-services-securities:web-services-securitystate'
        self._meta_data['reduction_forcing_pairs'] = []

    def create(self, **kwargs):
        """Create is not supported for Web Services Security resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Web Services Security resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )

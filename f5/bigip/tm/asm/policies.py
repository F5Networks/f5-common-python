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

from distutils.version import LooseVersion
from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection
from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedOperation


class Policies_s(Collection):
    """BIG-IP® ASM Policies collection."""
    def __init__(self, asm):
        super(Policies_s, self).__init__(asm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Policy]
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:policystate':
                Policy}


class Policy(AsmResource):
    """BIG-IP® ASM Policies resource."""
    def __init__(self, policies_s):
        super(Policy, self).__init__(policies_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:policystate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:methods:methodcollectionstate': Methods_s,
            'tm:asm:policies:filetypes:filetypecollectionstate': Filetypes_s,
            'tm:asm:policies:cookies:cookiecollectionstate': Cookies_s,
            'tm:asm:policies:host-names:host-namecollectionstate':
                Host_Names_s,
            'tm:asm:policies:urls:urlcollectionstate': Urls_s,
            'tm:asm:policies:parameters:parametercollectionstate':
                Parameters_s,
            'tm:asm:policies:whitelist-ips:whitelist-ipcollectionstate':
                Whitelist_Ips_s,
            'tm:asm:policies:gwt-profiles:gwt-profilecollectionstate':
                Gwt_Profiles_s,
            'tm:asm:policies:json-profiles:json-profilecollectionstate':
                Json_Profiles_s,
            'tm:asm:policies:xml-profiles:xml-profilecollectionstate':
                Xml_Profiles_s,
            'tm:asm:policies:signatures:signaturecollectionstate':
                Signatures_s,
            'tm:asm:policies:signature-sets:signature-setcollectionstate':
                Signature_Sets_s,
            'tm:asm:policies:headers:headercollectionstate': Headers_s,
            'tm:asm:policies:response-pages:response-pagecollectionstate':
                Response_Pages_s,
            'tm:asm:policies:policy-builder:pbconfigstate': Policy_Builder,
            'tm:asm:policies:history-revisions:'
            'history-revisioncollectionstate': History_Revisions_s,
            'tm:asm:policies:vulnerability-assessment:'
            'vulnerability-assessmentstate': Vulnerability_Assessment
        }
        self._set_attr_reg()

    def _set_attr_reg(self):
        """Helper method.

        Appends correct attribute registry, depending on TMOS version

        """
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        attributes = self._meta_data['attribute_registry']
        v12kind = 'tm:asm:policies:blocking-settings:blocking-' \
                  'settingcollectionstate'
        v11kind = 'tm:asm:policies:blocking-settings'
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            attributes[v11kind] = Blocking_Settings
        else:
            attributes[v12kind] = Blocking_Settings


class Methods_s(Collection):
    """BIG-IP® ASM Methods sub-collection."""
    def __init__(self, policy):
        super(Methods_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Method]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:methods:methodcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:methods:methodstate':
                Method}


class Method(AsmResource):
    """BIG-IP® ASM Methods Resource."""
    def __init__(self, methods_s):
        super(Method, self).__init__(methods_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:methods:methodstate'


class Filetypes_s(Collection):
    """BIG-IP® ASM Filetypes sub-collection."""
    def __init__(self, policy):
        super(Filetypes_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Filetype]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:filetypes:filetypecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:filetypes:filetypestate':
                Filetype}


class Filetype(AsmResource):
    """BIG-IP® ASM Filetypes Resource."""
    def __init__(self, filetypes_s):
        super(Filetype, self).__init__(filetypes_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:filetypes:filetypestate'


class Cookies_s(Collection):
    """BIG-IP® ASM Cookies sub-collection."""
    def __init__(self, policy):
        super(Cookies_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Cookie]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:cookies:cookiecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:cookies:cookiestate':
                Cookie}


class Cookie(AsmResource):
    """BIG-IP® ASM Cookies Resource."""
    def __init__(self, cookies_s):
        super(Cookie, self).__init__(cookies_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:cookies:cookiestate'


class Host_Names_s(Collection):
    """BIG-IP® ASM Host-Names sub-collection."""
    def __init__(self, policy):
        super(Host_Names_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Host_Name]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:host-names:host-namecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:host-names:host-namestate':
                Host_Name}


class Host_Name(AsmResource):
    """BIG-IP® ASM Host-Names Resource."""
    def __init__(self, host_names_s):
        super(Host_Name, self).__init__(host_names_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:host-names:host-namestate'


class Blocking_Settings(UnnamedResource):
    """BIG-IP® ASM Blocking-Settings Unnamed Resource."""
    def __init__(self, policy):
        super(Blocking_Settings, self).__init__(policy)
        tmos_v = policy._meta_data['bigip']._meta_data['tmos_version']
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Evasions_s, Http_Protocols_s, Violations_s,
            Web_Services_Securities_s]

        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            # kind has changed in v12, hence we need the below
            self._meta_data['required_json_kind'] = \
                'tm:asm:policies:blocking-settings:' \
                'blocking-settingcollectionstate'
        else:
            self._meta_data['required_json_kind'] = \
                'tm:asm:policies:blocking-settings'

        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:evasions'
            ':evasioncollectionstate': Evasions_s,
            'tm:asm:policies:blocking-settings:violations:'
            'violationcollectionstate': Violations_s,
            'tm:asm:policies:blocking-settings:http-protocols:'
            'http-protocolcollectionstate': Http_Protocols_s,
            'tm:asm:policies:blocking-settings:web-services-securities:'
            'web-services-securitycollectionstate': Web_Services_Securities_s
        }


class Evasions_s(Collection):
    """BIG-IP® ASM Evasions sub-collection."""
    def __init__(self, blocking_settings):
        super(Evasions_s, self).__init__(blocking_settings)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Evasion]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:blocking-settings:evasions:evasioncollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:evasions:evasionstate':
                Evasion}


class Evasion(AsmResource):
    """BIG-IP® ASM Evasions resource."""
    def __init__(self, evasions_s):
        super(Evasion, self).__init__(evasions_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:blocking-settings:evasions:evasionstate'
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
            'tm:asm:policies:blocking-settings:violations:' \
            'violationcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:violations:violationstate':
                Violation}


class Violation(AsmResource):
    """BIG-IP® ASM Violations resource."""
    def __init__(self, violations_s):
        super(Violation, self).__init__(violations_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:blocking-settings:violations:violationstate'
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
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:blocking-settings:http-protocols:' \
            'http-protocolcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:http-protocols:'
            'http-protocolstate': Http_Protocol}


class Http_Protocol(AsmResource):
    """BIG-IP® ASM Http-Protocols  resource."""
    def __init__(self, http_protocols_s):
        super(Http_Protocol, self).__init__(http_protocols_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:blocking-settings:' \
            'http-protocols:http-protocolstate'
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
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:blocking-settings:web-services-securities:' \
            'web-services-securitycollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:blocking-settings:web-services-securities:'
            'web-services-securitystate': Web_Services_Security}


class Web_Services_Security(AsmResource):
    """BIG-IP® ASM Web-Services-Securities resource."""
    def __init__(self, web_serices_securities_s):
        super(Web_Services_Security, self).__init__(
            web_serices_securities_s)
        self._meta_data['required_json_kind'] =\
            'tm:asm:policies:blocking-settings:web-services-securities:' \
            'web-services-securitystate'
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


class Urls_s(Collection):
    """BIG-IP® ASM Urls sub-collection."""
    def __init__(self, policy):
        super(Urls_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Url]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:urls:urlcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:urls:urlstate': Url}


class Url(AsmResource):
    """BIG-IP® ASM Urls resource."""
    def __init__(self, urls_s):
        super(Url, self).__init__(urls_s)
        self._meta_data['allowed_lazy_attributes'] = [Parameters_s]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:urls:urlstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:urls:parameters:parametercollectionstate':
                Parameters_s}


class Parameters_s(object):
    """As Parameters classes are used twice as a sub-collection.


    We need to utilize __new__ method in order to keep the user
    interface consistent.

    """
    def __new__(cls, container):
        if isinstance(container, Policy):
            return ParametersCollection(container)
        if isinstance(container, Url):
            return UrlParametersCollection(container)


class UrlParametersCollection(Collection):
    """BIG-IP® ASM Urls Parameters sub-collection."""
    def __init__(self, urls_s):
        self.__class__.__name__ = 'Parameters_s'
        super(UrlParametersCollection, self).__init__(urls_s)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Parameter]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:urls:parameters:parametercollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:urls:parameters:parameterstate':
                Parameter}


class ParametersCollection(Collection):
    """BIG-IP® ASM Policies Parameters sub-collection."""
    def __init__(self, policy):
        self.__class__.__name__ = 'Parameters_s'
        super(ParametersCollection, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Parameter]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:parameters:parametercollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:parameters:parameterstate':
                Parameter}


class Parameter(object):
    """As Parameter classes are used twice as a sub-collection.


    We need to utilize __new__ method in order to keep the user
    interface consistent.
    """

    def __new__(cls, container):
        if isinstance(container, ParametersCollection):
            return ParametersResource(container)
        if isinstance(container, UrlParametersCollection):
            return UrlParametersResource(container)


class UrlParametersResource(AsmResource):
    """BIG-IP® ASM Urls Parameters resource."""
    def __init__(self, urls_s):
        self.__class__.__name__ = 'Parameter'
        super(UrlParametersResource, self).__init__(urls_s)
        self.tmos_v = urls_s._meta_data['bigip']._meta_data['tmos_version']
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:urls:parameters:parameterstate'

    def create(self, **kwargs):
        """Custom create method for v12.x and above.


        Change of behavior in v12 where the returned selfLink is different
        from target resource, requires us to append URI after object is
        created. So any modify() calls will not lead to json kind
        inconsistency when changing the resource attribute.

        See issue #844
        """
        if LooseVersion(self.tmos_v) < LooseVersion('12.0.0'):
            return self._create(**kwargs)
        else:
            new_instance = self._create(**kwargs)
            tmp_name = str(new_instance.id)
            tmp_path = new_instance._meta_data['container']._meta_data['uri']
            finalurl = tmp_path + tmp_name
            new_instance._meta_data['uri'] = finalurl
            return new_instance


class ParametersResource(AsmResource):
    """BIG-IP® ASM Urls Parameters resource."""
    def __init__(self, policy):
        self.__class__.__name__ = 'Parameter'
        super(ParametersResource, self).__init__(policy)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:parameters:parameterstate'


class Whitelist_Ips_s(Collection):
    """BIG-IP® ASM Whitelist-Ips sub-collection."""
    def __init__(self, policy):
        super(Whitelist_Ips_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Whitelist_Ip]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:whitelist-ips:whitelist-ipcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:whitelist-ips:whitelist-ipstate': Whitelist_Ip}


class Whitelist_Ip(AsmResource):
    """BIG-IP® ASM Whitelist-Ip resource."""
    def __init__(self, whitelist_ips_s):
        super(Whitelist_Ip, self).__init__(whitelist_ips_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        self._meta_data['read_only_attributes'] = ['ipMask']
        self._meta_data['required_creation_parameters'] = set(('ipAddress',))


class Gwt_Profiles_s(Collection):
    """BIG-IP® ASM Gwt-Profiles sub-collection."""
    def __init__(self, policy):
        super(Gwt_Profiles_s, self).__init__(policy)
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Gwt_Profile]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:gwt-profiles:gwt-profilecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:gwt-profiles:gwt-profilestate': Gwt_Profile}


class Gwt_Profile(AsmResource):
    """BIG-IP® ASM Gwt-Profile resource."""
    def __init__(self, gwt_profiles_s):
        super(Gwt_Profile, self).__init__(gwt_profiles_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:gwt-profiles:gwt-profilestate'


class Json_Profiles_s(Collection):
    """BIG-IP® ASM Json-Profiles sub-collection.

    Due to the bug that prevents from creating this object in 11.5.4 Final,
    I am disabling this for anything lower than 11.6.0.
    This will be subject to change at some point
    """
    def __init__(self, policy):
        super(Json_Profiles_s, self).__init__(policy)
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Json_Profile]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:json-profiles:json-profilecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:json-profiles:json-profilestate': Json_Profile}


class Json_Profile(AsmResource):
    """BIG-IP® ASM Json-Profile resource."""
    def __init__(self, json_profiles_s):
        super(Json_Profile, self).__init__(json_profiles_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:json-profiles:json-profilestate'


class Xml_Profiles_s(Collection):
    """BIG-IP® ASM Xml-Profiles sub-collection.

    Due to the bug that prevents from creating this object in 11.5.4 Final,
    I am disabling this for anything lower than 11.6.0.
    This will be subject to change at some point
    """
    def __init__(self, policy):
        super(Xml_Profiles_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Xml_Profile]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:xml-profiles:xml-profilecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:xml-profiles:xml-profilestate': Xml_Profile}


class Xml_Profile(AsmResource):
    """BIG-IP® ASM Xml-Profile resource."""
    def __init__(self, xml_profiles_s):
        super(Xml_Profile, self).__init__(xml_profiles_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:xml-profiles:xml-profilestate'


class Signatures_s(Collection):
    """BIG-IP® ASM Signatures sub-collection."""
    def __init__(self, policy):
        super(Signatures_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Signature]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:signatures:signaturecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:signatures:signaturestate': Signature}


class Signature(AsmResource):
    """BIG-IP® ASM Signature resource."""
    def __init__(self, signatures_s):
        super(Signature, self).__init__(signatures_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:signatures:signaturestate'

    def create(self, **kwargs):
        """Create is not supported for Signature resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Signature resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Signature_Sets_s(Collection):
    """BIG-IP® ASM Signature-Sets sub-collection."""
    def __init__(self, policy):
        super(Signature_Sets_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Signature_Set]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:signature-sets:signature-setcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:signature-sets:signature-setstate':
                Signature_Set}


class Signature_Set(AsmResource):
    """BIG-IP® ASM Signature-Sets resource."""
    def __init__(self, signature_sets_s):
        super(Signature_Set, self).__init__(signature_sets_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:signature-sets:signature-setstate'
        self._meta_data['required_creation_parameters'] = \
            set(('signatureSetReference',))


class Headers_s(Collection):
    """BIG-IP® ASM Headers sub-collection."""
    def __init__(self, policy):
        super(Headers_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Header]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:headers:headercollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:headers:headerstate':
                Header}


class Header(AsmResource):
    """BIG-IP® ASM Headers resource."""
    def __init__(self, headers_s):
        super(Header, self).__init__(headers_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:headers:headerstate'


class Response_Pages_s(Collection):
    """BIG-IP® ASM Response Pages sub-collection."""
    def __init__(self, policy):
        super(Response_Pages_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Response_Page]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:response-pages:response-pagecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:response-pages:response-pagestate':
                Response_Page}


class Response_Page(AsmResource):
    """BIG-IP® ASM Response Page resource."""
    def __init__(self, response_pages_s):
        super(Response_Page, self).__init__(response_pages_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:response-pages:response-pagestate'

    def create(self, **kwargs):
        """Create is not supported for Response Page resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Response Page resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Policy_Builder(UnnamedResource):
    """BIG-IP® ASM Policy Builder resource."""
    def __init__(self, policy):
        super(Policy_Builder, self).__init__(policy)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:policy-builder:pbconfigstate'
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['object_has_stats'] = False

    def update(self, **kwargs):
        """Update is not supported for Policy Builder resource

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )


class History_Revisions_s(Collection):
    """BIG-IP® ASM History Revisions sub-collection."""
    def __init__(self, policy):
        super(History_Revisions_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [History_Revision]
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:history-revisions:history-revisioncollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:history-revisions:history-revisionstate':
                History_Revision}


class History_Revision(AsmResource):
    """BIG-IP® ASM History Revision resource."""
    def __init__(self, response_pages_s):
        super(History_Revision, self).__init__(response_pages_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:history-revisions:history-revisionstate'

    def create(self, **kwargs):
        """Create is not supported for History Revision resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for History Revision resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for History Revision resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Vulnerability_Assessment(UnnamedResource):
    """BIG-IP® ASM Vulnerability Assessment resource."""
    def __init__(self, policy):
        super(Vulnerability_Assessment, self).__init__(policy)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:vulnerability-assessment:' \
            'vulnerability-assessmentstate'
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'

    def update(self, **kwargs):
        """Update is not supported for Vulnerability Assessment resource

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )

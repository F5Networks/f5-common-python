# coding=utf-8
#
# Copyright 2015-2017 F5 Networks Inc.
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

"""BIG-IP® Advanced Firewall Manager™ (AFM®) module.

REST URI
    ``http://localhost/mgmt/tm/security/dos``

GUI Path
    ``Security --> Dos Protection``

REST Kind
    ``tm:security:dos*``
"""

from f5.bigip.mixins import CheckExistenceMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import NonExtantApplication

from distutils.version import LooseVersion


class Dos(OrganizingCollection):
    """BIG-IP® DOS organizing collection."""

    def __init__(self, security):
        super(Dos, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [Profiles]


class Profiles(Collection):
    """BIG-IP® Dos Profile collection"""
    def __init__(self, dos):
        super(Profiles, self).__init__(dos)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['attribute_registry'] = \
            {'tm:security:dos:profile:profilestate': Profile}


class Profile(Resource):
    """BIG-IP® Dos Profile resource"""
    def __init__(self, profile_s):
        super(Profile, self).__init__(profile_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:profilestate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['attribute_registry'] = \
            {'tm:security:dos:profile:application:applicationcollectionstate':
                Applications,
             'tm:security:dos:profile:dos-network:dos-networkcollectionstate':
                 Dos_Networks,
             'tm:security:dos:profile:protocol-dns:'
             'protocol-dnscollectionstate': Protocol_Dns_s,
             'tm:security:dos:profile:protocol-sip:protocol'
             '-sipcollectionstate': Protocol_Sips}


class Applications(Collection):
    """BIG-IP® Dos Profile Application sub-collection"""
    def __init__(self, profile):
        super(Applications, self).__init__(profile)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:application:applicationcollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Application]
        self._meta_data['attribute_registry'] = \
            {'tm:security:dos:profile:application:applicationstate':
                Application}


class Application(Resource, CheckExistenceMixin):
    """BIG-IP® Dos Profile Application resource"""
    def __init__(self, applications):
        super(Application, self).__init__(applications)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:application:applicationstate'
        self.tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']

    def load(self, **kwargs):
        """Custom load method to address issue in 11.6.0 Final,

        where non existing objects would be True.
        """
        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._load_11_6(**kwargs)
        else:
            return super(Application, self)._load(**kwargs)

    def _load_11_6(self, **kwargs):
        """Must check if rule actually exists before proceeding with load."""
        if self._check_existence_by_collection(self._meta_data['container'],
                                               kwargs['name']):
            return super(Application, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the ' \
              'device.'.format(kwargs['name'])
        raise NonExtantApplication(msg)

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """

        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Application, self)._load(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(
            self._meta_data['container'], kwargs['name'])


class Dos_Networks(Collection):
    """BIG-IP® Dos Profile Dos Networks sub-collection"""
    def __init__(self, profile):
        super(Dos_Networks, self).__init__(profile)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:dos-network:dos-networkcollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Dos_Network]
        self._meta_data['attribute_registry'] = \
            {'tm:security:dos:profile:dos-network:dos-networkstate':
                Dos_Network}


class Dos_Network(Resource, CheckExistenceMixin):
    """BIG-IP® Dos Profile Dos Network resource"""
    def __init__(self, dos_networks):
        super(Dos_Network, self).__init__(dos_networks)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:dos-network:dos-networkstate'
        self.tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']

    def load(self, **kwargs):
        """Custom load method to address issue in 11.6.0 Final,

        where non existing objects would be True.
        """
        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._load_11_6(**kwargs)
        else:
            return super(Dos_Network, self)._load(**kwargs)

    def _load_11_6(self, **kwargs):
        """Must check if rule actually exists before proceeding with load."""
        if self._check_existence_by_collection(self._meta_data['container'],
                                               kwargs['name']):
            return super(Dos_Network, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the ' \
              'device.'.format(kwargs['name'])
        raise NonExtantApplication(msg)

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """

        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Dos_Network, self)._load(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(
            self._meta_data['container'], kwargs['name'])


class Protocol_Dns_s(Collection):
    """BIG-IP® Dos Profile Protocol Dns sub-collection"""
    def __init__(self, profile):
        super(Protocol_Dns_s, self).__init__(profile)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:protocol-dns:protocol-dnscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Protocol_Dns]
        self._meta_data['attribute_registry'] = \
            {'tm:security:dos:profile:protocol-dns:protocol-dnsstate':
                Protocol_Dns}


class Protocol_Dns(Resource, CheckExistenceMixin):
    """BIG-IP® Dos Profile Protocol Dns resource"""
    def __init__(self, protocol_dns_s):
        super(Protocol_Dns, self).__init__(protocol_dns_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:protocol-dns:protocol-dnsstate'
        self.tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']

    def load(self, **kwargs):
        """Custom load method to address issue in 11.6.0 Final,

        where non existing objects would be True.
        """
        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._load_11_6(**kwargs)
        else:
            return super(Protocol_Dns, self)._load(**kwargs)

    def _load_11_6(self, **kwargs):
        """Must check if rule actually exists before proceeding with load."""
        if self._check_existence_by_collection(self._meta_data['container'],
                                               kwargs['name']):
            return super(Protocol_Dns, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the ' \
              'device.'.format(kwargs['name'])
        raise NonExtantApplication(msg)

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """

        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Protocol_Dns, self)._load(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(
            self._meta_data['container'], kwargs['name'])


class Protocol_Sips(Collection):
    """BIG-IP® Dos Profile Protocol Sip sub-collection"""
    def __init__(self, profile):
        super(Protocol_Sips, self).__init__(profile)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:protocol-sip:protocol-sipcollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Protocol_Sip]
        self._meta_data['attribute_registry'] = \
            {'tm:security:dos:profile:protocol-sip:protocol-sipstate':
                Protocol_Sip}


class Protocol_Sip(Resource, CheckExistenceMixin):
    """BIG-IP® Dos Profile Protocol Sip resource"""
    def __init__(self, protocol_sips):
        super(Protocol_Sip, self).__init__(protocol_sips)
        self._meta_data['required_json_kind'] = \
            'tm:security:dos:profile:protocol-sip:protocol-sipstate'
        self.tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']

    def load(self, **kwargs):
        """Custom load method to address issue in 11.6.0 Final,

        where non existing objects would be True.
        """
        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._load_11_6(**kwargs)
        else:
            return super(Protocol_Sip, self)._load(**kwargs)

    def _load_11_6(self, **kwargs):
        """Must check if rule actually exists before proceeding with load."""
        if self._check_existence_by_collection(self._meta_data['container'],
                                               kwargs['name']):
            return super(Protocol_Sip, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the ' \
              'device.'.format(kwargs['name'])
        raise NonExtantApplication(msg)

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """

        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Protocol_Sip, self)._load(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(
            self._meta_data['container'], kwargs['name'])

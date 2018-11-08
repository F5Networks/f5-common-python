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
    ``http://localhost/mgmt/tm/security/scrubber``

GUI Path
    ``Security --> Option --> Network Firewall -->  External Redirection
    --> Scrubbing Profile``

REST Kind
    ``tm:security:scrubbercollectionstate:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Scrubber(OrganizingCollection):
    """BIG-IP® AFM® Scrubber organizing collection."""

    def __init__(self, security):
        super(Scrubber, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Profile_s]


class Profile_s(Collection):
    """BIG-IP® AFM® Scrubber Profile collection"""

    def __init__(self, scrubber):
        super(Profile_s, self).__init__(scrubber)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['attribute_registry'] = \
            {'tm:security:scrubber:profile:profilestate':
                Profile}


class Profile(Resource):
    """BIG-IP® AFM® Scrubber Profile resource"""

    def __init__(self, profile_s):
        super(Profile, self).__init__(profile_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:scrubber:profile:profilestate'
        self._meta_data['required_load_parameters'].update(('partition', 'name'))

        self._meta_data['attribute_registry'] = \
            {'tm:security:scrubber:profile:scrubber-rt-domain:scrubber_rt_domaincollectionstate': Scrubber_Rt_Domain_s,
             'tm:security:scrubber:profile:scrubber-categories:scrubber-categoriescollectionstate': Scrubber_Categories_s,
             'tm:security:scrubber:profile:scrubber-virtual-server:scrubber-virtual-servercollectionstate': Scrubber_Virtual_Server_s,
             'tm:security:scrubber:profile:scrubber-netflow-protected-server:scrubber-netflow-protected-servercollectionstate':
                Scrubber_Netflow_Protected_Server_s}

        self._meta_data['allowed_lazy_attributes'] = [
            Scrubber_Rt_Domain_s,
            Scrubber_Virtual_Server_s,
            Scrubber_Categories_s,
            Scrubber_Netflow_Protected_Server_s]


class Scrubber_Rt_Domain_s(Collection):
    """BIG-IP® AFM® Scrubber Profile Route Domain collection"""

    def __init__(self, profile):
        super(Scrubber_Rt_Domain_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Scrubber_Rt_Domain]
        self._meta_data['attribute_registry'] = \
            {'tm:security:scrubber:profile:scrubber-rt-domain:scrubber-rt-domainstate':
                Scrubber_Rt_Domain}


class Scrubber_Rt_Domain(Resource):
    """BIG-IP® AFM® Scrubber Profile Route Domain resource"""

    def __init__(self, scrubber_rt_domain_s):
        super(Scrubber_Rt_Domain, self).__init__(scrubber_rt_domain_s)
        self._meta_data['allowed_lazy_attributes'] = [Scrubber_Rd_Network_Prefix_s]
        self._meta_data['required_json_kind'] = \
            'tm:security:scrubber:profile:scrubber-rt-domain:scrubber-rt-domainstate'
        self._meta_data['attribute_registry'] = \
            {'tm:security:scrubber:profile:scrubber-rt-domain:scrubber-rd-network-prefix:scrubber-rd-network-prefixcollectionstate':
                Scrubber_Rd_Network_Prefix_s}
        self._meta_data['required_creation_parameters'].update(('name', 'routeDomain'))


class Scrubber_Rd_Network_Prefix_s(Collection):
    """BIG-IP® AFM® Scrubber Rd Network Prefix collection"""

    def __init__(self, scrubber_rt_domain):
        super(Scrubber_Rd_Network_Prefix_s, self).__init__(scrubber_rt_domain)
        self._meta_data['allowed_lazy_attributes'] = [Scrubber_Rd_Network_Prefix]
        self._meta_data['attribute_registry'] = \
            {'tm:security:scrubber:profile:scrubber-rt-domain:scrubber-rd-network-prefix:scrubber-rd-network-prefixstate':
                Scrubber_Rd_Network_Prefix}


class Scrubber_Rd_Network_Prefix(Resource):
    """BIG-IP® AFM® Scrubber Rd Network Prefix resource"""

    def __init__(self, scrubber_rd_network_prefix_s):
        super(Scrubber_Rd_Network_Prefix, self).__init__(scrubber_rd_network_prefix_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:scrubber:profile:scrubber-rt-domain:scrubber-rd-network-prefix:scrubber-rd-network-prefixstate'
        self._meta_data['required_creation_parameters'].update(('name', 'nextHop', 'dstIp', 'mask'))


class Scrubber_Virtual_Server_s(Collection):
    """BIG-IP® AFM® Scrubber Profile Virtual Server collection"""

    def __init__(self, profile):
        super(Scrubber_Virtual_Server_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Scrubber_Virtual_Server]
        self._meta_data['attribute_registry'] = \
            {'tm:security:scrubber:profile:scrubber-virtual-server:scrubber-virtual-serverstate':
                Scrubber_Virtual_Server}


class Scrubber_Virtual_Server(Resource):
    """BIG-IP® AFM® Scrubber Profile Virtual Server resource"""

    def __init__(self, scrubber_virtual_server_s):
        super(Scrubber_Virtual_Server, self).__init__(scrubber_virtual_server_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:scrubber:profile:scrubber-virtual-server:scrubber-virtual-serverstate'
        self._meta_data['required_creation_parameters'].update(('name', 'vsName'))


class Scrubber_Categories_s(Collection):
    """BIG-IP® AFM® Scrubber Profile Categories collection"""

    def __init__(self, profile):
        super(Scrubber_Categories_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Scrubber_Categories]
        self._meta_data['attribute_registry'] = \
            {'tm:security:scrubber:profile:scrubber-categories:scrubber-categoriesstate':
                Scrubber_Categories}


class Scrubber_Categories(Resource):
    """BIG-IP® AFM® Scrubber Profile Categories resource"""

    def __init__(self, scrubber_categories_s):
        super(Scrubber_Categories, self).__init__(scrubber_categories_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:scrubber:profile:scrubber-categories:scrubber-categoriesstate'
        self._meta_data['required_creation_parameters'].update(('name', 'blacklistCategory', 'routeDomainName'))


class Scrubber_Netflow_Protected_Server_s(Collection):
    """BIG-IP® AFM® Scrubber Profile Netflow Protected Server collection"""

    def __init__(self, profile):
        super(Scrubber_Netflow_Protected_Server_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Scrubber_Netflow_Protected_Server]
        self._meta_data['attribute_registry'] = \
            {'tm:security:scrubber:profile:scrubber-netflow-protected-server:scrubber-netflow-protected-serverstate':
                Scrubber_Netflow_Protected_Server}


class Scrubber_Netflow_Protected_Server(Resource):
    """BIG-IP® AFM® Scrubber Profile Netflow Protected Server resource"""

    def __init__(self, scrubber_netflow_protected_server_s):
        super(Scrubber_Netflow_Protected_Server, self).__init__(scrubber_netflow_protected_server_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:scrubber:profile:scrubber-netflow-protected-server:scrubber-netflow-protected-serverstate'
        self._meta_data['required_creation_parameters'].update(('name', 'npsName'))

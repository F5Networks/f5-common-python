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
    ``http://localhost/mgmt/tm/security/ip-intelligence``

GUI Path
    ``Security --> Network Firewall --> IP Intelligence``

REST Kind
    ``tm:security:ip-intelligence:*``
"""
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.bigip.resource import UnnamedResource


class Ip_Intelligence(OrganizingCollection):
    """BIG-IP® AFM® Firewall IP Intelligence organizing collection."""

    def __init__(self, security):
        super(Ip_Intelligence, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Feed_list_s,
            Policy_s,
            Blacklist_Categorys,
            Global_Policy]


class Feed_list_s(Collection):
    """BIG-IP® AFM® IP Intelligence Feedlist collection"""

    def __init__(self, policy):
        super(Feed_list_s, self).__init__(policy)
        self._meta_data['allowed_lazy_attributes'] = [Feed_list]
        self._meta_data['attribute_registry'] = \
            {'tm:security:ip-intelligence:feed-list:feed-liststate':
                Feed_list}


class Feed_list(Resource):
    """BIG-IP® AFM® IP-INtelligence Feedlist resource"""

    def __init__(self, feed_list_s):
        super(Feed_list, self).__init__(feed_list_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:ip-intelligence:feed-list:feed-liststate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))


class Policy_s(Collection):
    """BIG-IP® AFM® IP-Intelligence Policy collection"""

    def __init__(self, ip_intelligence):
        super(Policy_s, self).__init__(ip_intelligence)
        self._meta_data['allowed_lazy_attributes'] = [Policy]
        self._meta_data['attribute_registry'] = \
            {'tm:security:ip-intelligence:policy:policystate':
                Policy}


class Policy(Resource):
    """BIG-IP® AFM® IP-Intelligence Policy resource"""

    def __init__(self, policy_s):
        super(Policy, self).__init__(policy_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:ip-intelligence:policy:policystate'
        self._meta_data['allowed_lazy_attributes'] = [Feed_list_s]
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['attribute_registry'] = \
            {'tm:security:ip-intelligence:feed-list:feed-listcollectionstate':
                Feed_list_s}


class Blacklist_Categorys(Collection):
    """BIG-IP® AFM® IP-Intelligence Blacklist Categories collection"""

    def __init__(self, ip_intelligence):
        super(Blacklist_Categorys, self).__init__(ip_intelligence)
        self._meta_data['allowed_lazy_attributes'] = [Blacklist_Category]
        self._meta_data['attribute_registry'] = \
            {'tm:security:ip-intelligence:blacklist-category:blacklist-categorystate':
                Blacklist_Category}


class Blacklist_Category(Resource):
    """BIG-IP® AFM® IP-Intelligence Blacklist Category resource"""

    def __init__(self, blacklist_categorys):
        super(Blacklist_Category, self).__init__(blacklist_categorys)
        self._meta_data['required_json_kind'] = \
            'tm:security:ip-intelligence:blacklist-category:blacklist-categorystate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))


class Global_Policy(UnnamedResource):
    """BIG-IP® AFM® Global Rules resource"""
    def __init__(self, global_policy):
        super(Global_Policy, self).__init__(global_policy)
        self._meta_data['required_json_kind'] = \
            'tm:security:ip-intelligence:global-policy:global-policystate'

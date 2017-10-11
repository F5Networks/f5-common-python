# coding=utf-8
#
#  Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager (LTM) policy module.

REST URI
    ``http://localhost/mgmt/tm/ltm/policy``

GUI Path
    ``Local Traffic --> policy``

REST Kind
    ``tm:ltm:policy:*``
"""

from f5.bigip.mixins import CheckExistenceMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import DraftPolicyNotSupportedInTMOSVersion
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import NonExtantPolicyRule
from f5.sdk_exception import OperationNotSupportedOnPublishedPolicy

from distutils.version import LooseVersion
import logging

logger = logging.getLogger(__name__)


class Policys(Collection):
    """BIG-IP® LTM policy collection."""
    def __init__(self, ltm):
        super(Policys, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Policy]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:policystate': Policy}


class Policy(Resource):
    """BIG-IP® LTM policy resource."""
    def __init__(self, policy_s):
        super(Policy, self).__init__(policy_s)
        self._meta_data['allowed_lazy_attributes'] = [Rules_s]
        self._meta_data['required_json_kind'] = 'tm:ltm:policy:policystate'
        self._meta_data['required_creation_parameters'].update(('strategy',))
        temp = {'tm:ltm:policy:rules:rulescollectionstate': Rules_s}
        self._meta_data['attribute_registry'] = temp
        self._meta_data['optional_parameters'] = {'rules': ['description']}

    def _filter_version_specific_options(self, tmos_ver, **kwargs):
        '''Filter version-specific optional parameters

        Some optional parameters only exist in v12.1.0 and greater,
        filter these out for earlier versions to allow backward comatibility.
        '''

        if LooseVersion(tmos_ver) < LooseVersion('12.1.0'):
            for k, parms in self._meta_data['optional_parameters'].items():
                for r in kwargs.get(k, []):
                    for parm in parms:
                        value = r.pop(parm, None)
                        if value is not None:
                            logger.info(
                                "Policy parameter %s:%s is invalid for v%s",
                                k, parm, tmos_ver)

    def _create(self, **kwargs):
        '''Allow creation of draft policy and ability to publish a draft

        Draft policies only exist in 12.1.0 and greater versions of TMOS.
        But there must be a method to create a draft, then publish it.

        :raises: MissingRequiredCreationParameter
        '''

        tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']
        legacy = kwargs.pop('legacy', False)
        publish = kwargs.pop('publish', False)
        self._filter_version_specific_options(tmos_ver, **kwargs)
        if LooseVersion(tmos_ver) < LooseVersion('12.1.0'):
            return super(Policy, self)._create(**kwargs)
        else:
            if legacy:
                return super(Policy, self)._create(legacy=True, **kwargs)
            else:
                if 'subPath' not in kwargs:
                    msg = "The keyword 'subPath' must be specified when " \
                        "creating draft policy in TMOS versions >= 12.1.0. " \
                        "Try and specify subPath as 'Drafts'."
                    raise MissingRequiredCreationParameter(msg)
                self = super(Policy, self)._create(**kwargs)
                if publish:
                    self.publish()
                return self

    def _modify(self, **patch):
        '''Modify only draft or legacy policies

        Published policies cannot be modified
        :raises: OperationNotSupportedOnPublishedPolicy
        '''

        legacy = patch.pop('legacy', False)
        tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']
        self._filter_version_specific_options(tmos_ver, **patch)
        if 'Drafts' not in self._meta_data['uri'] and \
                LooseVersion(tmos_ver) >= LooseVersion('12.1.0') and \
                not legacy:
            msg = 'Modify operation not allowed on a published policy.'
            raise OperationNotSupportedOnPublishedPolicy(msg)
        super(Policy, self)._modify(**patch)

    def _update(self, **kwargs):
        '''Update only draft or legacy policies

        Published policies cannot be updated
        :raises: OperationNotSupportedOnPublishedPolicy
        '''

        legacy = kwargs.pop('legacy', False)
        tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']
        self._filter_version_specific_options(tmos_ver, **kwargs)
        if 'Drafts' not in self._meta_data['uri'] and \
                LooseVersion(tmos_ver) >= LooseVersion('12.1.0') and \
                not legacy:
            msg = 'Update operation not allowed on a published policy.'
            raise OperationNotSupportedOnPublishedPolicy(msg)
        super(Policy, self)._update(**kwargs)

    def publish(self, **kwargs):
        '''Publishing a draft policy is only applicable in TMOS 12.1 and up.

        This operation updates the meta_data['uri'] of the existing object
        and effectively moves a draft into a published state on the device.
        The self object is also updated with the response from a GET to the
        device.

        :raises: PolicyNotDraft
        '''

        assert 'Drafts' in self._meta_data['uri']
        assert self.status.lower() == 'draft'
        base_uri = self._meta_data['container']._meta_data['uri']
        requests_params = self._handle_requests_params(kwargs)
        session = self._meta_data['bigip']._meta_data['icr_session']
        if 'command' not in kwargs:
            kwargs['command'] = 'publish'
        if 'Drafts' not in self.name:
            kwargs['name'] = self.fullPath
        session.post(base_uri, json=kwargs, **requests_params)
        get_kwargs = {
            'name': self.name, 'partition': self.partition,
            'uri_as_parts': True
        }
        response = session.get(base_uri, **get_kwargs)
        json_data = response.json()
        self._local_update(json_data)
        self._activate_URI(json_data['selfLink'])

    def draft(self, **kwargs):
        '''Allows for easily re-drafting a policy

        After a policy has been created, it was not previously possible
        to re-draft the published policy. This method makes it possible
        for a user with existing, published, policies to create drafts
        from them so that they are modifiable.
        See https://github.com/F5Networks/f5-common-python/pull/1099

        :param kwargs:
        :return:
        '''
        tmos_ver = self._meta_data['bigip']._meta_data['tmos_version']
        legacy = kwargs.pop('legacy', False)
        if LooseVersion(tmos_ver) < LooseVersion('12.1.0') or legacy:
            raise DraftPolicyNotSupportedInTMOSVersion(
                "Drafting on this version of BIG-IP is not supported"
            )
        kwargs = dict(
            createDraft=True
        )
        super(Policy, self)._modify(**kwargs)

        get_kwargs = {
            'name': self.name,
            'partition': self.partition,
            'uri_as_parts': True,
            'subPath': 'Drafts'
        }
        base_uri = self._meta_data['container']._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']
        response = session.get(base_uri, **get_kwargs)
        json_data = response.json()
        self._local_update(json_data)
        self._activate_URI(json_data['selfLink'])


class Rules_s(Collection):
    """BIG-IP® LTM policy rules sub-collection."""
    def __init__(self, policy):
        super(Rules_s, self).__init__(policy)
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:rules:rulesstate': Rules}
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:rulescollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Rules]


class Rules(Resource, CheckExistenceMixin):
    """BIG-IP® LTM policy rules sub-collection resource."""
    def __init__(self, rules_s):
        super(Rules, self).__init__(rules_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:rulesstate'
        temp = {'tm:ltm:policy:rules:actions:actionscollectionstate':
                Actions_s,
                'tm:ltm:policy:rules:conditions:conditionscollectionstate':
                Conditions_s}
        self._meta_data['attribute_registry'] = temp

    def _load(self, **kwargs):
        """Must check if rule actually exists before proceeding with load."""

        if self._check_existence_by_collection(
                self._meta_data['container'], kwargs['name']):
            return super(Rules, self)._load(**kwargs)
        msg = 'The rule named, {}, does not exist on the device.'.format(
            kwargs['name'])
        raise NonExtantPolicyRule(msg)

    def exists(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(
            self._meta_data['container'], kwargs['name'])


class Actions_s(Collection):
    """BIG-IP® LTM policy actions sub-collection."""
    def __init__(self, rules):
        super(Actions_s, self).__init__(rules)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:actions:actionscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Actions]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:rules:actions:actionsstate': Actions}


class Actions(Resource):
    """BIG-IP® LTM policy actions sub-collection resource."""
    def __init__(self, actions_s):
        super(Actions, self).__init__(actions_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:actions:actionsstate'


class Conditions_s(Collection):
    """BIG-IP® LTM policy conditions sub-collection."""
    def __init__(self, rules):
        super(Conditions_s, self).__init__(rules)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:conditions:conditionscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Conditions]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:rules:conditions:conditionsstate': Conditions}


class Conditions(Resource):
    """BIG-IP® LTM policy conditions sub-collection resource."""
    def __init__(self, conditions_s):
        super(Conditions, self).__init__(conditions_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:conditions:conditionsstate'

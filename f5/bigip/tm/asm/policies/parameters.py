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


class UrlParametersCollection(Collection):
    """BIG-IP® ASM Urls Parameters sub-collection."""
    def __init__(self, urls_s):
        self.__class__.__name__ = 'Parameters_s'
        super(UrlParametersCollection, self).__init__(urls_s)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Parameter]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:urls:parameters:parametercollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:urls:parameters:parameterstate': Parameter
        }


class ParametersCollection(Collection):
    """BIG-IP® ASM Policies Parameters sub-collection."""
    def __init__(self, policy):
        self.__class__.__name__ = 'Parameters_s'
        super(ParametersCollection, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Parameter]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:parameters:parametercollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:parameters:parameterstate': Parameter
        }


class Parameters_s(object):
    """As Parameters classes are used twice as a sub-collection.


    We need to utilize __new__ method in order to keep the user
    interface consistent.

    """
    def __new__(cls, container):
        from f5.bigip.tm.asm.policies import Policy
        from f5.bigip.tm.asm.policies.urls import Url
        if isinstance(container, Policy):
            return ParametersCollection(container)
        if isinstance(container, Url):
            return UrlParametersCollection(container)


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
        self._meta_data['required_json_kind'] = 'tm:asm:policies:urls:parameters:parameterstate'

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
        self._meta_data['required_json_kind'] = 'tm:asm:policies:parameters:parameterstate'

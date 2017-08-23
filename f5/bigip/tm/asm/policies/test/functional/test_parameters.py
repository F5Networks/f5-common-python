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
#

import os
import pytest
import tempfile

from f5.bigip.tm.asm.policies.parameters import UrlParametersResource
from f5.bigip.tm.asm.policies.parameters import UrlParametersCollection
from f5.bigip.tm.asm.policies.parameters import ParametersCollection
from f5.bigip.tm.asm.policies.parameters import ParametersResource
from f5.bigip.tm.asm.policies.parameters import Parameters_s
from f5.bigip.tm.asm.policies.parameters import Parameter
from requests.exceptions import HTTPError
from six import iterkeys


class TestParametersCol(object):
    def test_new_method(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url_res = policy.urls_s.url.create(name=name)
        kind_pol = 'tm:asm:policies:parameters:parameterstate'
        kind_url = 'tm:asm:policies:urls:parameters:parameterstate'

        policyparam = Parameters_s(policy)
        test_meta_pol = policyparam._meta_data['attribute_registry']
        test_meta_pol2 = policyparam._meta_data['allowed_lazy_attributes']
        assert isinstance(policyparam, ParametersCollection)
        assert hasattr(policyparam, 'parameter')
        assert policyparam.__class__.__name__ == 'Parameters_s'
        assert kind_pol in list(iterkeys(test_meta_pol))
        assert Parameter in test_meta_pol2

        urlparam = Parameters_s(url_res)
        test_meta_url = urlparam._meta_data['attribute_registry']
        test_meta_url2 = urlparam._meta_data['allowed_lazy_attributes']
        assert isinstance(urlparam, UrlParametersCollection)
        assert hasattr(urlparam, 'parameter')
        assert urlparam.__class__.__name__ == 'Parameters_s'
        assert kind_url in list(iterkeys(test_meta_url))
        assert Parameter in test_meta_url2
        url_res.delete()


class TestParametersRes(object):
    def test_new_method(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url_res = policy.urls_s.url.create(name=name)
        kind_pol = 'tm:asm:policies:parameters:parameterstate'
        kind_url = 'tm:asm:policies:urls:parameters:parameterstate'

        policyparam = Parameter((Parameters_s(policy)))
        test_meta_pol = policyparam._meta_data['required_json_kind']
        assert isinstance(policyparam, ParametersResource)
        assert policyparam.__class__.__name__ == 'Parameter'
        assert kind_pol in test_meta_pol

        urlparam = Parameter((Parameters_s(url_res)))
        test_meta_url = urlparam._meta_data['required_json_kind']
        assert isinstance(urlparam, UrlParametersResource)
        assert urlparam.__class__.__name__ == 'Parameter'
        assert kind_url in test_meta_url
        url_res.delete()


class TestUrlParameters(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name)
        param1 = url.parameters_s.parameter.create(name=name + '_parameter')
        assert param1.kind == 'tm:asm:policies:urls:parameters:parameterstate'
        assert param1.name == name + '_parameter'
        assert param1.type == 'explicit'
        assert param1.sensitiveParameter is False
        param1.delete()
        url.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name)
        param1 = url.parameters_s.parameter.create(
            name=name + '_parameter',
            sensitiveParameter=True
        )
        assert param1.kind == 'tm:asm:policies:urls:parameters:parameterstate'
        assert param1.name == name + '_parameter'
        assert param1.type == 'explicit'
        assert param1.sensitiveParameter is True
        param1.delete()
        url.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name)
        param1 = url.parameters_s.parameter.create(name=name + '_parameter')
        param2 = url.parameters_s.parameter.load(id=param1.id)
        assert param1.kind == param2.kind
        assert param1.name == param2.name
        assert param1.sensitiveParameter == param2.sensitiveParameter
        param2.modify(sensitiveParameter=True)
        assert param1.sensitiveParameter is False
        assert param2.sensitiveParameter is True
        param1.refresh()
        assert param1.sensitiveParameter is True
        param1.delete()
        url.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name)
        param1 = url.parameters_s.parameter.create(name=name + '_parameter')
        idhash = str(param1.id)
        param1.delete()
        with pytest.raises(HTTPError) as err:
            url.parameters_s.parameter.load(id=idhash)
        assert err.value.response.status_code == 404
        url.delete()

    def test_load_no_object(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name)
        with pytest.raises(HTTPError) as err:
            url.parameters_s.parameter.load(id='Lx3553-321')
        assert err.value.response.status_code == 404
        url.delete()

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name)
        param1 = url.parameters_s.parameter.create(name=name + '_parameter')
        assert param1.kind == 'tm:asm:policies:urls:parameters:parameterstate'
        assert param1.name == name + '_parameter'
        assert param1.type == 'explicit'
        assert param1.sensitiveParameter is False
        param1.modify(sensitiveParameter=True)
        assert param1.sensitiveParameter is True
        param2 = url.parameters_s.parameter.load(id=param1.id)
        assert param1.name == param2.name
        assert param1.selfLink == param2.selfLink
        assert param1.kind == param2.kind
        assert param1.sensitiveParameter == param2.sensitiveParameter
        param1.delete()
        url.delete()

    def test_url_parameters_subcollection(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name)
        param1 = url.parameters_s.parameter.create(name=name + '_parameter')
        assert param1.kind == 'tm:asm:policies:urls:parameters:parameterstate'
        assert param1.name == name + '_parameter'
        assert param1.type == 'explicit'
        assert param1.sensitiveParameter is False

        cc = url.parameters_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], UrlParametersResource)
        param1.delete()
        url.delete()

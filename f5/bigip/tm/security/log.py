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

from distutils.version import LooseVersion
from f5.bigip.mixins import CheckExistenceMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from requests.exceptions import HTTPError
from requests import Response


class Log(OrganizingCollection):
    def __init__(self, security):
        super(Log, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Profiles,
        ]


class Profiles(Collection):
    def __init__(self, log):
        super(Profiles, self).__init__(log)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['attribute_registry'] = {
            'tm:security:log:profile:profilestate': Profile
        }


class Profile(Resource):
    def __init__(self, profiles):
        super(Profile, self).__init__(profiles)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:profilestate'
        self._meta_data['allowed_lazy_attributes'] = []
        self._meta_data['attribute_registry'] = {
            'tm:security:log:profile:application:applicationcollectionstate': Applications,
            'tm:security:log:profile:network:networkcollectionstate': Networks,
            'tm:security:log:profile:protocol-dns:protocol-dnscollectionstate': Protocol_Dns_s,
            'tm:security:log:profile:protocol-sip:protocol-sipcollectionstate': Protocol_Sips,
        }


class Applications(Collection):
    def __init__(self, profile):
        super(Applications, self).__init__(profile)
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:application:applicationcollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Application]
        self._meta_data['attribute_registry'] = {
            'tm:security:log:profile:application:applicationstate': Application
        }


class Application(Resource, CheckExistenceMixin):
    def __init__(self, applications):
        super(Application, self).__init__(applications)
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:application:applicationstate'
        self.tmos_ver = self._meta_data['bigip'].tmos_version

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
        if self._check_existence_by_collection(self._meta_data['container'], kwargs['name']):
            return super(Application, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the device.'.format(kwargs['name'])
        resp = Response()
        resp.status_code = 404
        ex = HTTPError(msg, response=resp)
        raise ex

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """
        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Application, self)._exists(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(self._meta_data['container'], kwargs['name'])

    def modify(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._modify(**kwargs)

    def update(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._update(**kwargs)

    def delete(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._delete(**kwargs)

    def create(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._create(**kwargs)

    def _mutate_name(self, kwargs):
        partition = kwargs.pop('partition', None)
        if partition is not None:
            kwargs['name'] = '/{0}/{1}'.format(partition, kwargs['name'])
        return kwargs


class Networks(Collection):
    def __init__(self, profile):
        super(Networks, self).__init__(profile)
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:application:applicationcollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Network]
        self._meta_data['attribute_registry'] = {
            'tm:security:log:profile:network:networkstate': Network
        }


class Network(Resource, CheckExistenceMixin):
    def __init__(self, networks):
        super(Network, self).__init__(networks)
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:network:networkstate'
        self.tmos_ver = self._meta_data['bigip'].tmos_version

    def load(self, **kwargs):
        """Custom load method to address issue in 11.6.0 Final,

        where non existing objects would be True.
        """
        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._load_11_6(**kwargs)
        else:
            return super(Network, self)._load(**kwargs)

    def _load_11_6(self, **kwargs):
        """Must check if rule actually exists before proceeding with load."""
        if self._check_existence_by_collection(self._meta_data['container'], kwargs['name']):
            return super(Network, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the device.'.format(kwargs['name'])
        resp = Response()
        resp.status_code = 404
        ex = HTTPError(msg, response=resp)
        raise ex

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """

        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Network, self)._exists(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(self._meta_data['container'], kwargs['name'])

    def modify(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._modify(**kwargs)

    def update(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._update(**kwargs)

    def delete(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._delete(**kwargs)

    def create(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._create(**kwargs)

    def _mutate_name(self, kwargs):
        partition = kwargs.pop('partition', None)
        if partition is not None:
            kwargs['name'] = '/{0}/{1}'.format(partition, kwargs['name'])
        return kwargs


class Protocol_Dns_s(Collection):
    def __init__(self, profile):
        super(Protocol_Dns_s, self).__init__(profile)
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:protocol-dns:protocol-dnscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Protocol_Dns]
        self._meta_data['attribute_registry'] = {
            'tm:security:log:profile:protocol-dns:protocol-dnsstate': Protocol_Dns
        }


class Protocol_Dns(Resource, CheckExistenceMixin):
    def __init__(self, protocol_dns_s):
        super(Protocol_Dns, self).__init__(protocol_dns_s)
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:protocol-dns:protocol-dnsstate'
        self.tmos_ver = self._meta_data['bigip'].tmos_version

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
        if self._check_existence_by_collection(self._meta_data['container'], kwargs['name']):
            return super(Protocol_Dns, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the device.'.format(kwargs['name'])
        resp = Response()
        resp.status_code = 404
        ex = HTTPError(msg, response=resp)
        raise ex

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """

        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Protocol_Dns, self)._exists(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(self._meta_data['container'], kwargs['name'])

    def modify(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._modify(**kwargs)

    def update(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._update(**kwargs)

    def delete(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._delete(**kwargs)

    def create(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._create(**kwargs)

    def _mutate_name(self, kwargs):
        partition = kwargs.pop('partition', None)
        if partition is not None:
            kwargs['name'] = '/{0}/{1}'.format(partition, kwargs['name'])
        return kwargs


class Protocol_Sips(Collection):
    def __init__(self, profile):
        super(Protocol_Sips, self).__init__(profile)
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:protocol-sip:protocol-sipcollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Protocol_Sip]
        self._meta_data['attribute_registry'] = {
            'tm:security:log:profile:protocol-sip:protocol-sipstate': Protocol_Sip
        }


class Protocol_Sip(Resource, CheckExistenceMixin):
    def __init__(self, protocol_sips):
        super(Protocol_Sip, self).__init__(protocol_sips)
        self._meta_data['required_json_kind'] = 'tm:security:log:profile:protocol-sip:protocol-sipstate'
        self.tmos_ver = self._meta_data['bigip'].tmos_version

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
        if self._check_existence_by_collection(self._meta_data['container'], kwargs['name']):
            return super(Protocol_Sip, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the device.'.format(kwargs['name'])
        resp = Response()
        resp.status_code = 404
        ex = HTTPError(msg, response=resp)
        raise ex

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """

        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Protocol_Sip, self)._exists(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(self._meta_data['container'], kwargs['name'])

    def modify(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._modify(**kwargs)

    def update(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._update(**kwargs)

    def delete(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._delete(**kwargs)

    def create(self, **kwargs):
        kwargs = self._mutate_name(kwargs)
        return self._create(**kwargs)

    def _mutate_name(self, kwargs):
        partition = kwargs.pop('partition', None)
        if partition is not None:
            kwargs['name'] = '/{0}/{1}'.format(partition, kwargs['name'])
        return kwargs

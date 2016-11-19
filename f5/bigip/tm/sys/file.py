# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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
"""BIG-IP® system file module

REST URI
    ``http://localhost/mgmt/tm/sys/file``

GUI Path
    N/A

REST Kind
    ``tm:sys:file:*``
"""

from distutils.version import LooseVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedMethod


class File(OrganizingCollection):
    def __init__(self, sys):
        super(File, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Data_Groups,
            Ifiles,
            Ssl_Certs,
            Ssl_Csrs,
            Ssl_Crls,
            Ssl_Keys]


class Data_Groups(Collection):
    def __init__(self, File):
        super(Data_Groups, self).__init__(File)
        self._meta_data['allowed_lazy_attributes'] = [Data_Group]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:file:data-group:data-groupstate': Data_Group}


class Data_Group(Resource):
    def __init__(self, data_groups):
        super(Data_Group, self).__init__(data_groups)
        self._meta_data['required_json_kind'] =\
            'tm:sys:file:data-group:data-groupstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'sourcePath', 'type'))

    def modify(self, **kwargs):
        '''Modify is not supported for iFiles

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__)

    def update(self, **kwargs):
        if LooseVersion(self._meta_data['bigip']._meta_data['tmos_version']) \
                < LooseVersion('12.0.0'):
            if 'type' in self.__dict__:
                del self.__dict__['type']
        return self._update(**kwargs)


class Ifiles(Collection):
    def __init__(self, File):
        super(Ifiles, self).__init__(File)
        self._meta_data['allowed_lazy_attributes'] = [Ifile]
        self._meta_data['attribute_registry'] = \
            {'tm:sys:file:ifile:ifilestate': Ifile}


class Ifile(Resource):
    def __init__(self, ifiles):
        super(Ifile, self).__init__(ifiles)
        self._meta_data['required_json_kind'] =\
            'tm:sys:file:ifile:ifilestate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'sourcePath'))

    def modify(self, **kwargs):
        '''Modify is not supported for iFiles

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )


class Ssl_Certs(Collection):
    def __init__(self, File):
        super(Ssl_Certs, self).__init__(File)
        self._meta_data['allowed_lazy_attributes'] = [Ssl_Cert]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:file:ssl-cert:ssl-certstate': Ssl_Cert}


class Ssl_Cert(Resource):
    def __init__(self, ssl_certs):
        super(Ssl_Cert, self).__init__(ssl_certs)
        self._meta_data['required_json_kind'] =\
            'tm:sys:file:ssl-cert:ssl-certstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'sourcePath'))

    def modify(self, **kwargs):
        '''Modify is not supported for iFiles

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )


class Ssl_Crls(Collection):
    def __init__(self, File):
        super(Ssl_Crls, self).__init__(File)
        self._meta_data['allowed_lazy_attributes'] = [Ssl_Crl]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:file:ssl-crl:ssl-crlstate': Ssl_Crl}


class Ssl_Crl(Resource):
    def __init__(self, ssl_crls):
        super(Ssl_Crl, self).__init__(ssl_crls)
        self._meta_data['required_json_kind'] =\
            'tm:sys:file:ssl-crl:ssl-crlstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'sourcePath'))

    def modify(self, **kwargs):
        '''Modify is not supported for iFiles

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )


class Ssl_Csrs(Collection):
    def __init__(self, File):
        super(Ssl_Csrs, self).__init__(File)
        self._meta_data['allowed_lazy_attributes'] = [Ssl_Csr]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:file:ssl-csr:ssl-csrstate': Ssl_Csr}
        self._meta_data['minimum_version'] = '12.0.0'


class Ssl_Csr(Resource):
    def __init__(self, ssl_csrs):
        super(Ssl_Csr, self).__init__(ssl_csrs)
        self._meta_data['required_json_kind'] =\
            'tm:sys:file:ssl-csr:ssl-csrstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'sourcePath'))

    def modify(self, **kwargs):
        '''Modify is not supported for iFiles

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )


class Ssl_Keys(Collection):
    def __init__(self, File):
        super(Ssl_Keys, self).__init__(File)
        self._meta_data['allowed_lazy_attributes'] = [Ssl_Key]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:file:ssl-key:ssl-keystate': Ssl_Key}


class Ssl_Key(Resource):
    def __init__(self, ssl_keys):
        super(Ssl_Key, self).__init__(ssl_keys)
        self._meta_data['required_json_kind'] =\
            'tm:sys:file:ssl-key:ssl-keystate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'sourcePath'))

    def modify(self, **kwargs):
        '''Modify is not supported for iFiles

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )

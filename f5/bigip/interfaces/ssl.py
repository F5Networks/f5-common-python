# Copyright 2014 F5 Networks Inc.
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
from f5.common.logger import Log
from f5.common import constants as const
from f5.bigip.interfaces import icontrol_rest_folder, icontrol_folder
from f5.bigip import exceptions
from f5.bigip.interfaces import log

import os
import re
import urllib2
import time
import datetime
import json
from OpenSSL import crypto


class SSL(object):
    """ Interface for SSL related REST methods """

    OBJ_PREFIX = 'uuid_'

    def __init__(self, bigip):
        self.bigip = bigip

        self.bigip.icontrol.add_interfaces(['Management.KeyCertificate',
                                            'LocalLB.ProfileClientSSL'])
        self.mgmt_keycert = self.bigip.icontrol.Management.KeyCertificate
        self.lb_clientssl = self.bigip.icontrol.LocalLB.ProfileClientSSL

    class Certificate():
        """
        provides import and download capability for X.509 certificates
        and their associated keys.
        """

        __key_passphrase__ = None
        __verified__ = False

        key_length = 0
        key_passphrase_required = False
        subject_cn = None
        serial_number = None
        certificate_data = None
        expiration_date = None
        issuer_cn = None
        version = None

        certifcate_id = None

        def __init__(self,
                     name=None,
                     cert=None,
                     key=None,
                     pkcs12=None,
                     passphrase=None):
            if name:
                self.certifcate_id = name
            if cert:
                try:
                    self.get_PEM_certificate(url=cert)
                except ValueError:
                    self.certificate_from_PEM_data(PEM_data=cert)
            if key:
                try:
                    self.get_PEM_key(url=key, key_passphrase=passphrase)
                except ValueError:
                    self.key_from_PEM_data(PEM_data=cert)

        def id_from_subject_cn(self):
            if self.subject_cn:
                self.certificate_id = \
                    str(self.subject_cn).replace("*", 'wildcard') + \
                    "-" + \
                    re.sub('[^A-Za-z0-9]+', '', str(self.serial_number)) + \
                    "-"+str(self.expiration_date.isoformat())

        def certificate_from_PEM_data(self, PEM_data=None):
            if PEM_data:
                x509cert = crypto.load_certificate(  # @UndefinedVariable
                    crypto.FILETYPE_PEM,  # @UndefinedVariable
                    PEM_data
                )
                tm = list(
                    time.strptime(
                        x509cert.get_notAfter()[:8], "%Y%m%d"
                    )
                )[:6]
                tm.append(0)
                tm.append(None)

                self.subject_cn = x509cert.get_subject().__getattribute__('CN')
                self.serial_number = x509cert.get_serial_number()

                self.certificate_data = PEM_data
                self.expiration_date = datetime(*tm).date()
                self.issuer_cn = x509cert.get_issuer().__getattribute__('CN')
                self.version = int(x509cert.get_version())

                if not self.certificate_id:
                    self.id_from_subject_cn()

            else:
                raise ValueError("PEM data for certificate must not be None")

        def key_from_PEM_data(self,
                              PEM_data=None,
                              key_passphrase=""):
            try:

                x509key = crypto.load_privatekey(  # @UndefinedVariable
                    crypto.FILETYPE_PEM,  # @UndefinedVariable
                    PEM_data,
                    key_passphrase
                )
                self.key_data = PEM_data
                self.bit_length = int(x509key.bits())

                if key_passphrase != "":
                    self.__key_passphrase__ = key_passphrase
                    self.key_passphrase_required = True
                    self.key_passphrase = key_passphrase

            except crypto.Error as error:  # @UndefinedVariable
                if "bad decrypt" in error.message[0]:
                    raise ValueError("key passphrase was incorrect")
                else:
                    raise

        def from_PKCS12_data(self, pkcs12_data=None, import_passphrase=None):
            if len(pkcs12_data):
                if not import_passphrase:
                    raise Exception("PKCS12 requires a import password.")

                try:
                    pkcspackage = crypto.load_pkcs12(  # @UndefinedVariable
                        pkcs12_data,
                        import_passphrase
                    )
                except crypto.Error as error:  # @UndefinedVariable
                    if "mac verify failure" in error.message[0]:
                        raise Exception(
                            "import passphrase for PKCS12 was incorrect"
                        )
                    else:
                        raise
                x509cert = pkcspackage.get_certificate()
                tm = list(
                    time.strptime(
                        x509cert.get_notAfter()[:8], "%Y%m%d"
                    )
                )[:6]
                tm.append(0)
                tm.append(None)

                self.subject_cn = \
                    x509cert.get_subject().__getattribute__('CN')
                self.serial_number = int(x509cert.get_serial_number())
                self.certificate_data = \
                    crypto.dump_certificate(  # @UndefinedVariable
                        crypto.FILETYPE_PEM,  # @UndefinedVariable
                        x509cert
                    )
                self.expiration_date = datetime(*tm).date()
                self.issuer_cn = \
                    x509cert.get_issuer().__getattribute__('CN')
                self.version = int(x509cert.get_version())

                private_key = pkcspackage.get_privatekey()
                self.key_data = crypto.dump_privatekey(  # @UndefinedVariable
                    crypto.FILETYPE_PEM,  # @UndefinedVariable
                    private_key
                )
                self.bit_length = int(private_key.bits())
                self.key_passphrase_required = False
                self.key_passphrase = None

                if not self.certificate_id:
                    self.id_from_subject_cn()

            else:
                raise Exception("PKCS12 data must not be None")

        def get_PEM_certificate(self, url=None):
            if url:
                reader = urllib2.urlopen(url)
                certificate = reader.read()
                if len(certificate):
                    self.certificate_from_PEM_data(PEM_data=certificate)
                else:
                    raise ValueError(
                        "PEM certificate URL %s read with no content."
                        % url
                    )
            else:
                raise ValueError(
                    "Must supply a URL to download PEM certificate." +
                    " i.e. file:///path/host.crt"
                )

        def get_PEM_key(self, url=None, key_passphrase=""):
            if url:
                reader = urllib2.urlopen(url)
                try:
                    key = reader.read()
                    if len(key):
                        self.key_from_PEM_data(PEM_data=key,
                                               key_passphrase=key_passphrase)
                except crypto.Error as error:  # @UndefinedVariable
                    if "bad decrypt" in error.message[0]:
                        raise ValueError("key passphrase was incorrect")
                    else:
                        raise
            else:
                raise ValueError("Must supply a URL to download PEM key." +
                                 " i.e. file:///path/host.crt")

        def get_PKCS12(self, url=None, import_passphrase=None):
            if url:

                if not import_passphrase:
                    raise ValueError("PKCS12 requires a import password.")
                reader = urllib2.urlopen(url)
                pkcspackage = reader.read()

                if len(pkcspackage):
                    self.from_PKCS12_data(pkcs12_data=pkcspackage,
                                          import_passphrase=import_passphrase)
                else:
                    raise ValueError(
                        "PKCS12 URL %s read with no content." % url
                    )
            else:
                raise ValueError(
                    "Must supply a URL to download PEM certificate." +
                    " i.e. file:///path/host.crt"
                )

    @log
    @icontrol_folder
    def create_clientssl_profile_for_certificate(
            self,
            certificate=None,
            parent_profile='/Common/clientssl',
            folder='Common'
    ):
        """
        Creates tenant ssl profile for the specified certificate
        folder to create the ssl client profile
        """
        if not isinstance(certificate, Certificate):  # @UndefinedVariable
            raise Exception('certificate is not an instance of Certificate')

        profile_name = certificate.certificate_id
        user_default_parent = True

        if not parent_profile == '/Common/clientssl':
            parent_profile_name = os.path.basename(parent_profile)
            parent_profile_folder = os.path.dirname(parent_profile)
            if not self.client_profile_exists(name=parent_profile_name,
                                              folder=parent_profile_folder):
                raise ValueError('parent clientssl profile %s does not exist'
                                 % parent_profile)
            user_default_parent = False

        if not self.client_profile_exits(name=profile_name, folder=folder):
            # add certificates to group
            self.mgmt_keycert.certificate_import_from_pem(
                mode='MANAGEMENT_MODE_DEFAULT',
                cert_ids=[profile_name],
                pem_data=[certificate.certificate_data],
                overwrite=True
            )
            self.mgmt_keycert.key_import_from_pem(
                mode='MANAGEMENT_MODE_DEFAULT',
                key_ids=[profile_name],
                pem_data=[certificate.key_data],
                overwrite=True
            )
            # add SSL profile
            profile_string_cert = \
                self.lb_clientssl.typefactory.create('LocalLB.ProfileString')
            profile_string_cert.value = profile_name+".crt"
            profile_string_cert.default_flag = False
            profile_string_key = \
                self.lb_clientssl.typefactory.create('LocalLB.ProfileString')
            profile_string_key.value = profile_name+".key"
            profile_string_key.default_flag = False
            self.lb_clientssl.create_v2(
                profile_names=[profile_name],
                keys=[profile_string_key],
                certs=[profile_string_cert]
            )

            if not user_default_parent:
                profile_string_defaults = \
                    self.lb_clientssl.typefactory.create(
                        'LocalLB.ProfileString'
                    )
                profile_string_defaults.value = parent_profile
                profile_string_defaults.default_flag = False
                self.lb_clientssl.set_default_profile(
                    profile_names=[profile_name],
                    defaults=[profile_string_defaults]
                )
            if certificate.__key_passphrase__:
                profile_string_passphrase = \
                    self.lb_clientssl.typefactory.create(
                        'LocalLB.ProfileString'
                    )
                profile_string_passphrase.value = \
                    certificate.__key_passphrase__
                profile_string_passphrase.default_flag = False
                self.lb_clientssl.set_passphrease(
                    profile_names=[profile_name],
                    passphrases=[profile_string_passphrase]
                )

    @log
    @icontrol_folder
    def remove_clientssl_profile_and_certificate(self,
                                                 certificate=None,
                                                 folder='Common'):
        """
        Removes a client ssl profile
        """
        if not isinstance(certificate, Certificate):  # @UndefinedVariable
            raise Exception('certificate is not an instance of Certificate')

        profile_name = certificate.certifcate_id

        if self.client_profile_exits(name=profile_name, folder=folder):
            # remove ssl profile
            self.lb_clientssl.delete_profile([profile_name])
            # remove certificate
            self.mgmt_keycert.certificate_delete(
                mode='MANAGEMENT_MODE_DEFAULT',
                cert_ids=[profile_name]
            )
            # remove key
            self.mgmt_keycert.key_delete(
                mode='MANAGEMENT_MODE_DEFAULT',
                key_ids=[profile_name]
            )

    @log
    @icontrol_rest_folder
    def all_client_profile_names(self, name=None, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/profile/client-ssl/'
        request_url += '?$select=name,partition'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT
        )
        profile_names = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for profile in return_obj['items']:
                    print("%s" % profile)
                    profile_name = '/' + \
                                   profile['partition'] + \
                                   '/' + \
                                   profile['name']
                    profile_names.append(profile_name)
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return profile_names

    @log
    @icontrol_rest_folder
    def client_profile_exits(self, name=None, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/profile/client-ssl/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return False

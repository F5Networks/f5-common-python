
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

from distutils.version import LooseVersion
import pytest


from OpenSSL import crypto
import os
from requests import HTTPError
from tempfile import NamedTemporaryFile


def gen_key():
    # returns key pair in PKey object
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    return key


def gen_csr(key, **name):
    # returns the certificate request in an X509Req object
    req = crypto.X509Req()
    subj = req.get_subject()
    for (k, v) in name.items():
        setattr(subj, k, v)
    req.set_pubkey(key)
    req.sign(key, 'sha1')
    return req


def gen_cert(req, (ca_cert, ca_key), serial):
    # returns the signed certificate in an X509 object
    cert = crypto.X509()
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(86400)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(ca_key, 'sha1')
    return cert


def create_sslfiles():
    # Create a CA Key/Cert
    ca_key = gen_key()
    ca_csr = gen_csr(ca_key, CN='Certificate Authority')
    ca_cert = gen_cert(ca_csr, (ca_csr, ca_key), 0)

    # Create Key/Cert/CSR for uploading to BIG-IP
    key = gen_key()
    csr = gen_csr(key, CN='mycert.test.local')
    cert = gen_cert(csr, (ca_cert, ca_key), 1)

    return key, csr, cert


def setup_ifile_test(request, mgmt_root, name, sourcepath):
    if1 = mgmt_root.tm.sys.file.ifiles.ifile.create(name=name,
                                                    sourcePath=sourcepath)

    def teardown():
        # Remove the ifile.
        try:
            if1.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
    request.addfinalizer(teardown)

    return if1


def test_CURDL_ifile(request, mgmt_root):
    # Create
    ntf = NamedTemporaryFile()
    ntf_basename = os.path.basename(ntf.name)
    ntf.write('this is a test file')
    ntf.seek(0)
    # Upload the file
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)

    tpath_name = 'file:/var/config/rest/downloads/{0}'.format(ntf_basename)
    if1 = setup_ifile_test(request, mgmt_root, ntf_basename, tpath_name)
    assert if1.name == ntf_basename

    # Load Object
    if2 = mgmt_root.tm.sys.file.ifiles.ifile.load(name=ntf_basename)
    assert if1.name == if2.name

    # Rewrite file contents and Update Object
    ntf.write('this is still a test file')
    ntf.seek(0)
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)

    if3 = mgmt_root.tm.sys.file.ifiles.ifile.load(name=ntf_basename)
    if3.update(sourcePath=tpath_name)
    assert if1.revision != if3.revision

    # Refresh if2 and make sure revision matches if3
    if2.refresh()
    assert if2.revision == if3.revision


def setup_sslkey_test(request, mgmt_root, name, sourcepath):
    key = mgmt_root.tm.sys.file.ssl_keys.ssl_key.create(name=name,
                                                        sourcePath=sourcepath)

    def teardown():
        # Remove the key.
        try:
            key.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
    request.addfinalizer(teardown)

    return key


def setup_sslcsr_test(request, mgmt_root, name, sourcepath):
    csr = mgmt_root.tm.sys.file.ssl_csrs.ssl_csr.create(name=name,
                                                        sourcePath=sourcepath)

    def teardown():
        # Remove the key.
        try:
            csr.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise

    request.addfinalizer(teardown)

    return csr


def setup_sslcrt_test(request, mgmt_root, name, sourcepath):
    cert = mgmt_root.tm.sys.file.ssl_certs.ssl_cert.create(
        name=name, sourcePath=sourcepath)

    def teardown():
        # Remove the key.
        try:
            cert.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise

    request.addfinalizer(teardown)

    return cert


def test_CURDL_sslkeyfile(request, mgmt_root):
    # Create temporary Key File.
    # Use extensions so tmui doesn't break in managing them.
    ntf_key = NamedTemporaryFile(suffix='.key')
    ntf_key_basename = os.path.basename(ntf_key.name)
    ntf_key_sourcepath = 'file:/var/config/rest/downloads/{0}'.format(
        ntf_key_basename)

    # Create a CA Key/Cert
    key, csr, cert = create_sslfiles()

    # Write Data to Temporary File
    ntf_key.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    ntf_key.seek(0)

    # Upload File to BIG-IP
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf_key.name)

    # Finally, Let's test something!
    key1 = setup_sslkey_test(request, mgmt_root, ntf_key_basename,
                             ntf_key_sourcepath)
    assert key1.name == ntf_key_basename

    key2 = mgmt_root.tm.sys.file.ssl_keys.ssl_key.load(name=ntf_key_basename)
    assert key1.name == key2.name

    # Create new CA Key/Cert
    key, csr, cert = create_sslfiles()

    # Write new data to Temporary File
    ntf_key.seek(0)
    ntf_key.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    ntf_key.truncate()
    ntf_key.seek(0)

    # Upload File to BIG-IP
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf_key.name)

    # Update Key
    key2.update()
    assert key2.revision != key1.revision

    # Refresh Key
    key1.refresh()
    assert key2.revision == key1.revision


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('12.0.0'),
    reason='csr management is only supported in 12.0.0 or greater.'
)
def test_CURDL_sslcsrfile(request, mgmt_root):
    # Create temporary CSR File.
    # Use extensions so tmui doesn't break in managing them.
    ntf_csr = NamedTemporaryFile(suffix='.csr')
    ntf_csr_basename = os.path.basename(ntf_csr.name)
    ntf_csr_sourcepath = 'file:/var/config/rest/downloads/{0}'.format(
        ntf_csr_basename)

    # Create a CA Key/Cert
    key, csr, cert = create_sslfiles()

    # Write Data to Temporary File
    ntf_csr.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr))
    ntf_csr.seek(0)

    # Upload File to BIG-IP
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf_csr.name)

    # Finally, Let's test something!
    csr1 = setup_sslcsr_test(request, mgmt_root, ntf_csr_basename,
                             ntf_csr_sourcepath)
    assert csr1.name == ntf_csr_basename

    csr2 = mgmt_root.tm.sys.file.ssl_csrs.ssl_csr.load(name=ntf_csr_basename)
    assert csr1.name == csr2.name

    # Create new CA Key/Cert
    key, csr, cert = create_sslfiles()

    # Write new data to Temporary File
    ntf_csr.seek(0)
    ntf_csr.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr))
    ntf_csr.truncate()
    ntf_csr.seek(0)

    # Upload File to BIG-IP
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf_csr.name)

    # Update Key
    csr2.update()
    assert csr2.revision != csr1.revision

    # Refresh Key
    csr1.refresh()
    assert csr2.revision == csr1.revision


def test_CURDL_sslcertfile(request, mgmt_root):
    # Create temporary CSR File.
    # Use extensions so tmui doesn't break in managing them.
    ntf_cert = NamedTemporaryFile(suffix='.crt')
    ntf_cert_basename = os.path.basename(ntf_cert.name)
    ntf_cert_sourcepath = 'file:/var/config/rest/downloads/{0}'.format(
        ntf_cert_basename)

    # Create a CA Key/Cert
    key, csr, cert = create_sslfiles()

    # Write Data to Temporary File
    ntf_cert.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    ntf_cert.seek(0)

    # Upload File to BIG-IP
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf_cert.name)

    # Finally, Let's test something!
    cert1 = setup_sslcrt_test(request, mgmt_root, ntf_cert_basename,
                              ntf_cert_sourcepath)
    assert cert1.name == ntf_cert_basename

    cert2 = mgmt_root.tm.sys.file.ssl_certs.ssl_cert.load(
        name=ntf_cert_basename)
    assert cert1.name == cert2.name

    # Create new CA Key/Cert
    key, csr, cert = create_sslfiles()

    # Write new data to Temporary File
    ntf_cert.seek(0)
    ntf_cert.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    ntf_cert.truncate()
    ntf_cert.seek(0)

    # Upload File to BIG-IP
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf_cert.name)

    # Update Key
    cert2.update()
    assert cert2.revision != cert1.revision

    # Refresh Key
    cert1.refresh()
    assert cert2.revision == cert1.revision

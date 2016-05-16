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

from pprint import pprint as pp
import pytest

from f5.bigip import ManagementRoot

FAKE_CERT = """-----BEGIN CERTIFICATE-----
MIIBozCCAQwCAQEwDQYJKoZIhvcNAQEFBQAwGjEYMBYGA1UEAxQPY2EtaW50QGFj
bWUuY29tMB4XDTE2MDUxMTE2MjcyN1oXDTI2MDUwOTE2MjcyN1owGjEYMBYGA1UE
AxQPc2VydmVyQGFjbWUuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCn
48EdxKMaBvd2nBY4Pt3UI9OhWfDt0JHF/FnE0MOR1DYEP9WqlRlDorojVSignlne
febsSOFxciUGkeYvGTycR58/aAcWfp6lz6gLoTydfi7/XdReQt4JLzH9f0HYdKzz
z06PjNTOGKtcBipUQjAjtH8HRIfOyatIAiUAHHBrBwIDAQABMA0GCSqGSIb3DQEB
BQUAA4GBACvhrSKPtZVMvTUz4I0oxpl85IeM6p2X1qNjlSreCtLLp8o55HF1BEdI
gLdNgzCs1x9/Mi7ZIwA0FySS4s6E8hMA3OG5Z/42aKGCJyHybeoWXsiVYIwkQi/J
7293ACoLewtjwaGAFeSijukgyHooJUkqWi/oG8qc+K2GwZ8yeYYi
-----END CERTIFICATE-----"""

FAKE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCn48EdxKMaBvd2nBY4Pt3UI9OhWfDt0JHF/FnE0MOR1DYEP9Wq
lRlDorojVSignlnefebsSOFxciUGkeYvGTycR58/aAcWfp6lz6gLoTydfi7/XdRe
Qt4JLzH9f0HYdKzzz06PjNTOGKtcBipUQjAjtH8HRIfOyatIAiUAHHBrBwIDAQAB
AoGBAIKTPZBEbkIA5xhlv1ZRdr/WeXNFe3/KtoWQhdTwNRrHPJfDeg+o1LRo7HIs
emOppOXJb/+Xk1djWm6orKk27I6wgIGcLJv61jRq9mOG3Hlfs9ZSkVsQIqutUSVm
amhp3uwK3KIk3k7yv16+VTGfsXsPWsT1oWd4CWmWNAjMol9JAkEA3IloSbt+orEf
x36qv//jsq87gOr5eUmwXTySMHaxbXmkIjaCjZHAb70/kWewXZMoj7k6c1Pj9i3T
Tdfhgl3eLQJBAMLjFS1xIqXKLeBzMjcBfVlDF/ZJa4e2EZd1OOJreGkllx3j23fU
NBdsN71XGr16RuxkLo/4HozequTCh5fU4oMCQAfFG5SFc5e9z9XSg6eSF26jN+B5
5uI8E2eli60DcYre30aJTx43xWTqcQPpeFBDsAkoSIPpr71rrecvNPXH4t0CQGGB
JbZPlUsnZV6Xo/b7StCfDd0ODLugbxq87lHx/RN2WC3/M223gLx7S0Py0ZEdHWDm
GpmzRO2r9gpv/VEMlKsCQQCV+EffCQ4wKBIYeCchdntop1/A9PWWCS+pjUNdIJNR
CKxlxUfEZw9yNfLw9g0FKxrdSZiHCAw7fwN7s+CszjT4
-----END RSA PRIVATE KEY-----"""


@pytest.fixture
def cleaner(request, symbols):
    mr = ManagementRoot(symbols.bigip_netloc,
                        symbols.bigip_username,
                        symbols.bigip_password,
                        port=symbols.bigip_port)
    initsslclientprofiles = mr.tm.ltm.profile.client_ssls.get_collection()
    initfullpaths = [iscp.fullPath for iscp in initsslclientprofiles]

    def cleaner():
        sslclientprofiles = mr.tm.ltm.profile.client_ssls.get_collection()
        for sscp in sslclientprofiles:
            pp(sscp.raw)
            if sscp.fullPath not in initfullpaths:
                sscp.delete()
    request.addfinalizer(cleaner)


def test_ssl_profile_creation(cleaner, symbols, tmpdir):
    testdatadir = tmpdir.mkdir('testdir')
    FAKEKEYFILENAME = 'fakekey.key'
    CERTFILENAME = 'NEWTESTCLIENTPROFILENAME.crt'
    certpath = testdatadir.join(CERTFILENAME)
    certpath.write(FAKE_CERT)
    keypath = testdatadir.join(FAKEKEYFILENAME)
    keypath.write(FAKE_KEY)
    mr = ManagementRoot(symbols.bigip_netloc,
                        symbols.bigip_username,
                        symbols.bigip_password,
                        port=symbols.bigip_port)
    uploader = mr.shared.file_transfer.uploads
    cert_registrar = mr.tm.sys.crypto.certs
    pp(cert_registrar.raw)
    key_registrar = mr.tm.sys.crypto.keys
    ssl_client_profile = mr.tm.ltm.profile.client_ssls.client_ssl
    uploader.upload_file(str(certpath))
    uploader.upload_file(str(keypath))
    cert_registrar.install_cert(CERTFILENAME)
    pp([cert.raw for cert in cert_registrar.get_collection()])
    key_registrar.install_key(CERTFILENAME, FAKEKEYFILENAME)
    pp([key.raw for key in key_registrar.get_collection()])
    ssl_client_profile.create(certname='/Common/NEWTESTCLIENTPROFILENAME.crt',
                              keyname='/Common/NEWTESTCLIENTPROFILENAME.key')
    pp(ssl_client_profile.raw)

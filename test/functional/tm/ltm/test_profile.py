# Copyright 2015-2106 F5 Networks Inc.
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
pp(__file__)
import pytest

TESTDESCRIPTION = "TESTDESCRIPTION"

end_lst = ['Certificate_Authoritys', 'Classifications', 'Client_Ldaps',
           'Client_Ssls', 'Dhcpv4s', 'Dhcpv6s', 'Diameters', 'Dns_s',
           'Dns_Loggings', 'Fasthttps', 'Fastl4s', 'Fixs', 'Ftps',
           'Gtps', 'Htmls', 'Https', 'Http_Compressions',  'Http2s',
           'Icaps', 'Iiops', 'Ipothers', 'Mblbs', 'Mssqls', 'Ntlms',
           'Ocsp_Stapling_Params_s', 'One_Connects', 'Pcps', 'Pptps',
           'Qoes', 'Radius_s', 'Request_Adapts', 'Request_Logs',
           'Response_Adapts', 'Rtsps', 'Sctps', 'Server_Ldaps',
           'Server_Ssls', 'Sips', 'Smtps', 'Smtps_s', 'Socks_s',
           'Spdys', 'Statistics_s', 'Streams', 'Tcps', 'Tftps', 'Udps',
           'Web_Accelerations', 'Web_Securitys', 'Xmls', 'Analytics_s',
           'Rewrites']

common = 'bigip.ltm.profile.'


# Helper class to limit code repetition
class HelperTest(object):
    def __init__(self, item, idx):
        self.item = item
        self.idx = idx
        self.name = 'test' + self.fullstring()
        self.partition = 'Common'

    def fullstring(self):
        if self.item[self.idx].lower()[-2:] == '_s':
            endind = 2
        else:
            endind = 1
        full_str = '.' + self.item[self.idx][:-endind]
        return full_str.lower()

    def setup_test(self, request, bigip, **kwargs):
        hc = common+self.item[self.idx].lower()
        factory = eval(hc + self.fullstring())

        def teardown():
            if factory.exists(name=self.name, partition=self.partition):
                factory.load(name=self.name, partition=self.partition).delete()
        teardown()
        request.addfinalizer(teardown)
        profile =\
            factory.create(name=self.name, partition=self.partition, **kwargs)
        return profile, hc

    def test_CURDL(self, request, bigip, **kwargs):

        # Testing create
        profile1, hc = self.setup_test(request, bigip, **kwargs)
        assert profile1.name == self.name

        # Testing update
        profile1.description = TESTDESCRIPTION
        profile1.update()
        if hasattr(profile1, 'description'):
            assert profile1.description == TESTDESCRIPTION

        # Testing refresh
        profile1.description = ''
        profile1.refresh()
        if hasattr(profile1, 'description'):
            assert profile1.description == TESTDESCRIPTION

        # Testing load
        p2 = eval(hc+self.fullstring())
        profile2 = p2.load(partition=self.partition, name=self.name)
        assert profile1.selfLink == profile2.selfLink

    def test_CURDL_Adapt(self, request, bigip):

        # Testing create
        profile1, hc = self.setup_test(request, bigip)
        assert profile1.name == self.name

        # Testing update
        profile1.timeout = 10
        profile1.update()
        assert profile1.timeout == 10

        # Testing refresh
        profile1.timeout = 0
        profile1.refresh()
        assert profile1.timeout == 10

        # Testing load
        p2 = eval(hc+self.fullstring())
        profile2 = p2.load(partition=self.partition, name=self.name)
        assert profile1.selfLink == profile2.selfLink

# Begin Analytics tests
# Sub-collection setup function


def setup_test_subc(request, bigip):
    def teardown():
        if prf_alert.exists(name='test_alert'):
            prf_alert.delete()
        if prf_traffic.exists(name='test_traf_cap'):
            prf_traffic.delete()

    avr = HelperTest(end_lst, 50)
    avrstr, avrhc1 = avr.setup_test(request, bigip)
    del avrstr
    prf_alert = avrhc1.alerts_s.alerts
    prf_alert.create(name='test_alert', threshold=200)
    prf_traffic = avrhc1.traffic_captures.traffic_capture.create(
        name='test_traf_cap')
    request.addfinalizer(teardown)
    return prf_alert, prf_traffic, avrhc1


@pytest.mark.skipif(True, reason='this depends on an optional module')
class TestAnalytics(object):
    def test_CURDL(self, request, bigip):
        avr = HelperTest(end_lst, 50)
        avr.test_CURDL(request, bigip)


@pytest.mark.skipif(True, reason='this depends on an optional module')
class TestAnalyticsSubCol(object):
    def test_CURDL(self, request, bigip):

        # Testing create and delete
        alert1, traffic1, avrhc1 = setup_test_subc(request, bigip)
        assert alert1.name == 'test_alert'
        assert traffic1.name == 'test_traf_cap'

        # Testing update
        alert1.threshold = 250
        alert1.update()
        assert alert1.threshold == 250
        traffic1.requestCapturedParts = 'headers'
        traffic1.update()
        assert traffic1.requestCapturedParts == 'headers'

        # Testing refresh
        alert1.threshold = 200
        alert1.refresh()
        assert alert1.threshold == 250
        traffic1.requestCapturedParts = 'none'
        traffic1.refresh()
        assert traffic1.requestCapturedParts == 'headers'

        # Testing load
        alert2 = avrhc1.alerts_s.alerts.load(name='test_alert')
        assert alert1.name == alert2.name
        traffic2 = avrhc1.traffic_captures.traffic_capture.load(
            name='test_traf_cap')
        assert traffic1.name == traffic2.name


# End Analytics tests

# Begin Certificate Authority tests


class TestCertifcateAutority(object):
    def test_CURDL(self, request, bigip):
        ca = HelperTest(end_lst, 0)
        ca.test_CURDL(request, bigip)


# End Certificate Authority tests

# Begin Classification tests


class TestClassification(object):
    def test_RUL(self, request, bigip):

        # Load test
        klass1 = bigip.ltm.profile.classifications.classification.\
            load(name='classification')

        # Update test
        klass1.description = TESTDESCRIPTION
        klass1.update()
        assert klass1.description == TESTDESCRIPTION

        # Refresh test
        klass1.description = 'ICHANGEDIT'
        klass1.refresh()
        assert klass1.description == TESTDESCRIPTION


# End Classification tests

# Begin ClientLdap tests


class TestClientLdap(object):
    def test_CURDL(self, request, bigip):
        ldap = HelperTest(end_lst, 2)
        ldap.test_CURDL(request, bigip)


# End ClientLdap tests

# Begin ClientSSL tests


class TestClientSsl(object):
    def test_CURDL(self, request, bigip):
        cssl = HelperTest(end_lst, 3)
        cssl.test_CURDL(request, bigip)


# End ClientSSL tests

# Begin Dhcpv4 tests


class TestDhcpv4(object):
    def test_CURDL(self, request, bigip):
        dhcpv4 = HelperTest(end_lst, 4)
        dhcpv4.test_CURDL(request, bigip)


# End Dhcpv4 tests

# Begin Dhcpv6 tests


class TestDhcpv6(object):
    def test_CURDL(self, request, bigip):
        dhcpv6 = HelperTest(end_lst, 5)
        dhcpv6.test_CURDL(request, bigip)


# End Dhcpv6 tests

# Begin Diameter tests


class TestDiameter(object):
    def test_CURDL(self, request, bigip):
        diameter = HelperTest(end_lst, 6)
        diameter.test_CURDL(request, bigip)


# End Diameter tests

# Begin Dns tests


class TestDns(object):
    def test_CURDL(self, request, bigip):
        dns = HelperTest(end_lst, 7)
        dns.test_CURDL(request, bigip)


# End Dns tests

# Begin Dns Logging tests


class TestDnsLogging(object):
    def test_CURDL(self, request, bigip):
        dnslog = HelperTest(end_lst, 8)

        # Testing create

        dns1, dnshc = dnslog.setup_test(
            request, bigip,
            logPublisher='/Common/local-db-publisher')
        assert dns1.name == 'test.dns_logging'
        del dnshc

        # Testing update
        assert dns1.enableQueryLogging == 'yes'
        dns1.enableQueryLogging = 'no'
        dns1.update()
        assert dns1.enableQueryLogging == 'no'

        # Testing refresh
        dns1.enableQueryLogging = 'yes'
        dns1.refresh()
        assert dns1.enableQueryLogging == 'no'

        # Testing load
        dns2 = bigip.ltm.profile.dns_loggings.dns_logging.load(
            partition='Common', name='test.dns_logging')
        assert dns1.selfLink == dns2.selfLink

# End Dns Logging test

# Begin FastHttp tests


class TestFastHttp(object):
    def test_CURDL(self, request, bigip):
        fasthttp = HelperTest(end_lst, 9)
        fasthttp.test_CURDL(request, bigip)


# End FastHttp tests

# Begin FastL4 tests


class TestFastL4(object):
    def test_CURDL(self, request, bigip):
        fastl4 = HelperTest(end_lst, 10)
        fastl4.test_CURDL(request, bigip)


# End FastL4 tests

# Begin Fix tests


class TestFix(object):
    def test_CURDL(self, request, bigip):
        fix = HelperTest(end_lst, 11)

        # Testing create

        fix1, fixc = fix.setup_test(request, bigip)
        assert fix1.name == 'test.fix'
        del fixc

        # Testing update
        assert fix1.quickParsing == 'false'
        fix1.quickParsing = 'true'
        fix1.update()
        assert fix1.quickParsing == 'true'

        # Testing refresh
        fix1.quickParsing = 'false'
        fix1.refresh()
        assert fix1.quickParsing == 'true'

        # Testing load
        fix2 = bigip.ltm.profile.fixs.fix.load(
            partition='Common', name='test.fix')
        assert fix1.selfLink == fix2.selfLink


# End Fix tests

# Begin FTP tests


class TestFtp(object):
    def test_CURDL(self, request, bigip):
        ftp = HelperTest(end_lst, 12)
        ftp.test_CURDL(request, bigip)


# End FTP tests

# Begin GTP tests


class TestGtp(object):
    def test_CURDL(self, request, bigip):
        gtp = HelperTest(end_lst, 13)
        gtp.test_CURDL(request, bigip)


# End GTP tests

# Begin HTML tests


class TestHtml(object):
    def test_CURDL(self, request, bigip):
        html = HelperTest(end_lst, 14)
        html.test_CURDL(request, bigip)


# End HTML tests

# Begin HTTP tests


class TestHttp(object):
    def test_CURDL(self, request, bigip):
        http = HelperTest(end_lst, 15)
        http.test_CURDL(request, bigip)


# End HTTP tests

# Begin HTTP Compression tests


class TestHttpCompress(object):
    def test_CURDL(self, request, bigip):
        httpc = HelperTest(end_lst, 16)
        httpc.test_CURDL(request, bigip)


# End HTTP Compression tests

# Begin HTTP tests


class TestHttp2(object):
    def test_CURDL(self, request, bigip):
        http2 = HelperTest(end_lst, 17)
        http2.test_CURDL(request, bigip)


# End HTTP tests

# Begin ICAP tests


class TestIcap(object):
    def test_CURDL(self, request, bigip):
        icap = HelperTest(end_lst, 18)

        # Test Create
        icap1, icapc = icap.setup_test(request, bigip)
        assert icap1.name == 'test.icap'

        # Test Update
        icap1.previewLength = 100
        icap1.update()
        assert icap1.previewLength == 100

        # Test Refresh
        icap1.previewLength = 50
        icap1.refresh()
        assert icap1.previewLength == 100

        # Test Load
        icap2 = bigip.ltm.profile.icaps.icap.load(
            name='test.icap', partition='Common')
        assert icap1.selfLink == icap2.selfLink


# End ICAP tests

# Begin IIOP tests

@pytest.mark.skipif(pytest.config.getoption('--release') != '12.0.0',
                    reason='Needs v12 TMOS to pass')
class TestIiop(object):
    def test_CURDL(self, request, bigip):
        iiop = HelperTest(end_lst, 19)
        iiop.test_CURDL(request, bigip)


# End IIOP tests

# Begin Ipother tests


class TestIother(object):
    def ttest_CURDL(self, request, bigip):
        ipoth = HelperTest(end_lst, 20)
        ipoth.test_CURDL(request, bigip)


# End Ipother tests

# Begin Mblb tests


class TestMblb(object):
    def test_CURDL(self, request, bigip):
        mblb = HelperTest(end_lst, 21)
        mblb.test_CURDL(request, bigip)


# End Mblb tests

# Begin Mssql tests

class TestMssql(object):
    def test_CURDL(self, request, bigip):
        mssql = HelperTest(end_lst, 22)

        # Testing create

        mssql1, mssqlc = mssql.setup_test(request, bigip)
        assert mssql1.name == 'test.mssql'
        del mssqlc

        # Testing update
        assert mssql1.userCanWriteByDefault == 'true'
        mssql1.userCanWriteByDefault = 'false'
        mssql1.update()
        assert mssql1.userCanWriteByDefault == 'false'

        # Testing refresh
        mssql1.userCanWriteByDefault = 'true'
        mssql1.refresh()
        assert mssql1.userCanWriteByDefault == 'false'

        # Testing load
        mssql2 = bigip.ltm.profile.mssqls.mssql.load(
            partition='Common', name='test.mssql')
        assert mssql1.selfLink == mssql2.selfLink


# End Mssql tests

# Begin Ntlm tests


class TestNtlm(object):
    def test_CURDL(self, request, bigip):
        ntlm = HelperTest(end_lst, 23)
        ntlm.test_CURDL(request, bigip)


# End Ntlm tests

# Begin Ocsp Stapling Params tests

def setup_dns_resolver(request, bigip, name):
    def teardown():
        if dns_res.exists(name=name):
            dns_res.delete()
    request.addfinalizer(teardown)
    dns_res = bigip.net.dns_resolvers.dns_resolver.create(name=name)
    return dns_res


class TestOcspStaplingParams(object):
    def test_CURDL(self, request, bigip):

        # Setup DNS resolver as prerequisite
        dns = setup_dns_resolver(request, bigip, 'test_resolv')

        # Test CURDL
        ocsp = HelperTest(end_lst, 24)

        # Testing create
        ocsp1, ocsphc = ocsp.setup_test(
            request, bigip, dnsResolver=dns.name,
            trustedCa='/Common/ca-bundle.crt',
            useProxyServer='disabled')

        pp(ocsp1.raw)
        assert ocsp1.name == 'test.ocsp_stapling_params'
        del ocsphc

        # Testing update
        ocsp1.cacheErrorTimeout = 3000
        ocsp1.update()
        assert ocsp1.cacheErrorTimeout == 3000

        # Testing refresh
        ocsp1.cacheErrorTimeout = 30
        ocsp1.refresh()
        assert ocsp1.cacheErrorTimeout == 3000

        # Testing load
        ocsp_params = bigip.ltm.profile.ocsp_stapling_params_s
        ocsp2 = ocsp_params.ocsp_stapling_params.load(
            partition='Common', name='test.ocsp_stapling_params')

        assert ocsp1.selfLink == ocsp2.selfLink


# End Ocsp Stapling Params tests

# Begin Oneconnect tests


class TestOneConnect(object):
    def test_CURDL(self, request, bigip):
        onec = HelperTest(end_lst, 25)
        onec.test_CURDL(request, bigip)


# End Oneconnect tests

# Begin Pcp tests


@pytest.mark.skipif(True, reason='this depends on an optional module')
class TestPcp(object):
    def test_CURDL(self, request, bigip):
        pcp = HelperTest(end_lst, 26)
        pcp.test_CURDL(request, bigip)


# End Pcp tests

# Begin Pptp tests


class TestPptp(object):
    def test_CURDL(self, request, bigip):
        pptp = HelperTest(end_lst, 27)
        pptp.test_CURDL(request, bigip)


# End Pptp tests

# Begin Qoe tests


class TestQoe(object):
    def test_CURDL(self, request, bigip):
        qoe = HelperTest(end_lst, 28)

        # Testing create

        qoe1, qoec = qoe.setup_test(request, bigip)
        assert qoe1.name == 'test.qoe'
        del qoec

        # Testing update
        assert qoe1.video == 'false'
        qoe1.video = 'true'
        qoe1.update()
        assert qoe1.video == 'true'

        # Testing refresh
        qoe1.video = 'false'
        qoe1.refresh()
        assert qoe1.video == 'true'

        # Testing load
        qoe2 = bigip.ltm.profile.qoes.qoe.load(
            partition='Common', name='test.qoe')
        assert qoe1.selfLink == qoe2.selfLink


# End Qoe tests

# Begin Radius tests


class TestRadius(object):
    def test_CURDL(self, request, bigip):
        radius = HelperTest(end_lst, 29)
        radius.test_CURDL(request, bigip)


# End Radius tests

# Begin Request Adapt tests


class TestRequestAdapt(object):
    def test_CURDL(self, request, bigip):
        rq_adp = HelperTest(end_lst, 30)
        rq_adp.test_CURDL_Adapt(request, bigip)


# End Request Adapt tests

# Begin Request Log tests


class TestRequestLog(object):
    def test_CURDL(self, request, bigip):
        rq_log = HelperTest(end_lst, 31)
        rq_log.test_CURDL(request, bigip)


# End Request Log tests

# Begin Response Adapt tests


class TestResponseAdapt(object):
    def test_CURDL(self, request, bigip):
        res_adp = HelperTest(end_lst, 32)
        res_adp.test_CURDL_Adapt(request, bigip)


# End Response Adapt tests

# Begin Rewrite tests
# Sub-collection setup function


def setup_test_uri(request, bigip):
    def teardown():
        if uri1.exists(name='test.uri'):
            uri1.delete()

    rewrite = HelperTest(end_lst, 51)
    url_rw, rewrite_str = rewrite.setup_test(
        request, bigip, rewriteMode='uri-translation')
    del rewrite_str
    client = {'host': 'example.com', 'path': '/', 'scheme': 'http'}
    server = {'host': 'instance.com', 'path': '/', 'scheme': 'http'}
    uri1 = url_rw.uri_rules_s.uri_rules.create(name='test.uri',
                                               type='request',
                                               client=client,
                                               server=server)
    request.addfinalizer(teardown)
    return uri1, url_rw


class TestRewrite(object):
    def test_CURDL_rewrite(self, request, bigip):

        # Test Create
        rewrite = HelperTest(end_lst, 51)
        rewrite1, rewrite_str = \
            rewrite.setup_test(request, bigip)
        del rewrite_str
        assert rewrite1.name == 'test.rewrite'

        # Test update
        rewrite1.clientCachingType = 'no-cache'
        rewrite1.update()
        assert rewrite1.clientCachingType == 'no-cache'

        # Test refresh
        rewrite1.splitTunneling = 'true'
        rewrite1.refresh()
        assert rewrite1.splitTunneling == 'false'

        # Test load
        rewrite2 = bigip.ltm.profile.rewrites.rewrite.load(name='test.rewrite',
                                                           partition='Common')
        assert rewrite1.selfLink == rewrite2.selfLink


class TestUriRulesSubCol(object):
    def test_CURDL(self, request, bigip):

        # Test Create
        uri1, uri_rw = setup_test_uri(request, bigip)
        assert uri1.name == 'test.uri'

        # Test Update
        client = {'host': 'sample.com',
                  'path': '/', 'scheme': 'https'}
        uri1.client = client
        uri1.update()
        assert uri1.client == {'host': 'sample.com',
                               'path': '/', 'scheme': 'https'}

        # Test Refresh
        client = {'host': 'changed.com',
                  'path': '/', 'scheme': 'http'}
        uri1.client = client
        uri1.refresh()
        assert uri1.client == {'host': 'sample.com',
                               'path': '/', 'scheme': 'https'}

        # Test Load
        uri2 = uri_rw.uri_rules_s.uri_rules.load(name='test.uri')
        assert uri1.selfLink == uri2.selfLink


# End Rewrite tests

# Begin Rstps tests


class TestRstps(object):
    def test_CURDL(self, request, bigip):
        rstps = HelperTest(end_lst, 33)
        rstps.test_CURDL(request, bigip)


# End Rstps tests

# Begin Sctps tests


class TestSctps(object):
    def test_CURDL(self, request, bigip):
        sctps = HelperTest(end_lst, 34)
        sctps.test_CURDL(request, bigip)


# End Sctps tests

# Begin Server Ldap tests


class TestServerLdap(object):
    def test_CURDL(self, request, bigip):
        sldap = HelperTest(end_lst, 35)
        sldap.test_CURDL(request, bigip)


# End Server Ldap tests

# Begin Server Ssl tests


class TestServerSsl(object):
    def test_CURDL(self, request, bigip):
        sssl = HelperTest(end_lst, 36)
        sssl.test_CURDL(request, bigip)


# End Server Ldap tests

# Begin Sip tests


class TestSip(object):
    def test_CURDL(self, request, bigip):
        sip = HelperTest(end_lst, 37)
        sip.test_CURDL(request, bigip)


# End Sip tests

# Begin Smtp tests


class TestSmtp(object):
    def test_CURDL(self, request, bigip):
        smtp = HelperTest(end_lst, 38)
        smtp.test_CURDL(request, bigip)


# End Smtp tests

# Begin Smtps tests


class TestSmtps(object):
    def test_CURDL(self, request, bigip):
        smtps = HelperTest(end_lst, 39)
        smtps.test_CURDL(request, bigip)


# End Smtps tests

# Begin Sock tests


class TestSock(object):
    def test_CURDL(self, request, bigip):

        dns = setup_dns_resolver(request, bigip,
                                 'test_resolv')
        socks = HelperTest(end_lst, 40)
        socks.test_CURDL(request, bigip,
                         dnsResolver=dns.name)


# End Sock tests

# Begin Spdy tests


class TestSpdy(object):
    def test_CURDL(self, request, bigip):
        spdy = HelperTest(end_lst, 41)
        spdy.test_CURDL(request, bigip)


# End Spdy tests

# Begin Statistics tests


class TestStatistics(object):
    def test_CURDL(self, request, bigip):
        stat = HelperTest(end_lst, 42)
        stat.test_CURDL(request, bigip)


# End Statistics tests

# Begin Stream tests


class TestStream(object):
    def test_CURDL(self, request, bigip):
        stream = HelperTest(end_lst, 43)
        stream.test_CURDL(request, bigip)


# End Stream tests

# Begin Tcp tests


class TestTcp(object):
    def test_CURDL(self, request, bigip):
        testcp = HelperTest(end_lst, 44)
        testcp.test_CURDL(request, bigip)


# End Tcp tests

# Begin Tftp tests

@pytest.mark.skipif(pytest.config.getoption('--release') != '12.0.0',
                    reason='Needs v12 TMOS to pass')
class TestTftp(object):
    def test_CURDL(self, request, bigip):
        tftp = HelperTest(end_lst, 45)
        tftp.test_CURDL(request, bigip)


# End Tftp tests

# Begin Udp tests


class TestUdp(object):
    def test_CURDL(self, request, bigip):
        tesudp = HelperTest(end_lst, 46)
        tesudp.test_CURDL(request, bigip)


# End Udp tests


# Begin WebAcceleration tests


class TestWebAcceleration(object):
    def test_CURDL(self, request, bigip):
        wa = HelperTest(end_lst, 47)

        # Test Create
        wa1, wapc = wa.setup_test(request, bigip)
        assert wa1.name == 'test.web_acceleration'

        # Test Update
        wa1.cacheAgingRate = 5
        wa1.update()
        assert wa1.cacheAgingRate == 5

        # Test Refresh
        wa1.cacheAgingRate = 10
        wa1.refresh()
        assert wa1.cacheAgingRate == 5

        # Test Load
        wa2 = bigip.ltm.profile.web_accelerations.web_acceleration.load(
            name='test.web_acceleration', partition='Common')
        assert wa1.cacheAgingRate == wa2.cacheAgingRate


# End Web Acceleration tests

# Begin Web Security tests


class iTestWebSecurity(object):
    def test_load(self, request, bigip):
        ws1 = bigip.ltm.profile.\
            web_securitys.websecurity.load(name='websecurity')
        assert ws1.name == 'websecurity'


# End Web Security tests

# Begin Xml tests


class TestXml(object):
    def test_CURDL(self, request, bigip):
        testxml = HelperTest(end_lst, 49)
        testxml.test_CURDL(request, bigip)


# End Xml tests

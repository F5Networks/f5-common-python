
TESTDESCRIPTION = "TESTDESCRIPTION"

end_lst = ['Certificate_Authoritys', 'Classifications', 'Client_Ldaps', 'Client_Ssls',
       'Dhcpv4s','Dhcpv6s', 'Diameters', 'Dns_s', 'Dns_Loggings', 'Fasthttps',
       'Fastl4s', 'Fixs', 'Ftps','Gtps', 'Htmls', 'Https', 'Http_Compressions',
       'Http2s', 'Icaps', 'Iiops', 'Ipothers', 'Mblbs', 'Mssqls', 'Ntlms',
       'Ocsp_Stapling_Params_s', 'One_Connects', 'Pcps', 'Pptps', 'Qoes', 'Radius_s',
       'Request_Adapts', 'Request_Logs', 'Response_Adapts', 'Rtsps', 'Sctps','Server_Ldaps',
       'Server_Ssls', 'Sips', 'Smtps', 'Smtps_s', 'Socks_s','Spdys', 'Statistics_s', 'Streams',
       'Tcps', 'Tftps', 'Udps', 'Web_Accelerations', 'Web_Securitys', 'Xmls']
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
        full_str = '.' +self.item[self.idx][:-endind]
        return full_str.lower()

    def setup_test(self, request, bigip, **kwargs):
        def teardown():
            if profile.exists(name=self.name, partition=self.partition):
                profile.delete()
        request.addfinalizer(teardown)
        hc = common+self.item[self.idx].lower()
        profile = eval(hc + self.fullstring())
        profile.create(name=self.name, partition=self.partition, **kwargs)
        return hc, profile

    def test_CURDL(self, request, bigip, **kwargs):

        # Testing create
        hc, profile1 = self.setup_test(request, bigip, **kwargs)
        assert profile1.name == self.name

        # Testing update
        profile1.description = TESTDESCRIPTION
        profile1.update()
        assert profile1.description == TESTDESCRIPTION

        # Testing refresh
        profile1.description = ''
        profile1.refresh()
        assert profile1.description == TESTDESCRIPTION

        # Testing load
        profile2 = eval(hc+self.fullstring())
        profile2.load(partition=self.partition, name=self.name)
        assert profile1.selfLink == profile2.selfLink

# Begin Analytics tests
##placeholder
# End Analytics tests

# Begin Certificate Authority tests
class TestCertifcateAutority(object):
    def test_ca(self, request, bigip):
        ca = HelperTest(end_lst, 0)
        ca.test_CURDL(request, bigip)
# End Certificate Authority tests

# Begin Classification tests
##placeholder
# End Classification tests

# Begin ClientLdap tests
class TestClientLdap(object):
    def test_clientldap(self, request, bigip):
        ldap = HelperTest(end_lst, 2)
        ldap.test_CURDL(request, bigip)
# End ClientLdap tests

# Begin ClientSSL tests
class TestClientSsl(object):
    def test_clientssl(self, request, bigip):
        cssl = HelperTest(end_lst, 3)
        cssl.test_CURDL(request, bigip)
# End ClientSSL tests

# Begin Dhcpv4 tests
class TestDhcpv4(object):
    def test_dhcpv4(self, request, bigip):
        dhcpv4 = HelperTest(end_lst, 4)
        dhcpv4.test_CURDL(request, bigip)
# End Dhcpv4 tests

# Begin Dhcpv6 tests
class TestDhcpv6(object):
    def test_dhcpv6(self, request, bigip):
        dhcpv6 = HelperTest(end_lst, 5)
        dhcpv6.test_CURDL(request, bigip)
# End Dhcpv6 tests

# Begin Diameter tests
class TestDiameter(object):
    def test_diameter(self, request, bigip):
        diameter = HelperTest(end_lst, 6)
        diameter.test_CURDL(request, bigip)
# End Diameter tests

# Begin Dns tests
class TestDns(object):
    def test_dns(self, request, bigip):
        dns = HelperTest(end_lst, 7)
        dns.test_CURDL(request, bigip)
# End Dns tests

# Begin Dns Logging tests
class TestDnsLogging(object):
    def test_dns_logging(self, request, bigip):
        dnslog = HelperTest(end_lst, 8)
        dnslog.test_CURDL(request, bigip,
                          logPublisher='/Common/local-db-publisher')
# End Dns Logging test

# Begin FastHttp tests
class TestFastHttp(object):
    def test_fasthttp(self, request, bigip):
        fasthttp = HelperTest(end_lst, 9)
        fasthttp.test_CURDL(request, bigip)
# End FastHttp tests

# Begin FastL4 tests
class TestFastL4(object):
    def test_fastl4(self, request, bigip):
        fastl4 = HelperTest(end_lst, 10)
        fastl4.test_CURDL(request, bigip)
# End FastL4 tests

# Begin Fix tests
class TestFix(object):
    def test_fix(self, request, bigip):
        fix = HelperTest(end_lst, 11)
        fix.test_CURDL(request, bigip)
# End Fix tests

# Begin FTP tests
class TestFtp(object):
    def test_ftp(self, request, bigip):
        ftp = HelperTest(end_lst, 12)
        ftp.test_CURDL(request, bigip)
# End FTP tests

# Begin GTP tests
class TestGtp(object):
    def test_gtp(self, request, bigip):
        gtp = HelperTest(end_lst, 13)
        gtp.test_CURDL(request, bigip)
# End GTP tests

# Begin HTML tests
class TestHtml(object):
    def test_html(self, request, bigip):
        html = HelperTest(end_lst, 14)
        html.test_CURDL(request, bigip)
# End HTML tests

# Begin HTTP tests
class TestHttp(object):
    def test_http(self, request, bigip):
        http = HelperTest(end_lst, 15)
        http.test_CURDL(request, bigip)
# End HTTP tests

# Begin HTTP Compression tests
class TestHttpCompress(object):
    def test_httpcompress(self, request, bigip):
        httpc = HelperTest(end_lst, 16)
        httpc.test_CURDL(request, bigip)
# End HTTP Compression tests

# Begin HTTP tests
class TestHttp2(object):
    def test_http2(self, request, bigip):
        http2 = HelperTest(end_lst, 17)
        http2.test_CURDL(request, bigip)
# End HTTP tests

# Begin ICAP tests - Failing ## no attribute description
class TestIcap(object):
    def test_icap(self, request, bigip):
        icap = HelperTest(end_lst, 18)
        icap.test_CURDL(request, bigip)
# End ICAP tests

# Begin IIOP tests
class TestIiop(object):
    def test_iiop(self, request, bigip):
        iiop = HelperTest(end_lst, 19)
        iiop.test_CURDL(request, bigip)
# End IIOP tests

# Begin Ipother tests
class TestIother(object):
    def test_ipother(self, request, bigip):
        ipoth = HelperTest(end_lst, 20)
        ipoth.test_CURDL(request, bigip)
# End Ipother tests

# Begin Mblb tests
class TestMblb(object):
    def test_mblb(self, request, bigip):
        mblb = HelperTest(end_lst, 21)
        mblb.test_CURDL(request, bigip)
# End Mblb tests

# Begin Mssql tests
class TestMssql(object):
    def test_mssql(self, request, bigip):
        mssql = HelperTest(end_lst, 22)
        mssql.test_CURDL(request, bigip)
# End Mssql tests

# Begin Ntlm tests
class TestNtlm(object):
    def test_Ntlm(self, request, bigip):
        ntlm = HelperTest(end_lst, 23)
        ntlm.test_CURDL(request, bigip)
# End Ntlm tests

# Begin Ocsp Stapling Params tests ## Needs to determine dns resolver or proxy,
# so 2 mutually exclusive and required attr
class TestOcspStaplingParams(object):
    def test_ocspstapleparam(self, request, bigip):
        ocspst = HelperTest(end_lst, 24)
        ocspst.test_CURDL(request, bigip)
# End Ocsp Stapling Params tests

# Begin Oneconnect tests
class TestOneConnect(object):
    def test_oneconnect(self, request, bigip):
        onec = HelperTest(end_lst, 25)
        onec.test_CURDL(request, bigip)
# End Oneconnect tests

# Begin Pcp tests
class TestPcp(object):
    def test_pcp(self, request, bigip):
        pcp = HelperTest(end_lst, 26)
        pcp.test_CURDL(request, bigip)
# End Pcp tests

# Begin Pptp tests
class TestPptp(object):
    def test_pptp(self, request, bigip):
        pptp = HelperTest(end_lst, 27)
        pptp.test_CURDL(request, bigip)
# End Pptp tests

# Begin Qoe tests
class TestQoe(object):
    def test_qoe(self, request, bigip):
        qoe = HelperTest(end_lst, 28)
        qoe.test_CURDL(request, bigip)
# End Qoe tests

# Begin Radius tests
class TestRadius(object):
    def test_radius(self, request, bigip):
        radius = HelperTest(end_lst, 29)
        radius.test_CURDL(request, bigip)
# End Radius tests

# Begin Ramcache tests
##placeholder
# End Ramcache tests

# Begin Request Adapt tests -- no attribute Description
class TestRequestAdapt(object):
    def test_request_adapt(self, request, bigip):
        rq_adp = HelperTest( end_lst, 30)
        rq_adp.test_CURDL(request, bigip)
# End Request Adapt tests

# Begin Request Log tests
class TestRequestLog(object):
    def test_request_log(self, request, bigip):
        rq_log = HelperTest(end_lst, 31)
        rq_log.test_CURDL(request, bigip)
# End Request Log tests

# Begin Response Adapt tests  -- no attribute Description
class TestResponseAdapt(object):
    def test_response_adapt(self, request, bigip):
        res_adp = HelperTest(end_lst, 32)
        res_adp.test_CURDL(request, bigip)
# End Response Adapt tests

# Begin Rewrite tests
## placeholder
# End Rewrite tests

# Begin Rstps tests
class TestRstps(object):
    def test_rstps(self, request, bigip):
        rstps = HelperTest(end_lst, 33)
        rstps.test_CURDL(request, bigip)
# End Rstps tests

# Begin Sctps tests
class TestSctps(object):
    def test_sctps(self, request, bigip):
        sctps = HelperTest(end_lst, 34)
        sctps.test_CURDL(request, bigip)
# End Sctps tests

# Begin Server Ldap tests
class TestServerLdap(object):
    def test_server_ldap(self, request, bigip):
        sldap = HelperTest(end_lst, 35)
        sldap.test_CURDL(request, bigip)
# End Server Ldap tests

# Begin Server Ssl tests
class TestServerSsl(object):
    def test_server_ssl(self, request, bigip):
        sssl = HelperTest(end_lst, 36)
        sssl.test_CURDL(request, bigip)
# End Server Ldap tests

# Begin Sip tests
class TestSip(object):
    def test_sip(self, request, bigip):
        sip = HelperTest(end_lst, 37)
        sip.test_CURDL(request, bigip)
# End Sip tests

# Begin Smtp tests
class TestSmtp(object):
    def test_smtp(self, request, bigip):
        smtp = HelperTest(end_lst, 38)
        smtp.test_CURDL(request, bigip)
# End Smtp tests

# Begin Smtps tests -- this needs some special treatment as it barfs with name conflicts
class TestSmtps(object):
    def test_smtps(self, request, bigip):
        smtps = HelperTest(end_lst, 39)
        smtps.test_CURDL(request, bigip)
# End Smtps tests

# Begin Sock tests --needs dns resolver and does not support description
class TestSock(object):
    def test_sock(self, request, bigip):
        socks = HelperTest(end_lst, 40)
        socks.test_CURDL(request, bigip)
# End Sock tests

# Begin Spdy tests
class TestSpdy(object):
    def test_spdy(self, request, bigip):
        spdy = HelperTest(end_lst, 41)
        spdy.test_CURDL(request, bigip)
# End Spdy tests

# Begin Statistics tests
class TestStatistics(object):
    def test_statistics(self, request, bigip):
        stat = HelperTest(end_lst, 42)
        stat.test_CURDL(request, bigip)
# End Statistics tests

# Begin Stream tests
class TestStream(object):
    def test_stream(self, request, bigip):
        stream = HelperTest(end_lst, 43)
        stream.test_CURDL(request, bigip)
# End Stream tests

# Begin Tcp tests
class TestTcp(object):
    def test_tcp(self, request, bigip):
        testcp = HelperTest(end_lst, 44)
        testcp.test_CURDL(request, bigip)
# End Tcp tests

# Begin Tftp tests
class TestTftp(object):
    def test_tftp(self, request, bigip):
        tftp = HelperTest(end_lst, 45)
        tftp.test_CURDL(request, bigip)
# End Tftp tests

# Begin Udp tests
class TestUdp(object):
    def test_udp(self, request, bigip):
        tesudp = HelperTest(end_lst, 46)
        tesudp.test_CURDL(request, bigip)
# End Udp tests

# Begin Wa Cache tests
## placeholder
# End Wa Cache tests

# Begin WebAcceleration tests --no attribute description
class TestWebAcceleration(object):
    def test_web_acceleration(self, request, bigip):
        wa = HelperTest(end_lst, 47)
        wa.test_CURDL(request, bigip)
# End Web Acceleration tests

# Begin Web Security tests -- no attribute description
class TestWebSecurity(object):
    def test_web_security(self, request, bigip):
        ws = HelperTest(end_lst, 48)
        ws.test_CURDL(request, bigip)
# End Web Security tests

# Begin Xml tests
class TestXml(object):
    def test_xml(self, request, bigip):
        testxml = HelperTest(end_lst, 49)
        testxml.test_CURDL(request, bigip)
# End Xml tests


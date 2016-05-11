
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
    def __init__(self, partition, name, item, idx):
        self.name = name
        self.partition = partition
        self.item = item
        self.idx = idx


    def fullstring(self):
        if self.item[self.idx].lower()[-2:] == '_s':
            endind = 2
        else:
            endind = 1
        full_str = '.' +self.item[self.idx][:-endind]
        return full_str.lower()


    def setup_test(self, request, bigip):
        def teardown():
            if profile.exists(name=self.name, partition=self.partition):
                profile.delete()
        request.addfinalizer(teardown)
        hc = common+self.item[self.idx].lower()
        hc1 = eval(hc)
        profile = eval(hc + self.fullstring())
        profile.create(name=self.name, partition=self.partition)
        return hc1, profile

# Begin Analytics tests
##placeholder
# End Analytics tests

# Begin Analytics tests

# End Analytics tests


# Begin HTTP tests
class TestHttp(object):
    def test_CURDL(self, request, bigip):
        h = HelperTest('Common', 'test1', end_lst, 15)

        # Testing create
        hc1, http1 = h.setup_test(request, bigip)
        assert http1.name == 'test1'

        # Testing update
        http1.description = TESTDESCRIPTION
        http1.update()
        assert http1.description == TESTDESCRIPTION

        # Testing refresh
        http1.description = ''
        http1.refresh()
        assert http1.description == TESTDESCRIPTION

        # Testing load
        http2 = hc1.http
        http2.load(partition='Common', name='test1')
        assert http2.selfLink == http1.selfLink

# End HTTP tests

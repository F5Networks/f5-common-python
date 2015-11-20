import mock


class BigIPMock(object):

    def __init__(self, response=mock.MagicMock()):
        self.icontrol = self._create_icontrol()
        self.icr_session = self._create_icr_session()
        self.icr_url = 'https://host-abc/mgmt/tm'
        self.response = response

    def _create_icr_session(self):

        def mock_response(url, timeout):
            return self.response

        icr_session = mock.MagicMock()
        icr_session.delete = mock_response
        icr_session.get = mock_response
        icr_session.patch = mock_response
        icr_session.post = mock_response
        icr_session.put = mock_response

        return icr_session

    def _create_icontrol(self):

        return mock.MagicMock()

import mock


class BigIPMock(object):
    """Mock BigIP object

    Mocks a BigIP object by substituting a mock icr_session object which
    returns a user created mock response object. To use, create a mock response
    object which will get returned by any icr_session HTTP method, then create
    an interface object, passing in this BigIPMock object.

    Example:

        # Create a mock response object with status code and JSON. Here
        # read_json_file() is used to get mock JSON, but you can always pass
        # in a JSON string, or create a dictionary object and convert to JSON
        # using json.loads().
        response = BigIPMock.create_mock_response(
          200, BigIPMock.read_json_file("f5/bigip/interfaces/test/pool.json"))

        # Create BigIP object, passing in mocked response object
        big_ip = BigIPMock(response)

        # Create interface object
        test_pool = Pool(big_ip)

        # Call interface method which will receive mock response object created
        # above when it calls the icr_session method get().
        description = test_pool.get_description("my-Pool")
    """

    def __init__(self, response=mock.Mock()):
        """Initializes BigIPMock object.

        :param response: Mock response object to return from icr_session calls.
        :return:
        """
        self.icontrol = self._create_icontrol()
        self.icr_session = self._create_icr_session()
        self.icr_url = 'https://host-abc/mgmt/tm'
        self.response = response

    def _create_icontrol(self):
        return mock.Mock()

    def _create_icr_session(self):
        """Creates a mock icr_session object.

        This mocked icr_session substitutes basic request library
        methods (get, put, post, etc.) with a method that simply
        returns a mocked response object. Set the response on the BigIPMock
        object before calling one of the icr_session methods.

        :rtype object: mock session object.
        """

        def mock_response(url, timeout):
            return self.response

        icr_session = mock.Mock()
        icr_session.delete = mock_response
        icr_session.get = mock_response
        icr_session.patch = mock_response
        icr_session.post = mock_response
        icr_session.put = mock_response

        return icr_session

    @staticmethod
    def create_mock_response(status_code, json):
        """Creates a mock HTTP response.

        :param int status_code: HTTP response code to mock.
        :param string json: JSON string to mock.
        :rtype object: mock HTTP response object.
        """
        response = mock.Mock()
        response.status_code = status_code
        response.text = json

        return response

    @staticmethod
    def read_json_file(filename):
        """Reads JSON file, returning a JSON string.

        The file must contain a valid JSON object, for example:
        {"key": "value"...} or
        {"key": {"key": "value"}...}

        :param string name: Name of file containing JSON object.
        :rtype string: JSON object as a string.
        """

        file = open(filename)
        s = file.read()
        assert s.__len__() > 0

        return s

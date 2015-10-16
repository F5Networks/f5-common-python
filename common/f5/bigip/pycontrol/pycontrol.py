#!/bin/env python

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

import logging
import platform
import ssl

try:
    from urllib2 import ProxyHandler
    from urllib2 import HTTPBasicAuthHandler
    from urllib2 import HTTPSHandler
    from urllib import pathname2url
    import StringIO
except ImportError:
    from urllib.request import ProxyHandler  # @UnusedImport
    from urllib.request import HTTPBasicAuthHandler  # @UnusedImport
    from urllib.request import HTTPSHandler  # @UnusedImport
    from urllib.request import pathname2url
    from io import StringIO as StringIO  # @NoMove

from suds.cache import Cache
from suds.client import Client
from suds.client import ServiceSelector
from suds.client import Factory
from suds.options import Options
from suds.plugin import PluginContainer
from suds.reader import DefinitionsReader
from suds.servicedefinition import ServiceDefinition
from suds.wsdl import Definitions
from suds.xsd.doctor import Import, ImportDoctor
from suds import transport

# Fix missing imports. These can be global, as it applies to all f5 WSDLS.
IMP = Import('http://schemas.xmlsoap.org/soap/encoding/')
DOCTOR = ImportDoctor(IMP)
ICONTROL_URI = '/iControl/iControlPortal.cgi'
SESSION_WSDL = 'System.Session'

__version__ = '2.1'
__build__ = 'r3'


class BIGIP(object):
    """
    Wrap suds client object(s) and create a user-friendly class to use.
    """
    def __init__(self, hostname=None, username=None,
                 password=None, wsdls=None, directory=None,
                 fromurl=False, debug=False, proto='https',
                 sessions=False, cache=True, **kwargs):

        self.hostname = hostname
        self.username = username
        self.password = password
        self.directory = directory
        self.sessions = sessions
        self.fromurl = fromurl
        self.proto = proto
        self.debug = debug
        self.kw = kwargs
        self.sessionid = None

        # Setup the in-memory object cache
        if cache:
            self.cache = InMemoryCache()
        else:
            self.cache = None

        if self.debug:
            self._set_trace_logging()

        if not wsdls:
            wsdls = []

        if self.sessions:
            if SESSION_WSDL in wsdls:
                self.wsdls = [x for x in wsdls if not x.startswith(
                                                            'System.Session')]
                self.wsdls.insert(0, SESSION_WSDL)
            else:
                self.wsdls = wsdls
                self.wsdls.insert(0, SESSION_WSDL)
        else:
            self.wsdls = wsdls

        self.clients = self._get_clients()

        for client in self.clients:
            self._build_suds_interface(client)

    #---------------------
    # Methods to modify active pyControl objects
    #---------------------
    def set_timeout(self, timeout):
        if 0 < timeout <= 300:
            for client in self.clients:
                client.set_options(timeout=timeout)

    def add_interface(self, wsdl):
        if not wsdl in self.wsdls:
            self.wsdls.append(wsdl)
            client = self._get_client(wsdl)
            self._build_suds_interface(client)
            self.clients.append(client)

    def add_interfaces(self, wsdls):
        for wsdl in wsdls:
            if not wsdl in self.wsdls:
                self.wsdls.append(wsdl)
                client = self._get_client(wsdl)
                self._build_suds_interface(client)
                self.clients.append(client)

    #---------------------
    # Setters and getters.
    #---------------------

    def get_sessionid(self):
        """Fetch a session identifier from a v11.x BigIP."""
        mod = getattr(self, 'System')
        sessionid = getattr(mod, 'Session').get_session_identifier()
        return sessionid

    @staticmethod
    def set_sessionid(sessionid, client):
        """
        Sets the session header for a client.
        @sessionid (String) - session_id to add to the
                               X-iControl-Session header.
        @client - client object.
        """
        client.set_options(headers={'X-iControl-Session': sessionid})

    #---------------------
    # Private methods
    #---------------------

    def _build_suds_interface(self, client):
        location = '%s://%s%s' % (self.proto, self.hostname, ICONTROL_URI)

        self._set_module_attributes(client)
        self._set_interface_attributes(client)
        self._set_interface_sudsclient(client)
        self._set_type_factory(client)
        self._set_interface_methods(client)
        client.factory.separator('_')
        client.set_options(location=location, cache=self.cache)

        if self.sessions:
            if self.sessionid:
                pass
            else:
                self.sessionid = self.get_sessionid()

            self.set_sessionid(self.sessionid.__str__(), client)

    def _get_client(self, wsdl):
        url = self._set_url(wsdl)
        return self._get_suds_client(url, **self.kw)

    def _get_clients(self):
        """ Get a suds client for the wsdls passed in."""
        clients = []
        for wsdl in self.wsdls:
            client = self._get_client(wsdl)
            clients.append(client)
        return clients

    @staticmethod
    def _get_module_name(c):
        """ Returns the module name. Ex: 'LocalLB' """
        return c.sd[0].service.name.split('.')[0]

    def _get_module_object(self, c):
        """ Returns a module object (e.g. LocalLB) """
        return getattr(self, self._get_module_name(c))

    @staticmethod
    def _get_interface_name(c):
        """
        Returns the interface name. Ex: 'Pool' from 'LocalLB.Pool'
        """
        return c.sd[0].service.name.split('.')[1]

    def _get_interface_object(self, c, module):
        """
        Returns an interface object (e.g. Pool). Takes a client
        object and a module object as args.
        """
        return getattr(module, self._get_interface_name(c))

    @staticmethod
    def _get_methods(c):
        """
        Get and return a list of methods for a
        specific iControl interface
        """
        methods = [method[0] for method in c.sd[0].ports[0][1]]
        return methods

    def _get_suds_client(self, url, **kw):
        """
        Make a suds client for a specific WSDL (via url).
        Added new Suds cache features. Warning: These don't work on
        Windows. *nix should be fine. Also exposed general kwargs to
        pass down to Suds for advance users who don't want to deal
        with set_options().
        """
        if not url.startswith("https"):
            t = transport.http.HttpAuthenticated(username=self.username,
                                                 password=self.password)
            c = ROClient(url, transport=t, username=self.username,
                         password=self.password, doctor=DOCTOR, **kw)
        else:
            t = HTTPSUnVerifiedCertTransport(username=self.username,
                                             password=self.password)
            c = ROClient(url, transport=t, username=self.username,
                         password=self.password, doctor=DOCTOR, **kw)
        return c

    def _set_url(self, wsdl):
        """
        Set the path of file-based wsdls for processing.
        If not file-based, return a fully qualified url
        to the WSDL.
        """
        if self.fromurl:
            if wsdl.endswith('wsdl'):
                wsdl.replace('.wsdl', '')

            qstring = '?WSDL=%s' % wsdl
            return 'https://%s%s' % (self.hostname, ICONTROL_URI + qstring)
        else:
            if wsdl.endswith('wsdl'):
                pass
            else:
                wsdl += '.wsdl'

            # Check for windows and use goofy paths. Otherwise assume *nix
            if platform.system().lower() == 'windows':
                url = 'file:' + pathname2url(self.directory + '\\' + wsdl)
            else:
                url = 'file:' + pathname2url(self.directory + '/' + wsdl)
        return url

    def _set_module_attributes(self, c):
        """ Sets appropriate attributes for a Module. """
        module = self._get_module_name(c)
        if hasattr(self, module):
            return
        else:
            setattr(self, module, ModuleInstance(module))

    def _set_interface_sudsclient(self, c):
        """
        Set an attribute that points to the actual suds client. This
        will allow for power-users to get at suds client internals.
        """
        module = self._get_module_object(c)
        interface = self._get_interface_object(c, module)
        setattr(interface, 'suds', c)

    def _set_interface_attributes(self, c):
        """ Sets appropriate attributes for a Module. """
        module = self._get_module_object(c)
        interface = self._get_interface_name(c)
        setattr(module, interface, InterfaceInstance(interface))

    def _set_interface_methods(self, c):
        """
        Sets up methods as attributes for a particular iControl interface.
        Method keys (attrs) point to suds.service objects for the interface.
        """
        module = self._get_module_object(c)
        interface = self._get_interface_object(c, module)
        methods = self._get_methods(c)

        for method in methods:
            suds_method = getattr(c.service, method)
            setattr(interface, method, suds_method)
            m = getattr(interface, method)
            self._set_method_input_params(c, m, method)
            self._set_return_type(c, m, method)

    @staticmethod
    def _set_method_input_params(c, interface_method, method):
        """
        Set the method input argument attribute named 'params' for easy
        reference.
        """
        m = c.sd[0].ports[0][0].method(method)
        params = []
        for x in m.soap.input.body.parts:
            params.append((x.name, x.type[0]))
        setattr(interface_method, 'params', params)

    @staticmethod
    def _set_return_type(c, interface_method, method):
        """ Sets the return type in an attribute named response_type"""
        m = c.sd[0].ports[0][0].method(method)
        if len(m.soap.output.body.parts):
            res = m.soap.output.body.parts[0].type[0]
            setattr(interface_method, 'response_type', res)
        else:
            setattr(interface_method, 'response_type', None)

    def _set_type_factory(self, c):
        factory = getattr(c, 'factory')
        module = self._get_module_object(c)
        interface = self._get_interface_object(c, module)
        setattr(interface, 'typefactory', factory)

    @staticmethod
    def _set_trace_logging():
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('suds.client').setLevel(logging.DEBUG)


class ModuleInstance(object):
    """ An iControl module object to set attributes against. """
    def __init__(self, name):
        self.name = name


class InterfaceInstance(object):
    """ An iControl interface object to set attributes against. """
    def __init__(self, name):
        self.name = name


class ROClient(Client):
    def __init__(self, url, **kwargs):
        """
        @param url: The URL for the WSDL.
        @type url: str
        @param kwargs: keyword arguments.
        @see: L{Options}
        """
        options = Options()
        options.transport = transport.https.HttpAuthenticated()
        self.options = options
        options.cache = InMemoryCache()
        self.set_options(**kwargs)
        reader = DefinitionsReader(options, Definitions)
        self.wsdl = reader.open(url)
        plugins = PluginContainer(options.plugins)
        plugins.init.initialized(wsdl=self.wsdl)
        self.factory = Factory(self.wsdl)
        self.service = ServiceSelector(self, self.wsdl.services)
        self.sd = []
        for s in self.wsdl.services:
            sd = ServiceDefinition(self.wsdl, s)
            self.sd.append(sd)
        self.messages = dict(tx=None, rx=None)


class InMemoryCache(Cache):
    """
    In-memory cache.

    The contents of the cache is shared between all instances.
    """
    data = {}

    def get(self, objid):
        return self.data.get(objid)

    def getf(self, objid):
        obj = self.get(objid)
        return StringIO(obj) if obj else None

    def put(self, objid, obj):
        self.data[objid] = obj

    def putf(self, objid, fp):
        self.put(fp.read())

    def purge(self, objid):
        del self.data[objid]

    def clear(self):
        self.data = {}


class HTTPSUnVerifiedCertTransport(transport.https.HttpAuthenticated):

    def __init__(self, *args, **kwargs):
        transport.https.HttpAuthenticated.__init__(self, *args, **kwargs)

    def u2handlers(self):
        handlers = []
        handlers.append(ProxyHandler(self.proxy))
        handlers.append(HTTPBasicAuthHandler(self.pm))
        # python ssl Context support - PEP 0466
        if hasattr(ssl, '_create_unverified_context'):
            ssl_context = ssl._create_unverified_context()
            handlers.append(HTTPSHandler(context=ssl_context))
        else:
            handlers.append(HTTPSHandler())
        return handlers


def main():
    import sys
    if len(sys.argv) < 4:
        print("Usage: %s <hostname> <username> <password>" % sys.argv[0])
        sys.exit()

    a = sys.argv[1:]
    b = BIGIP(hostname=a[0],
              username=a[1],
              password=a[2],
              fromurl=True,
              wsdls=['LocalLB.Pool'])

    pools = b.LocalLB.Pool.get_list()
    version = b.LocalLB.Pool.get_version()
    print("Version is: %s\n" % version)
    print("Pools:")
    for x in pools:
        print("\t%s" % x)

if __name__ == '__main__':
    main()

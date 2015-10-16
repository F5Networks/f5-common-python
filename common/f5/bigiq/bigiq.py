""" Classes and functions for configuring BIG-IQ """
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
# pylint: disable=star-args

import json
import logging
import requests

LOG = logging.getLogger(__name__)


class BIGIQ(object):
    """An interface to a single BIG-IQ

    This class allows someone to make custom HTTP requests to
    a BIG-IQ or use existing well known ones as documented
    in our APIs.

    Every HTTP request made to a BIG-IQ returns the body of
    the response which should contained the JSON representation
    of the resource in the HTTP request.
    """

    # URI segments for top-level BIG-IQ namespaces
    MGMT_ENDPOINT_URI_SEGMENT = "mgmt"
    NS_CM_URI_SEGMENT = "cm"
    NS_SHARED_URI_SEGMENT = "shared"

    # URI segments for any BIG-IQ module
    NS_INDEX_URI_SEGMENT = "index"
    NS_RESOLVER_URI_SEGMENT = "resolver"

    SHARED_CONFIG_URI_SEGMENT = "config"

    UTILITY_URI_SEGMENT_EXAMPLE = 'example'

    # Query component identifiers used when constructing an indexer query
    CONFIG_QUERY_KEY_INFLATE = 'inflate'
    CONFIG_QUERY_KEY_REF_KIND = 'referenceKind'
    CONFIG_QUERY_KEY_REF_LINK = 'referenceLink'
    CONFIG_QUERY_KEY_REF_METHOD = 'referenceMethod'

    REF_METHOD_REF_ANY = 'referenceAny'
    REF_METHOD_REF_KIND = 'resourceReferencesKind'
    REF_METHOD_REF_RESOURCE = 'kindReferencesResource'

    # URI segments for BIG-IQ Cloud module
    SUB_CM_NS_CLOUD_URI_SEGMENT = "cloud"

    CLOUD_CONNECTORS_URI_SEGMENT = "connectors"
    CLOUD_IAPP_URI_SEGMENTS = "iapp"
    CLOUD_NODES_URI_SEGMENT = "nodes"
    CLOUD_PROVIDER_URI_SEGMENT = "provider"
    CLOUD_PROVIDERS_URI_SEGMENT = "providers"
    CLOUD_SERVICES_URI_SEGMENT = "services"
    CLOUD_TEMPLATES_URI_SEGMENT = "templates"
    CLOUD_TENANTS_URI_SEGMENT = "tenants"

    # Cloud Connectors
    CC_TYPE_EC2 = 'ec2'
    CC_TYPE_LOCAL = 'local'
    CC_TYPE_OPENSTACK = 'openstack'
    CC_TYPE_VMWARE_NSX = 'nsx'
    CC_TYPE_VMWARE_VSHIELD = 'vmware'

    # Constants used for constructing URLs
    PATH_SEPARATOR = "/"

    SCHEME_HTTPS = "https"
    SCHEME_SEPARATOR = "://"

    QUERY_COMPONENT_KV_SEPARATOR = "="   # key value separator
    QUERY_COMPONENT_KVP_SEPARATOR = "&"  # key value pair separator
    QUERY_COMPONENT_STARTER = "?"
    QUERY_COMPONENT_TERMINATOR = "#"

    def __init__(self, hostname, username, password):
        """Creates an instance of a BIG-IQ

        :param string hostname: The hostname of the BIG-IQ
        :param string username: The Administrator user name
        :param string password: The Administrator password
        """

        self.hostname = hostname
        self.username = username
        self.password = password

        # Setup our HTTP session to the BIG-IQ
        self.http_session = requests.Session()
        self.http_session.auth = (self.username, self.password)
        self.http_session.verify = False
        self.http_session.headers.update({'Content-Type': 'application/json'})

        # If we are able to successfully query the echo worker
        # we consider ourselves connected
        url = 'https://' + self.hostname + '/mgmt/shared/echo'
        self.http_session.get(url).raise_for_status()

    def delete(self, url):
        """Makes a HTTP DELETE request

        Makes a HTTP DELETE request to the argument provided to the 'url'
        parameter using the HTTP session previously established when
        the instance of this BIGIQ type was created. Thus the URL is
        presumed to be a resource on the BIG-IQ.

        :param string url: The URL to perform a HTTP DELETE on

        """
        response = self.http_session.delete(url)

        response.raise_for_status()

        # no json to parse on delete response
        return

    def get(self, url):
        """Makes a HTTP GET request

        Makes a HTTP GET request to the argument provided to the 'url'
        parameter using the HTTP session previously established when
        the instance of this BIGIQ type was created. Thus the URL is
        presumed to be a resource on the BIG-IQ.

        :param string url: The URL to perform a HTTP GET on

        :return: The JSON response body
        """
        response = self.http_session.get(url)

        response.raise_for_status()

        return response.json()

    def post(self, url, body):
        """Makes a HTTP POST request

        Makes a HTTP POST request to the argument provided to the 'url'
        parameter using the HTTP session previously established when
        the instance of this BIGIQ type was created. Thus the URL is
        presumed to be a resource on the BIG-IQ. The body posted is
        contained in the parameter 'body'. It will be serialized to
        JSON inside this method.

        :param string url: The URL to perform a HTTP POST on
        :param object body: An object that will be serialized to JSON
                            for the body

        :return: The JSON response body
        """
        response = self.http_session.post(url, json.dumps(body))

        response.raise_for_status()

        return response.json()

    def put(self, url, body):
        """Makes a HTTP PUT request

        Makes a HTTP PUT request to the argument provided to the 'url'
        parameter using the HTTP session previously established when
        the instance of this BIGIQ type was created. Thus the URL is
        presumed to be a resource on the BIG-IQ. The body posted is
        contained in the parameter 'body'. It will be serialized to
        JSON inside this method.

        :param string url: The URL to perform a HTTP PUT on
        :param object body: An object that will be serialized to JSON
                            for the body

        :return: The JSON response body
        """
        response = self.http_session.put(url, json.dumps(body))

        response.raise_for_status()

        return response.json()

    def build_bigiq_url(self, uri_path, query_component=None):
        """Builds a URL to a resource on the BIG-IQ

        The URL is that of a 'https' scheme. The URI path is presumed
        to be properly formed. The query component is presumed to be
        properly formed.

        :param string uri_path: The path of the URL
        :param string query_component: The query component of the URI.

        :return: URL
        """

        url = BIGIQ.SCHEME_HTTPS + BIGIQ.SCHEME_SEPARATOR + \
            self.hostname + uri_path

        if query_component:
            url += query_component

        return url

    @staticmethod
    def build_remote_uri_path(*uri_segments):
        """Builds a URI path to a remote resource on a BIG-IQ from URI segments

        URI segments can include leading or trailing path separators. If
        the URI segment doesn't include a leading path separator one is
        added. If the URI segment does include a trailing path separator
        it is removed.

        URI segments in the list should be strings. The types of the
        objects provided in uri_segments isn't type checked so providing
        non-string type objects may result in unexpected behavior with
        the possibility of an error occurring.

        The empty string will be returned if the list of URI segments is
        empty.

        The URI path returned will be prefixed with the 'mgmt' URI segment.

        :param list uri_segments: List of URI segments of object type string.

        :return: URI path
        """

        uri_path = ""

        if not uri_segments:
            return uri_path

        for uri_segment in uri_segments:
            # Skip the URI segment if it is empty
            if not uri_segment:
                continue

            # Add the URI segment with a leading '/' if it doesn't have one
            if uri_segment[0] == BIGIQ.PATH_SEPARATOR:
                uri_path += uri_segment
            else:
                uri_path += BIGIQ.PATH_SEPARATOR + uri_segment

            # Chop off the trailing '/' on the URI segment if it had one
            if uri_path[-1] == BIGIQ.PATH_SEPARATOR:
                uri_path = uri_path[:-1]

        start_path = BIGIQ.PATH_SEPARATOR + BIGIQ.MGMT_ENDPOINT_URI_SEGMENT
        if uri_path and not uri_path.startswith(start_path):
            uri_path = start_path + uri_path

        return uri_path

    @staticmethod
    def build_query_component(**key_value_pairs):
        """Builds a query component to be used in a URL

        Takes a dictionary and from the KvPs in the dictionary
        builds a query string made out of the KvPs.

        :param dict key_value_pairs: The KvPs to turn into the query component

        :return: string that can be used as the query component in an URL
        """
        if not key_value_pairs:
            return ""

        query_component = BIGIQ.QUERY_COMPONENT_STARTER

        for key, value in key_value_pairs.items():
            # Skip the key if it is empty
            if not key:
                continue
            add_component = key + BIGIQ.QUERY_COMPONENT_KV_SEPARATOR + \
                value + BIGIQ.QUERY_COMPONENT_KVP_SEPARATOR
            # Add the key value pair to the query string
            query_component += add_component

        # Chop off the trailing '&' on the query component
        query_component = query_component[:-1]

        # Terminate the query component with the '#' character
        query_component += BIGIQ.QUERY_COMPONENT_TERMINATOR

        return query_component

    def get_related(self, kind, self_link, inflate=False):
        """Makes an indexer query to get all kinds related by a reference

        :param string kind: The kind of object we are interested in
        :param string self_link: The 'selfLink' property on the resource
                                 referencing the objects
        :param boolean inflate: Whether the results should be inflated
                                or not (default is 'False')

        :return: List of all referenced objects serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_SHARED_URI_SEGMENT,
            BIGIQ.NS_INDEX_URI_SEGMENT,
            BIGIQ.SHARED_CONFIG_URI_SEGMENT)

        query_component = BIGIQ.build_query_component(**{
            BIGIQ.CONFIG_QUERY_KEY_REF_KIND: kind,
            BIGIQ.CONFIG_QUERY_KEY_REF_LINK: self_link,
            BIGIQ.CONFIG_QUERY_KEY_REF_METHOD:
            BIGIQ.REF_METHOD_REF_KIND,
            BIGIQ.CONFIG_QUERY_KEY_INFLATE: '%s' % inflate})

        url = self.build_bigiq_url(uri_path, query_component)

        response = self.get(url)

        return response.get('items', [])

    def get_resource_example(self, uri_path):
        """Gets the example of a resource

        :param string uri_path: The resource to get the example of

        :return: Example of the resource serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            uri_path, BIGIQ.UTILITY_URI_SEGMENT_EXAMPLE)

        url = self.build_bigiq_url(uri_path)

        return self.get(url)

    def get_cloud_connectors(self, connector_type):
        """Gets all the cloud connectors of a specific type

        :param string connector_type: The type of the connector to get
                                      (e.g. 'openstack', 'ec2', etc.)

        :return: List of connectors serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_CONNECTORS_URI_SEGMENT,
            connector_type)

        url = self.build_bigiq_url(uri_path)

        try:
            response = self.get(url)
        except requests.exceptions.HTTPError as httperr:
            if '404' in str(httperr):
                LOG.debug("No cloud connectors found: %s" % str(httperr))
                return []
            else:
                LOG.error("ERROR: getting cloud connectors")
                raise

        return response.get('items', [])

    def post_cloud_connector(self, connector_type, connector):
        """Creates a cloud connector of a specific type

        :param string connector_type: The type of the connector to create
                                      (e.g. 'openstack', 'ec2', etc.)
        :param dict connector: A dictionary representing the connector to be
                               used in the POST body

        :return: Created connector serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_CONNECTORS_URI_SEGMENT,
            connector_type)

        url = self.build_bigiq_url(uri_path)
        LOG.debug("Posting Cloud Connector, URL: %s body: %s"
                  % (url, connector))

        return self.post(url, connector)

    def post_cloud_device(
            self, ip_address, username, password, auto_update=True):
        """Adds a cloud device for management

        :param string ip_address: The address of the device
        :param string username: The username to use when authenticating the
                                device
        :param string password: The password to use when authenticating the
                                device
        :param boolean auto_update: Whether the device should be updated
                                    when managed (defaults to True)

        :return: The managed device serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_SHARED_URI_SEGMENT,
            BIGIQ.NS_RESOLVER_URI_SEGMENT,
            'device-groups',
            'cm-cloud-managed-devices',
            'devices')

        url = self.build_bigiq_url(uri_path)

        body = {}
        body['address'] = ip_address
        body['userName'] = username
        body['password'] = password
        body['rootUser'] = 'root'
        body['rootPassword'] = 'default'
        body['automaticallyUpdateFramework'] = auto_update

        LOG.debug("Posting Cloud Device, URL: %s body: %s"
                  % (url, body))
        return self.post(url, body)

    def get_provider_template(self, provider_template_name):
        """Get a provider template

        :param string provider_template_name: The name of the provider
                      template to get

        :return: The provider template serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_PROVIDER_URI_SEGMENT,
            BIGIQ.CLOUD_TEMPLATES_URI_SEGMENT,
            BIGIQ.CLOUD_IAPP_URI_SEGMENTS,
            provider_template_name)

        url = self.build_bigiq_url(uri_path)

        return self.get(url)

    def post_provider_template(self, provider_template):
        """Creates a provider template

        :param dict provider_template: A dictionary representing the
            provider template to be used in the POST body

        :return: Created provider template serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_PROVIDER_URI_SEGMENT,
            BIGIQ.CLOUD_TEMPLATES_URI_SEGMENT,
            BIGIQ.CLOUD_IAPP_URI_SEGMENTS)

        url = self.build_bigiq_url(uri_path)

        return self.post(url, provider_template)

    def post_tenant(self, tenant):
        """Creates a tenant

        :param dict connector: A dictionary representing the tenant to be
            used in the POST body

        :return: Created tenant serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_TENANTS_URI_SEGMENT)

        url = self.build_bigiq_url(uri_path)

        return self.post(url, tenant)

    def delete_tenant_service(self, tenant_name, service_name):
        """Deletes a tenant service

        :param string tenant_name: The name of the tenant to delete a
             service for
        :param string service_name: The name of the service to delete

        :return: The deleted tenant service serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_TENANTS_URI_SEGMENT,
            tenant_name,
            BIGIQ.CLOUD_SERVICES_URI_SEGMENT,
            BIGIQ.CLOUD_IAPP_URI_SEGMENTS,
            service_name)

        url = self.build_bigiq_url(uri_path)

        return self.delete(url)

    def get_tenant_service(self, tenant_name, service_name):
        """Gets a tenant service

        :param string tenant_name: The name of the tenant to get a service for
        :param string service_name: The name of the service to get

        :return: The tenant service serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_TENANTS_URI_SEGMENT,
            tenant_name,
            BIGIQ.CLOUD_SERVICES_URI_SEGMENT,
            BIGIQ.CLOUD_IAPP_URI_SEGMENTS,
            service_name)

        url = self.build_bigiq_url(uri_path)

        return self.get(url)

    def post_tenant_service(self, tenant_name, service):
        """Creates a tenant service

        :param string tenant_name: The name of the tenant to update a
                                   service for
        :param dict service: A dictionary representing the tenant service
                             to be used in the POST body

        :return: Created tenant service serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_TENANTS_URI_SEGMENT,
            tenant_name,
            BIGIQ.CLOUD_SERVICES_URI_SEGMENT,
            BIGIQ.CLOUD_IAPP_URI_SEGMENTS)

        url = self.build_bigiq_url(uri_path)

        return self.post(url, service)

    def put_tenant_service(self, tenant_name, service_name, service):
        """Updates a tenant service by full replacement

        :param string tenant_name: The name of the tenant to update a
                                   service for
        :param string service_name: The name of the service to update
        :param dict service: A dictionary representing the tenant service
                             to be used in the PUT body

        :return: Updated tenant service serialized to JSON
        """
        uri_path = BIGIQ.build_remote_uri_path(
            BIGIQ.NS_CM_URI_SEGMENT,
            BIGIQ.SUB_CM_NS_CLOUD_URI_SEGMENT,
            BIGIQ.CLOUD_TENANTS_URI_SEGMENT,
            tenant_name,
            BIGIQ.CLOUD_SERVICES_URI_SEGMENT,
            BIGIQ.CLOUD_IAPP_URI_SEGMENTS,
            service_name)

        url = self.build_bigiq_url(uri_path)

        return self.put(url, service)

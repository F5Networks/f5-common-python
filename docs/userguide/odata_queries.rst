OData Queries
==============

The REST service on the BIG-IP® device implements a subset of the Open Data Protocol, which allows a user to refine a set of data based on query parameters. This is especially useful when limiting the number of results returned on a ``get_collection()`` call. The way to use these query parameters with the f5-sdk is shown below:

.. topic:: Examples

**Filter example:** Retrieve only http profiles in a particular partition. Note this is an inclusive filter.
    .. code-block:: python

        mgmt = ManagementRoot('<ip_address>', '<username>', '<password>')
        http_profiles = mgmt.tm.ltm.profile.https
        http_profiles.get_collection(requests_params={'params': '$filter=partition+eq+test_folder'})

**Select example:** Retrieve only the name of the http profiles.
    .. code-block:: python

        http_profiles.get_collection(requests_params={'params': '$select=name'})

**Top example:** Retrieve only a certain number of rows of results from http profiles.
    .. code-block:: python

        http_profiles.get_collection(requests_params={'params': '$top=2'})

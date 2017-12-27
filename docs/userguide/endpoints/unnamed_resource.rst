.. _resource_section:

Unnamed Resource
~~~~~~~~~~~~~~~~

An unnamed resource is a partially configurable object for which the CURDLE :ref:`methods <methods_section>` are supported with the exception of the create and delete methods.

* |refresh|
* |update|
* |load|
* |exists|

In the F5® SDK, an unnamed resource is instantiated via its :ref:`collection <collection_section>`. Once loaded, unnamed resources contain attributes that map to the JSON fields returned by the BIG-IP®.

.. topic:: Example: Load a :class:`f5.bigip.tm.sys.dns` |Unnamed Resource| object.

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'admin', 'admin')
        >>> dns = mgmt.tm.sys.dns.load()
        >>> pp(dns.raw)
        {
         u'description': u'configured-by-dhcp',
         u'kind': u'tm:sys:dns:dnsstate',
         u'nameServers': [u'10.10.10.1', u'8.8.8.8'],
         u'numberOfDots': 0,
         u'search': [u'localdomain', u'test.local'],
         u'selfLink': u'https://localhost/mgmt/tm/sys/dns?ver=13.1.0.1'
        }

    The output of the :attr:`f5.bigip.tm.sys.dns` (above) shows all of the available attributes.

    Once you have loaded the object, you can access the attributes as shown below.

    .. code-block:: python

        dns.nameServers = ['2.2.2.2', '3.3.3.3']
        dns.update()



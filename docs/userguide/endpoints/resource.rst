.. _resource_section:

Resource
~~~~~~~~

``kind``: ``state``

A resource is a fully configurable object for which the CURDLE :ref:`methods <methods_section>` are supported.

* |create|
* |refresh|
* |update|
* |delete|
* |load|
* |exists|

In the F5® SDK, a resource is instantiated via its :ref:`collection <collection_section>`. Once created or loaded, resources contain attributes that map to the JSON fields returned by the BIG-IP®.

.. topic:: Example: Load a :class:`f5.bigip.tm.ltm.node.Node` |Resource| object.

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'myuser', 'mypass')
        >>> n = mgmt.tm.ltm.nodes.node.load(partition='Common', name='192.168.15.15')
        >>> print n.raw
        {
          "kind":"tm:ltm:node:nodestate",
          "name":"192.168.15.15",
          "partition":"Common",
          "fullPath":"/Common/192.168.15.15",
          "generation":16684,
          "selfLink":"https://localhost/mgmt/tm/ltm/node/~Common~192.168.15.15?ver=11.6.0",
          "address":"192.168.15.15",
          "connectionLimit":0,
          "dynamicRatio":1,
          "ephemeral":"false",
          "fqdn":{
            "addressFamily":"ipv4",
            "autopopulate":"disabled",
            "downInterval":5,
            "interval":3600
          },
          "logging":"disabled",
          "monitor":"default",
          "rateLimit":"disabled",
          "ratio":1,
          "session":"user-enabled",
          "state":"unchecked"
        }

    The output of the :attr:`f5.bigip.tm.ltm.node.Node.raw` (above) shows all of the available attributes.

    Once you have loaded the object, you can access the attributes as shown below.

    .. code-block:: python

        >>> n.fqdn['downInterval'] = 10
        >>> n.logging = 'enabled'
        >>> n.update()

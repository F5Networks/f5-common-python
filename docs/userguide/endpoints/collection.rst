.. _collection_section:

Collection
~~~~~~~~~~

``kind``: ``collectionstate``

A collection is similar to an |Organizing Collection Section| in that no configurations can be applied to it. A collection differs from an organizing collection in that a collection only contains references to objects of the same type in its ``items`` parameter.

.. include:: ../SDK_plural_note.rst

Because the collection ``kind`` is ``collectionstate``, only the |exists| method is supported for these objects. This method returns a list of the objects in the collection. For example, :meth:`~f5.bigip.resource.Collection.get_collection`.

The example below shows the JSON you would get back from a collection endpoint. Note that it contains an ``items`` attribute that contains |Resource| objects (we know the objects are resources because their ``kind`` ends in ``state``).

.. topic:: Example

    .. code-block:: json
        :emphasize-lines: 6, 30

        {
          "kind": "tm:ltm:node:nodecollectionstate",
          "selfLink": "https://localhost/mgmt/tm/ltm/node?ver=11.6.0",
          "items": [
            {
              "kind": "tm:ltm:node:nodestate",
              "name": "192.168.15.15",
              "partition": "Common",
              "fullPath": "/Common/192.168.15.15",
              "generation": 16684,
              "selfLink": "https://localhost/mgmt/tm/ltm/node/~Common~192.168.15.15?ver=11.6.0",
              "address": "192.168.15.15",
              "connectionLimit": 0,
              "dynamicRatio": 1,
              "ephemeral": "false",
              "fqdn": {
                "addressFamily": "ipv4",
                "autopopulate": "disabled",
                "downInterval": 5,
                "interval": 3600
              }
             "logging": "disabled",
             "monitor": "default",
             "rateLimit": "disabled",
             "ratio": 1,
             "session": "user-enabled",
             "state": "unchecked"
          },
          {
            "kind": "tm:ltm:node:nodestate",
            "name": "192.168.16.16",
            "partition": "Common",
            "fullPath": "/Common/192.168.16.16",
            "generation": 16685,
            "selfLink": "https://localhost/mgmt/tm/ltm/node/~Common~192.168.16.16?ver=11.6.0",
            "address": "192.168.16.16",
            "connectionLimit": 0,
            "dynamicRatio": 1,
            "ephemeral": "false",
            "fqdn": {
              "addressFamily": "ipv4",
              "autopopulate": "disabled",
              "downInterval": 5,
              "interval": 3600
            },
            "logging": "disabled",
            "monitor": "default",
            "rateLimit": "disabled",
            "ratio": 1,
            "session": "user-enabled",
            "state": "unchecked"
          }
         ]
        }




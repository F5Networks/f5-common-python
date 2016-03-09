.. _collection_section:

Collection
~~~~~~~~~~

``kind``: ``collectionstate``

A collection is similar to an |Organizing Collection Section| in that no configurations can be applied to it. A collection differs from an organizing collection in that a collection only contains references to objects of the same type in its ``items`` parameter.

.. include:: ../SDK_plural_note.rst

You can use :meth:`~f5.bigip.resource.Collection.get_collection` to get a list of the objects in the collection.

The example below shows the JSON you would get back from a REST collection
endpoint. Note that it contains an ``items`` attribute that contains
|Resource| objects (we know the objects are resources because their ``kind`` ends in ``state``).

.. topic:: Example

    .. code-block:: json
        :emphasize-lines: 4, 6, 37

        {
            kind: "tm:ltm:pool:poolcollectionstate",
            selfLink: "https://localhost/mgmt/tm/ltm/pool?ver=11.6.0",
            items: [
                {
                    kind: "tm:ltm:pool:poolstate",
                    name: "my_newpool",
                    partition: "Common",
                    fullPath: "/Common/my_newpool",
                    generation: 76,
                    selfLink: "https://localhost/mgmt/tm/ltm/pool/~Common~my_newpool?ver=11.6.0",
                    allowNat: "yes",
                    allowSnat: "yes",
                    description: "This is my pool",
                    ignorePersistedWeight: "disabled",
                    ipTosToClient: "pass-through",
                    ipTosToServer: "pass-through",
                    linkQosToClient: "pass-through",
                    linkQosToServer: "pass-through",
                    loadBalancingMode: "round-robin",
                    minActiveMembers: 0,
                    minUpMembers: 0,
                    minUpMembersAction: "failover",
                    minUpMembersChecking: "disabled",
                    queueDepthLimit: 0,
                    queueOnConnectionLimit: "disabled",
                    queueTimeLimit: 0,
                    reselectTries: 0,
                    serviceDownAction: "none",
                    slowRampTime: 10,
                    membersReference: {
                    link: "https://localhost/mgmt/tm/ltm/pool/~Common~my_newpool/members?ver=11.6.0",
                    isSubcollection: true
                    }
                },
                {
                    kind: "tm:ltm:pool:poolstate",
                    name: "mypool",
                    partition: "Common",
                    fullPath: "/Common/mypool",
                    generation: 121,
                    selfLink: "https://localhost/mgmt/tm/ltm/pool/~Common~mypool?ver=11.6.0",
                    allowNat: "yes",
                    allowSnat: "yes",
                    ignorePersistedWeight: "disabled",
                    ipTosToClient: "pass-through",
                    ipTosToServer: "pass-through",
                    linkQosToClient: "pass-through",
                    linkQosToServer: "pass-through",
                    loadBalancingMode: "round-robin",
                    minActiveMembers: 0,
                    minUpMembers: 0,
                    minUpMembersAction: "failover",
                    minUpMembersChecking: "disabled",
                    queueDepthLimit: 0,
                    queueOnConnectionLimit: "disabled",
                    queueTimeLimit: 0,
                    reselectTries: 0,
                    serviceDownAction: "none",
                    slowRampTime: 10,
                    membersReference: {
                    link: "https://localhost/mgmt/tm/ltm/pool/~Common~mypool/members?ver=11.6.0",
                    isSubcollection: true
                    }
                },
            ]
        }





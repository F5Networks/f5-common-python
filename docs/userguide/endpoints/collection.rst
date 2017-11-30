.. _collection_section:

Collection
~~~~~~~~~~

``kind``: ``collectionstate``

A :dfn:`collection` is similar to an |Organizing Collection Section| in it is not a configurable object. Unlike an `OrganizingCollection` collection,
however, a `Collection` only contains references to objects (or, resources) of the same type.

.. include:: ../SDK_plural_note.rst

.. topic:: Example: Use :meth:`f5.bigip.tm.ltm.pools.get_collection` to get a list of the objects in the :mod:`f5.bigip.tm.ltm.pool` collection.

    The ``items`` attribute in the JSON returned contains |Resource Section| objects that all share the same ``kind``. We can tell that these objects are resources because the ``kind`` ends in ``state``.

    .. code-block:: js
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





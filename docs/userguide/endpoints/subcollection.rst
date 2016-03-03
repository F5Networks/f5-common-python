.. _subcollection_section:

Subcollection
~~~~~~~~~~~~~

``kind``: ``collectionstate``

A subcollection is a |Collection| that's attached to a higher-level |Resource| object. Subcollections are almost exactly the same as collections; the exception is that they can only be accessed via the resource they're attached to (the 'parent' resource). A subcollection can be identified by the value ``isSubcollection: true``, followed by an ``items`` attribute listing the subcollection's resources.

Because the subcollection ``kind`` is ``collectionstate``, the :ref:`methods <methods_section>` available are limited to |exists|.

.. _subcollection_example:

.. topic:: Example

   A ``pool`` resource has a ``members_s`` subcollection attached to it; you must create or load the 'parent' resource (``pool``) before you can access the subcollection (``members_s``).

   >>> from f5.bigip import BigIP
   >>> bigip = BigIP('192.168.1.1', 'myuser', 'mypass')
   >>> pool = bigip.ltm.pools.pool.load(partition='Common', name='p1')
   >>> members = pool.members_s.get_collection()

   Note that the subcollection -- ``members`` -- is plural, so the subcollection object name ends in ``_s``.

The JSON returned for a pool with one member is shown below. Notice the highlighted rows which indicate the subcollection.

.. topic:: Example

    .. code-block:: json
        :emphasize-lines: 26, 28, 29

        {
            "kind": "tm:ltm:pool:poolstate",
            "name": "p1",
            "partition": "Common",
            "fullPath": "/Common/p1",
            "generation": 18703,
            "selfLink": "https://localhost/mgmt/tm/ltm/pool/~Common~p1?expandSubcollections=true&ver=11.6.0",
            "allowNat": "yes",
            "allowSnat": "yes",
            "ignorePersistedWeight": "disabled",
            "ipTosToClient": "pass-through",
            "ipTosToServer": "pass-through",
            "linkQosToClient": "pass-through",
            "linkQosToServer": "pass-through",
            "loadBalancingMode": "round-robin",
            "minActiveMembers": 0,
            "minUpMembers": 0,
            "minUpMembersAction": "failover",
            "minUpMembersChecking": "disabled",
            "queueDepthLimit": 0,
            "queueOnConnectionLimit": "disabled",
            "queueTimeLimit": 0,
            "reselectTries": 0,
            "serviceDownAction": "none",
            "slowRampTime": 10,
            "membersReference": {
                "link": "https://localhost/mgmt/tm/ltm/pool/~Common~p1/members?ver=11.6.0",
                "isSubcollection": true,
                "items": [
                      {
                        "kind": "tm:ltm:pool:members:membersstate",
                        "name": "n1:80",
                        "partition": "Common",
                        "fullPath": "/Common/n1:80",
                        "generation": 18703,
                        "selfLink": "https://localhost/mgmt/tm/ltm/pool/~Common~p1/members/~Common~n1:80?ver=11.6.0",
                        "address": "192.168.51.51",
                        "connectionLimit": 0,
                        "dynamicRatio": 1,
                        "ephemeral": "false",
                        "fqdn": {
                          "autopopulate": "disabled",
                        }
                        "inheritProfile": "enabled",
                        "logging": "disabled",
                        "monitor": "default",
                        "priorityGroup": 0,
                        "rateLimit": "disabled",
                        "ratio": 1,
                        "session": "user-enabled",
                        "state": "unchecked",
                      }
                ]
            },
        }



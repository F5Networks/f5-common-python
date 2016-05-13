.. _subcollection_resource_section:

Subcollection Resource
~~~~~~~~~~~~~~~~~~~~~~

``kind``: ``state``

A subcollection resource is essentially the same as a :ref:`resource <resource_section>`. As with collections and subcollections, the only difference between the two is that you must access the subcollection resource via the subcollection attached to the main resource.

.. topic:: Example

   To build on the :ref:`subcollection example <subcollection_example>`: ``pool`` is the resource, ``members_s`` is the subcollection, and ``members`` (the actual pool member) is the subcollection resource.

   >>> from f5.bigip import ManagementRoot
   >>> mgmt = ManagementRoot('192.168.1.1', 'myuser', 'mypass')
   >>> pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name='p1')
   >>> member = pool.members_s.members.load(partition='Common', name='n1:80')

   The JSON below shows a :obj:`f5.bigip.tm.ltm.pool.members_s.members` object.

   .. code-block:: json
       :emphasize-lines: 2

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

.. tip::

    It's easy to tell that this is a Resource object because the ``kind`` is ``state``, not ``collectionstate``.

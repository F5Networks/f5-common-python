Python Object Paths
===================

The object classes used in the SDK directly correspond to the REST endpoints you'd use to access the objects via the API. Remembering the patterns below will help you easily derive an SDK object class from an object URI.

1. Objects take the form ``f5.<product>.<organizing_collection>.<collection>.<resource>.<subcollection>.<resource>``.

2. The collection and the resource generally have the same name, so the collection is the *plural* version of the resource. This means that you add ``s`` to the end of the resource to get the collection, *unless* the resource already ends in ``s``. If the resource is already plural, add ``_s`` to get the collection.

3. The object itself is accessed by its CamelCase name, but the usage of the object is all lowercase.

4. The characters ``.`` and ``-`` are always replaced with ``_`` in the SDK.

Because the REST API endpoints have a hierarchical structure, you need to load/create the highest-level objects before you can load lower-level ones. The example below shows how the pieces of the URI correspond to the REST endpoints/SDK classes. The first part of the URI is the IP address of your BIG-IP®.

.. include:: uri_code_breakdown.rst

.. table::

    =============   ==================================================
    OC              :ref:`Organizing Collection <oc_section>`
    Coll            :ref:`Collection <coll_section>`
    Resource        :ref:`Resource <res_section>`
    SC              :ref:`Subcollection <subcoll_section>`
    SubColl Resrc   :ref:`Subcollection Resource <subcollres_section>`
    =============   ==================================================


In the sections below, we'll walk through the Python object paths using LTM® pools and pool members as examples. You can also skip straight to the |Coding Example|.

.. _oc_section:

|Organizing Collection Section|
-------------------------------
The ``mgmt/tm`` and ``ltm`` organizing collections define what area of the BIG-IP® you're going to work with. The ``mgmt/tm`` organizing collection corresponds to the management plane of your BIG-IP® device (TMOS). Loading ``ltm`` indicates that we're going to work with the BIG-IP®'s :guilabel:`Local Traffic Manager®` module.

.. include:: endpoints/endpoint_table_tm.rst
.. include:: endpoints/endpoint_table_ltm.rst

.. topic:: Example: Connect to the BIG-IP® and load the LTM® module

    .. code-block:: python

        from f5.bigip import BigIP
        bigip = BigIP('192.168.1.1', 'myuser', 'mypass')
        ltm = bigip.ltm

        >>> print bigip
        <f5.bigip.BigIP object at 0x8a29d0>

        >>> print ltm
        <f5.bigip.ltm.LTM object at 0x8c0b30>


.. _coll_section:

|Collection Section|
--------------------

Now that the higher-level organizing collections are loaded (in other words, we signed in to the BIG-IP® and accessed the LTM® module), we can load the ``pool`` collection.

.. include:: endpoints/endpoint_table_ltm_pool.rst

.. topic:: Example: Load the pools collection

    .. code-block:: python

        from f5.bigip import BigIP

        bigip = BigIP('192.168.1.1', 'myuser', 'mypass')
        pool_collection = bigip.ltm.pools
        pools = bigip.ltm.pools.get_collection()

        for pool in pools:
             print pool.name

        my_newpool
        mypool
        pool2
        pool_1

In the above example, we instantiated the class :class:`f5.bigip.ltm.pool.Pools`, then used the :meth:`f5.bigip.ltm.pool.Pools.get_collection()` method to fetch the collection (in other words, a list of the pool :ref:`resources <res_section>` configured on the BIG-IP®).


.. _res_section:

|Resource Section|
------------------
In the SDK, we refer to a single instance of a configuration object as a resource. As shown in the previous sections, we are able to access the ``pool`` resources on the BIG-IP® after loading the ``mgmt\tm\ltm`` organizing collections and the ``pools`` collection.

.. include:: endpoints/endpoint_table_ltm_pool_pools.rst

.. topic:: Example: Load a pool resource

    .. code-block:: python

        from f5.bigip import BigIP
        pool = pools.pool.load(partition='Common', name='mypool')


In the example above, we instantiated the class :class:`f5.bigip.ltm.pool.Pool` and loaded the :obj:`f5.bigip.ltm.pools.pool` object. The object is a python representation of the BIG-IP® pool we loaded (in this case, ``Common/mypool``).

.. tip::

    You can always see the representation of an object using the :meth:`~f5.bigip.ltm.pool.Pools.raw` method.

    .. code-block:: python

        >>> pool.raw
        {
         u'generation': 123,
         u'minActiveMembers': 0,
         u'ipTosToServer': u'pass-through',
         u'loadBalancingMode': u'round-robin',
         u'allowNat': u'yes',
         u'queueDepthLimit': 0,
         u'membersReference': {
            u'isSubcollection': True,
            u'link': u'https://localhost/mgmt/tm/ltm/pool/~Common~mypool/members?ver=11.6.0'},
            u'minUpMembers': 0, u'slowRampTime': 10,
            u'minUpMembersAction': u'failover',
            '_meta_data': {
                'attribute_registry': {
                    'tm:ltm:pool:memberscollectionstate': <class 'f5.bigip.ltm
                .pool.Members_s'>
                },
                'container': <f5.bigip.ltm.pool.Pools object at 0x835ef0>,
                'uri': u'https://10.190.6.253/mgmt/tm/ltm/pool/~Common~mypool/',
                'exclusive_attributes': [],
                'read_only_attributes': [],
                'allowed_lazy_attributes': [<class 'f5.bigip.ltm.pool.Members_s'>],
                'required_refresh_parameters': set(['name']),
                'required_json_kind': 'tm:ltm:pool:poolstate',
                'bigip': <f5.bigip.BigIP object at 0x5826f0>,
                'required_creation_parameters': set(['name']),
                'creation_uri_frag': '',
                'creation_uri_qargs': {u'ver': [u'11.6.0']}
            },
            u'minUpMembersChecking': u'disabled',
            u'queueTimeLimit': 0,
            u'linkQosToServer': u'pass-through',
            u'queueOnConnectionLimit': u'disabled',
            u'fullPath': u'/Common/mypool',
            u'kind': u'tm:ltm:pool:poolstate',
            u'name': u'mypool',
            u'partition': u'Common',
            u'allowSnat': u'yes',
            u'ipTosToClient': u'pass-through',
            u'reselectTries': 0,
            u'selfLink': u'https://localhost/mgmt/tm/ltm/pool/~Common~mypool?ver=11.6.0',
            u'serviceDownAction': u'none',
            u'ignorePersistedWeight': u'disabled',
            u'linkQosToClient': u'pass-through'
           }


.. _subcoll_section:

|Subcollection Section|
-----------------------
A subcollection is a collection of resources that can only be accessed via its parent resource.

To continue our example: The :class:`f5.bigip.ltm.pool.Pool` resource object contains :class:`f5.bigip.ltm.pool.Member` :ref:`subcollection resource <subcollres_section>` objects. These subcollection resources -- the real-servers that are attached to the pool, or 'pool members' -- are part of the ``members_s`` subcollection. (Remember, we have to add ``_s`` to the end of collection object names if the name of the resource object it contains already ends in ``s``).

.. include:: endpoints/endpoint_table_ltm_pool_members_s.rst

.. topic:: Example: Load the members_s collection

    .. code-block:: python

        from f5.bigip import BigIP
        members = pool.members_s.get_collection()
        print members
        [<f5.bigip.ltm.pool.Members object at 0x9d7ff0>, <f5.bigip.ltm.pool.Members object at 0x9d7830>]


.. _subcollres_section:

|Subcollection Resource Section|
--------------------------------

As explained in the previous section, a subcollection contains subcollection resources. These subcollection resources can only be loaded after all of the parent objects (organizing collections, resource, and subcollection) have been loaded.

.. include:: endpoints/endpoint_table_ltm_pool_members.rst

.. topic:: Example: Load member objects

    .. code-block:: python

        from f5.bigip import BigIP
        member = members_s.members.load(partition='Common', name='m1')
        print member
        <f5.bigip.ltm.pool.Members object at 0x9fd530>



|Coding Example|




.. |Coding Example| replace:: :ref:`Coding Example <pools-and-members_code-example>`
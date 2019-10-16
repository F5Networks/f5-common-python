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
    Unnamed Resrc   :ref:`Unnamed Resource <unnamed_resource_section>`
    SC              :ref:`Subcollection <subcoll_section>`
    SubColl Resrc   :ref:`Subcollection Resource <subcollres_section>`
    =============   ==================================================


In the sections below, we'll walk through the Python object paths using LTM® pools and pool members as examples. You can also skip straight to the |Coding Example|.

.. _oc_section:

|Organizing Collection Section|
-------------------------------

The ``tm`` and ``ltm`` organizing collections define what area of the BIG-IP® you're going to work with. The ``tm`` organizing collection corresponds to the traffic management plane of your BIG-IP® (``tmsh``). Loading ``ltm`` indicates that we're going to work with the BIG-IP®'s :guilabel:`Local Traffic` module.

.. include:: endpoints/endpoint_table_tm.rst
.. include:: endpoints/endpoint_table_ltm.rst

.. topic:: Example: Connect to the BIG-IP® and load the ``ltm`` organizing collection

    .. code-block:: python

        from f5.bigip import ManagementRoot
        mgmt = ManagementRoot('192.168.1.1', 'myuser', 'mypass')
        ltm = mgmt.tm.ltm

        >>> print mgmt
        <f5.bigip.ManagementRoot object at 0x1044e3210>

        >>> print ltm
        <f5.bigip.tm.ltm.Ltm object at 0x104aee7d0>


.. _coll_section:

|Collection Section|
--------------------

Now that the higher-level organizing collections are loaded (in other words, we signed in to the BIG-IP® and accessed the LTM® module), we can load the ``pool`` collection.

.. include:: endpoints/endpoint_table_ltm_pool.rst

.. topic:: Example: Load the ``pools`` collection

    .. code-block:: python

        pool_collection = mgmt.tm.ltm.pools.get_collection()
        pools = mgmt.tm.ltm.pools

        for pool in pool_collection:
             print pool.name

        pool1
        pool2

In the above example, we used the :meth:`f5.bigip.tm.ltm.pool.Pools.get_collection()` method to fetch the collection (in other words, a list of the pool :ref:`resources <res_section>` configured on the BIG-IP®). Then, we instantiated the class :class:`f5.bigip.tm.ltm.pool.Pools`.


.. _res_section:

|Resource Section|
------------------

In the SDK, we refer to a single instance of a configuration object as a :dfn:`resource`. As shown in the previous sections, we are able to access the ``pool`` resources on the BIG-IP® after loading the ``/mgmt/tm/ltm/`` organizing collections and the ``pools`` collection.

.. include:: endpoints/endpoint_table_ltm_pool_pools.rst

.. topic:: Example: Load a ``pool`` resource

    .. code-block:: python

        pool = pools.pool
        pool1 = pool.load(partition='Common', name='pool1')


In the example above, we instantiated the class :class:`f5.bigip.tm.ltm.pool.Pool` and used it to load the :obj:`f5.bigip.tm.ltm.pools.pool` object. The object is a python representation of an actual BIG-IP® pool in the Common partition (or, ``Common/pool1``).

.. tip::

    You can always see the representation of an object using the :meth:`~f5.bigip.tm.ltm.pool.Pools.raw` method.

    .. code-block:: python

        >>> pool1.raw
        {
            u'generation': 208,
            u'minActiveMembers': 0,
            u'ipTosToServer': u'pass-through',
            u'loadBalancingMode': u'round-robin',
            u'allowNat': u'yes',
            u'queueDepthLimit': 0,
            u'membersReference': {
                u'isSubcollection': True,
                u'link': u'https://localhost/mgmt/tm/ltm/pool/~Common~pool1/members?ver=11.6.0'},
            u'minUpMembers': 0,
            u'slowRampTime': 10,
            u'minUpMembersAction': u'failover',
            '_meta_data': {
                'attribute_registry': {
                    'tm:ltm:pool:memberscollectionstate': <class 'f5.bigip.tm.ltm.pool.Members_s'>
                    },
                'container': <f5.bigip.tm.ltm.pool.Pools object at 0x102e6c550>,
                'exclusive_attributes': [],
                'read_only_attributes': [],
                'allowed_lazy_attributes': [<class 'f5.bigip.tm.ltm.pool.Members_s'>],
                'uri': u'https://10.190.7.161:443/mgmt/tm/ltm/pool/~Common~pool1/',
                'required_json_kind': 'tm:ltm:pool:poolstate',
                'bigip': <f5.bigip.ManagementRoot object at 0x1006e4bd0>,
                'icontrol_version': '',
                'icr_session': <icontrol.session.iControlRESTSession object at 0x1006e4c90>,
                'required_load_parameters': set(['name']),
                'required_creation_parameters': set(['name']),
                'creation_uri_frag': '',
                'creation_uri_qargs': {
                    u'ver': [u'11.6.0']
                }
            },
            u'minUpMembersChecking': u'disabled',
            u'queueTimeLimit': 0,
            u'linkQosToServer': u'pass-through',
            u'description': u'This is my pool',
            u'queueOnConnectionLimit': u'disabled',
            u'fullPath': u'/Common/pool1',
            u'kind': u'tm:ltm:pool:poolstate',
            u'name': u'pool1',
            u'partition': u'Common',
            u'allowSnat': u'yes',
            u'ipTosToClient': u'pass-through',
            u'reselectTries': 0,
            u'selfLink': u'https://localhost/mgmt/tm/ltm/pool/~Common~pool1?ver=11.6.0',
            u'serviceDownAction': u'none',
            u'ignorePersistedWeight': u'disabled',
            u'linkQosToClient': u'pass-through'
        }


.. _unnamed_resource_section:

|Unnamed Resource Section|
--------------------------

In the SDK, we refer to a single instance of a configuration object with no name field as an :dfn:`unnamed resource`. Unnamed resources cannot be created or deleted, but they can be loaded, updated, etc.

.. topic:: Example: Load the ``httpd`` unnamed resource settings

    .. code-block:: python

        >>> httpd = b.tm.sys.httpd.load()
        >>> httpd.maxClients = 5
        >>> httpd.update()

In the example above, we instantiated the class :class:`f5.bigip.tm.sys.httpd` and used it to update the max clients to 5.

.. _subcoll_section:

|Subcollection Section|
-----------------------
A subcollection is a collection of resources that can only be accessed via its parent resource. To continue our example:

The :class:`f5.bigip.tm.ltm.pool.Pool` resource object contains :class:`f5.bigip.tm.ltm.pool.Members` :ref:`subcollection resource <subcollres_section>` objects. These subcollection resources -- the real-servers that are attached to the pool, or 'pool members' -- are part of the ``members_s`` subcollection in the SDK. (Remember, we have to add ``_s`` to the end of collection object names if the name of the resource object it contains already ends in ``s``).

.. include:: endpoints/endpoint_table_ltm_pool_members_s.rst

.. topic:: Example: Load the ``members_s`` collection to view a list of ``members``

    .. code-block:: python

        members_collection = pool.members_s.get_collection()
        members = pool.members_s

        print members_collection
        [<f5.bigip.tm.ltm.pool.Members object at 0x9d7ff0>, <f5.bigip.tm.ltm.pool.Members object at 0x9d7830>]


.. _subcollres_section:

|Subcollection Resource Section|
--------------------------------

As explained in the previous section, a subcollection contains subcollection resources. These subcollection resources can only be loaded after all of the parent objects (organizing collections, resource, and subcollection) have been loaded.

.. include:: endpoints/endpoint_table_ltm_pool_members.rst

.. topic:: Example: Load ``members`` objects

    .. code-block:: python

        members = pool.members_s
        member = pool.members_s.members
        print member
        <f5.bigip.tm.ltm.pool.Members object at 0x9fd530>


|Coding Example|




.. |Coding Example| replace:: :ref:`Coding Example <pools-and-members_code-example>`

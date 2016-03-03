Python Object Paths
===================

The object classes used in the SDK directly correspond to the REST endpoints you'd use to access the objects via the API. Remembering the patterns below will help you easily derive an SDK object class from an object URI.

1. Objects take the form ``f5.<product>.<organizing_collection>.<collection>.<resource>.<subcollection>.<resource>``.

2. The collection and the resource generally have the same name, so the collection is the *plural* version of the resource. This means that you add ``s`` to the end of the resource to get the collection, *unless* the resource already ends in ``s``. If the resource is already plural, add ``_s`` to get the collection.

3. The object itself is accessed by its CamelCase name, but the usage of the object is all lowercase.

4. The characters ``.`` and ``-`` are always replaced with ``_`` in the SDK.

Because the REST API endpoints have a hierarchical structure, you need to load/create the highest-level objects before you can load lower-level ones. The example below shows how the pieces of the URI correspond to the REST endpoints/SDK classes. The first part of the URI is the IP address of your BIG-IP device.

.. include:: uri_code_breakdown.rst

.. table::

    =============   ==================================================
    OC              :ref:`Organizing Collection <oc_section>`
    Coll            :ref:`Collection <coll_section>`
    Resource        :ref:`Resource <res_section>`
    SC              :ref:`Subcollection <subcoll_section>`
    SubColl Resrc   :ref:`Subcollection Resource <subcollres_section>`
    =============   ==================================================


In the sections below, we'll walk through the Python object paths using LTM pools and pool members as examples.

.. _oc_section:

|Organizing Collection Section|
-------------------------------
The ``mgmt\tm` and ``ltm`` organizing collections define what area of the BIG-IP you're going to work with. The ``mgmt\tm`` organizing collection corresponds to the management plane of your BIG-IP device (TMOS). Loading ``ltm`` indicates that we're going to work with the BIG-IP's :guilabel:`Local Traffic` module.

.. include:: endpoints/endpoint_table_tm.rst
.. include:: endpoints/endpoint_table_ltm.rst

.. topic:: Example: Connect to the BIG-IP

    .. code-block:: python

        from f5.bigip import BigIP
        bigip = BigIP('192.168.1.1', 'myuser', 'mypass')

        >>> print bigip
        <f5.bigip.BigIP object at 0x8a29d0>

.. _coll_section:

|Collection Section|
--------------------

Now that the higher-level organizing collections are loaded (in other words, we're signed in to the BIG-IP), we can load the ``pool`` collection.

.. include:: endpoints/endpoint_table_ltm_pool.rst

.. topic:: Example: Load the pool collection

    .. code-block:: python

        from f5.bigip import BigIP

        bigip = BigIP('192.168.1.1', 'myuser', 'mypass')
        pool_collection = bigip.ltm.pools
        pools = bigip.ltm.pools.get_collection()

        print pools
        [<f5.bigip.ltm.pool.Pool object at 0x8c0f50>, <f5.bigip.ltm.pool.Pool object at 0x8c0b70>, <f5.bigip.ltm.pool.Pool object at 0x8c0e30>]


In the above example, we instantiated the class :class:`f5.bigip.ltm.pool.Pools`, then used the :meth:`f5.bigip.ltm.pool.Pools.get_collection()` method to fetch the collection (in other words, a list of the pool :ref:`resources <res_section>` configured on the BIG-IP).


.. _res_section:

|Resource Section|
------------------
In the SDK, we refer to a single instance of a configuration object as a :ref:`resource <endpoints/_resource_section>`. As shown in the previous sections, we are able to access the ``pool`` resources on the BIG-IP after loading the ``mgmt\tm\ltm`` organizing collections and the ``pools`` collection.

.. include:: endpoints/endpoint_table_ltm_pool_pools.rst

.. topic:: Example: Load the pool collection

    .. code-block:: python

        from f5.bigip import BigIP

        bigip = BigIP('192.168.1.1', 'myuser', 'mypass')
        pool_collection = bigip.ltm.pools
        pools = bigip.ltm.pools.get_collection()

        print pools
        [<f5.bigip.ltm.pool.Pool object at 0x8c0f50>, <f5.bigip.ltm.pool.Pool object at 0x8c0b70>, <f5.bigip.ltm.pool.Pool object at 0x8c0e30>]





Just like the :class:`~f5.bigip.ltm.pool.Pools` class above, :class:`~f5.bigip.ltm.pool.Pool` is a python class that has methods that allow it to create, manage, and delete pool objects on the BIG-IP. The :obj:`f5.bigip.ltm.pools.pool` instance is a representation of the BIG-IP pool whose attributes are derived from the JSON blob that is returned when
the object is created, loaded, updated, or refreshed.  You can always see the representation of an object by using the :meth:`~f5.bigip.ltm.pool.Pool.raw` method.

**Code Example**

.. code-block:: python

    from f5.bigip import BigIP

    # Connect to the BigIP
    bigip = BigIP('192.168.1.1', 'admin', 'admin')

    # Get a pool object and load it
    pool_obj = bigip.ltm.pools.pool
    pool_1 = pool_obj.load(partition='Common', name='mypool')

        # We can also skip the object and just load it directly
    pool_2 = bigip.ltm.pools.pool.load(partition='Common', name='mypool')

    # Print the object
    print pool_1.raw

    # Make sure 1 and 2 have the same names and generation
    assert pool_1.name == pool_2.name
    assert pool_1.generation == pool_2.generation

    # Update the description
    pool_1.description = "This is my pool"
    pool_1.update()

    # Since we haven't refreshed pool_2 is shouldn't match pool_1 andy more
    assert pool_1.generation > pool_2.generation

    # Refresh pool 2 and check that is now equal
    pool_2.refresh()
    assert pool_1.generation == pool_2.generation

    # We are done with this pool so remove it from bigip
    pool_1.delete()

    # Make sure it is gone
    assert not bigip.ltm.pools.pool.exists(partition='Common', name='mypool')

.. _subcoll_section:

Subcollections
--------------
A subcollection is a collection of resources that can only be accessed via a
parent resource.  For example :class:`~f5.bigip.ltm.pool.Pool` objects have
:class:`~f5.bigip.ltm.pool.Member` objects which are the real-servers attached
to the pool.  All of the pool's members are stored in a sub-collection that
follows the same rule as Collections of Objects above (the collection is the
pluralized version of the object they contain).

Pool Members Subcollection Example (a.k.a pools.pool.members_s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
URI Path
    ``https://192.168.1.1/mgmt/tm/ltm/pool/~Common~mypool/members``
GUI Path
    ``Local Traffic --> Pools --> mypool --> Members Tab``
Python SDK class
    :class:`f5.bigip.ltm.pool.Members_s`
Pool Instance
    :obj:`f5.bigip.ltm.pools.pool.members_s`
JSON Kind
    ``tm:ltm:pool:members:memberscollectionstate``

There is no difference in this subcollection than the collection of pools above
except that you can only access it via the pool object that the subcollection
is attached to.  Since this is really just a plain old
:class:`~f5.bigip.resource.Collection` it has the same methods available
to it.

**Code Example**

.. code-block:: python

    from f5.bigip import BigIP

    # Connect to the BigIP
    bigip = BigIP('192.168.1.1', 'admin', 'admin')

    # Get our pool
    pool = bigip.ltm.pools.pool.load(partition='Common', name='mypool')

    # Get all of the pool members for the pool and print their name
    members = pool.members_s.get_collection()
    for member in members:
        print member.name


.. _subcollres_section:

Subcollection Resources
-----------------------
Just like a subcollection really is no different than a collection the same
can be said for a subcollection resource and a resource. They have the same
behavior and methods, the only difference is that you must access them
through a subcollection that is attached to a resource.  A single member of
an LTM pool is a great example of this.

Pool Members Subcollection Resource Example (a.k.a pools.pool.members_s.member)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
URI Path
    ``https://192.168.1.1/mgmt/tm/ltm/pool/~Common~mypool/members/~Common~m1``
GUI Path
    ``Local Traffic --> Pools --> mypool --> Members Tab --> m1``
Python SDK class
    :class:`f5.bigip.ltm.pool.Members_s.member`
Pool Instance
    :obj:`f5.bigip.ltm.pools.pool.members_s.member`
JSON Kind
    ``tm:ltm:pool:members:membersstate``

**Code Example**

.. code-block:: python

    from f5.bigip import BigIP

    # Connect to the BigIP
    bigip = BigIP('192.168.1.1', 'admin', 'admin')

    # Load our pool and member m1
    pool = bigip.ltm.pools.pool.load(partition='Common', name='mypool')
    m1 = pool.members_s.member.load(partition='Common', name='m1')

    # Create a new pool member
    m2 = pool.members_s.member.create(partition='Common', name='m1')

    # Delete our old member
    m1.delete()

    # Make sure it is gone
    assert pool.members_s.member.exists(partition='Common', name='m1')


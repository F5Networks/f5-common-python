Python Object Paths
===================
The way that you access a BigIP rest endpoint in the SDK can be derived from the
URI that is used to access it via the API.  For the the following discussion
lets assume that you are working with LTM pools and their members.  The following
URI's would be used to access the various objects and would be mapped to the
associated python instances.

There are a few patterns you should remember when using this SDK to help
you derive access to the objects.

  1. The objects take the form
     ``f5.<product>.<organizing_collection>.<collection>.<resource>.<subcollection>.<resource>``.
  2. The collection and the resource generally have the same name so the
     collection is the *plural* version of the resource.  This means that you
     add ``s`` to the end of the resource unless the resource ends in a ``s``.
     In that case you add ``_s``.
  3. The object itself is accessed by its CamelCase name, while the usage of
     that object is all lowercase.
  4. Any ``.`` or ``-`` are replaced with ``_``.

Collections
-----------
A BigIP can have multiple LTM pool objects configured on it.  The REST API can
give you this list by querying the pool collection.  This is what the SDK refers
to as a :ref:`collection <_collection_section>` of pool objects and the REST API
returns you JSON with an ``items`` attribute that contains a list of references
to the pools that are configured on the BigIP.

Pool Collection Example (a.k.a pools)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
URI Path
    ``https://192.168.1.1/mgmt/tm/ltm/pool/``
GUI Path
    ``Local Traffic --> Pools``
Python SDK class
    :class:`f5.bigip.ltm.pool.Pools`
Pool Instance
    :obj:`f5.bigip.ltm.pools`
JSON Kind
    ``tm:ltm:pool:poolcollectionstate``

The :class:`~f5.bigip.ltm.pool.Pools` class is exactly that, a Python class that
has methods that make it useful once it is instantiated like
:meth:`~f5.bigip.ltm.pool.Pools.get_collection()` which returns a list of pool
:ref:`resources <_resources_section>` currently configured on the BigIP.

**Code Example**

.. code-block:: python

   from f5.bigip import BigIP

   bigip = BigIP('192.168.1.1', 'admin', 'admin')
   pool_collection = bigip.ltm.pools
   pools = pool_collection.get_collection()


Resources
---------
A single instance of a configuration object is referred to by the SDK as a
:ref:`resource <endpoints/_resource_section>`.  Resources are contained in collections
and are accessed through that collection. Resources accept configuration and
support the following F5 SDK CURDLE methods unless
otherwise specified in the :doc:`documentation <../apidoc/f5>` for their class:

* :meth:`~f5.bigip.resource.Resource.create`
* :meth:`~f5.bigip.resource.Resource.update`
* :meth:`~f5.bigip.resource.Resource.refresh`
* :meth:`~f5.bigip.resource.Resource.delete`
* :meth:`~f5.bigip.resource.Resource.load`
* :meth:`~f5.bigip.resource.Resource.exists`

Pool Resource Example (a.k.a pools.pool)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
URI Path
    ``https://192.168.1.1/mgmt/tm/ltm/pool/~Common~mypool``
GUI Path
    ``Local Traffic --> Pools --> mypool``
Python SDK class
    :class:`f5.bigip.ltm.pool.Pool`
Pool Instance
    :obj:`f5.bigip.ltm.pools.pool`
JSON Kind
    ``tm:ltm:pool:poolstate``

Just like the :class:`~f5.bigip.ltm.pool.Pools` class above
:class:`~f5.bigip.ltm.pool.Pool` is a python class that has methods that allow
it to create, manage, and delete pool objects on the BigIP.  The
:obj:`f5.bigip.ltm.pools.pool` instance is a representation of the BigIP
pool who's attributes are derived from the JSON blob that is returned when
the object is created, loaded, updated, or refreshed.  You can always see
the representation of an object by using the :meth:`~f5.bigip.ltm.pool.Pool.raw`
method.

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

Sub-Collections
---------------
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

Sub-Collection Resources
------------------------
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


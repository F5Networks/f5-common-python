REST API Endpoints
==================

REST URI Segments
-----------------
To start the exploring the REST API's endpoints we can look at the example
below which details the how the :ref:`endpoint types <endpoint_section>` map to
the different parts of the URI.  The example is the URI that returns the JSON
for a LTM pool member and shows all of the different types of resources the SDK
uses.

.. code::

    http://192.168.1.1/mgmt/tm/ltm/pool/~Common~mypool/members/~Common~m1:80
                      |-------|---|----|--------------|-------|-------------|
                         OC     OC  CR      Resource     SC    Sub-Resrc Obj

**OC** -- :ref:`Organizing Collection <organizing_collection_section>`

**CR** -- :ref:`Collection Resource <collection_section>`

**Resource** -- :ref:`Resource <resource_section>`

**SC** -- :ref:`Subcollection <subcollection_resource_section>`

**Sub-Resrc Obj** -- :ref:`Sub-Resource Object <subcollection_resource_section>`

iControl REST ``kind`` Parameters
---------------------------------
Almost all REST API entries return JSON that has a parameter in it named
``kind`` which tells the user what to expect after it.  There are three types
of kinds: ``collectionstate``, ``state``, ``stats`` that are discussed below.

``collectionstate``
~~~~~~~~~~~~~~~~~~~
When an endpoint has a ``kind`` that ends in ``<object>collectionstate`` we
call this a |Collection| and it means that there is generally no configuration
associated with the object and it contains references to additional
|Collection| or |Resource| objects.

``state``
~~~~~~~~~
When an endpoint has a kind that ends in ``<object>state`` we call that a
|Resource| and it means that you can apply configuration directly to
that object.  It also means that in general our CURDLE (:meth:`Create`,
:meth:`Update`, :meth:`Refresh`, :meth:`Delete`, :meth:`Load`, :meth:`Exists`)
methods can be applied to it.


A ``state`` kind may also contain a :ref:`subcollection <subcollection_section>`
is also not a collection of things so it may contain a reference to a list of
resources in an ``items``.

``stats``
~~~~~~~~~
An endpoint with a kind that ends is ``<object>stats`` it contains data about
something on the BigIP.  These are very basic objects and only provide
read-like operations (:meth:`~f5.bigip.resource.Resource.load`,
:meth:`~f5.bigip.resource.Resource.refresh`).


.. _endpoint_section:

Endpoint Types
--------------

.. _organizing_collection_section:

Organizing Collection
~~~~~~~~~~~~~~~~~~~~~
Organizing collections are the first object under the :mod:`f5.bigip` module.
Organizing collections can be thought of as the different modules that are
available on the BigIP. The `iControl REST User Guide <https://devcentral.f5.com/d/the-user-guide-for-the-icontrol-rest-interface-in-big-ip-version-1160?download=true>`_
refers an *organizing collection* as a URI that designates all of the ``tmsh``
subordinate modules and components in the specified module.

While the names may not directly map to the GUI, users who are familiar with the
BigIP's GUI will recognize these as the drawers on the left side.  Many of the
names are abbreviated in the REST API, but the mapping is pretty straight
forward.  For example the SDK module :mod:`f5.bigip.sys` maps to the System
drawer in the GUI.

|OrganizingCollection| objects do not have configuration parameters.  They
contain a list of references to |Collection| and |Resource| objects in the
``items`` parameter of the JSON blob that is return from an ``HTTP GET`` to its
URI. Their ``kind`` ends in the string ``collectionstate``.

Here is an example of the JSON you will get when from an `organizing
collection`:

.. code-block:: json

    {
        "kind":"tm:ltm:ltmcollectionstate",
        "selfLink":"https://localhost/mgmt/tm/ltm?ver=11.5.0",
        "items":[
            {
            "reference":{
            "link":"https://../mgmt/tm/ltm/auth?ver=11.5.0"
            }
            },
            {
            "reference":{
            "link":"https://../mgmt/tm/ltm/classification?ver=11.5.0"
            }
            },
            ...
        ]
    }


.. _collection_section:

Collection
~~~~~~~~~~
A collection is similar to an |Organizing Collection Section| in that it does not
have configuration that can bee applied to it.  The difference between the two
is that a collection contains references to a list of the same object types
in its ``items`` parameter.  Since these these objects do not have configuration
they do not support the traditional CRUD methods for REST APIs.  Instead they
have methods to get the list of objects they contain.  For example the
:meth:`~f5.bigip.resource.Collection.get_collection` which returns a list of the
objects in the collection.

When using the SDK you will notice that these collection objects are
referenced by using the plural version of the |Resource| objects they contain.
The one exception is when the |Resource| object's type ends in a ``s`` in
which case you refer to them by adding ``_s`` to the name.  This ``_`` rule
applies to all object collections if the object in the collection ends in
``s``.

**Examples**

* LTM Pool objects are collected in :mod:`f5.bigip.ltm.pool.Pools` and are
  accessed by the user with the path :meth:`f5.bigip.pools.get_collection`.

* Network Tunnels objects are stored in :class:`f5.bip.net.tunnels.Tunnels_s`
  and are accessed by the user with the path
  :meth:`f5.bigip.net.tunnels_s.get_collection`.

Just like an |Organizing Collection Section| a collection object's ``kind`` ends in
``collectionstate``.

Here is an example of the JSON you would get back from a collection endpoint.
Notice that it has a kind that ends in ``collectionstate`` and an ``items``
attribute that is a list of :class:`~f5.bigip.ltm.node.Node` objects (we
know this because their ``kind`` ends in ``node:nodestate``).

.. code-block:: json

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
    }



.. _resource_section:

Resource
~~~~~~~~
A resource is a REST API endpoint that can contains configuration.  These
endpoints support the traditional CRUD methods for REST API's as well as a
few extra that we have added for our users.  For most resources you can
assume that they will support the following methods.

* :meth:`~f5.bigip.resource.Resource.create`
* :meth:`~f5.bigip.resource.Resource.refresh`
* :meth:`~f5.bigip.resource.Resource.update`
* :meth:`~f5.bigip.resource.Resource.delete`
* :meth:`~f5.bigip.resource.Resource.load`
* :meth:`~f5.bigip.resource.Resource.exists`

When using the SDK you will notice that these classes are instantiated via
their :ref:`collection <collection_section>` and once created or loaded
will contain attributes that map the the json fields returned by the BigIP.

Below is an example of a :class:`f5.bigip.ltm.node.Node` object that was loaded
with the following code.

   >>> from f5.bigip import BigIP
   >>> bigip = BigIP('192.168.1.1', 'myuser', 'mypass')
   >>> n = bigip.ltm.nodes.node.load(partition='Common', name='192.168.15.15')
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

With the output of the :attr:`f5.bigip.ltm.node.Node.raw` we can see all of
the attributes we have available to us.  For example after loading the object
you can access them by doing the following.

    >>> n.fqdn['downInterval'] = 10
    >>> n.logging = 'enabled'
    >>> n.update()

.. _subcollection_section:

Subcollection
~~~~~~~~~~~~~
Subcollections are collections of resources that are attached to another
resource object.  They exactly the same as
:ref:`collections <collection_section>` except that they must be accessed
via the resource that they are attached to.  An example of a subcollection are
pool members that are attached to a pool.  In order to access them you
have to know what pool you are dealing with and there for you need to
create or load the pool object first and then access the members from there.

A resource will have a refernce to its subcollection indicating it is a
subcollection and that reference will have a list of resources in its ``items``
attribute.

Just like a collection there is no configuration associated so the methods
are limited to just getting the collection of objects.

   >>> from f5.bigip import BigIP
   >>> bigip = BigIP('192.168.1.1', 'myuser', 'mypass')
   >>> pool = bigip.ltm.pools.pool.load(partition='Common', name='p1')
   >>> members = pool.members_s.get_collection()

.. note::

    In the example above the URI and ``kind`` for the member objects associated
    with a pool is ``members`` so the collection name ends in ``_s``

Here is the JSON from a pool with one member. Notice the highlighted rows
indicating the subcollection.

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

.. _subcollection_resource_section:

Subcollection Resource
~~~~~~~~~~~~~~~~~~~~~~
Similar to a subcollection a subresource is the same as a
:ref:`resource <resource_section>` with the only difference being that you
access it via the subcollection attached to the main resource.  Continuing
with the example above the actual pool member instance associated with a pool
via the ``members_s`` subcollection is the subcollection resource.

   >>> from f5.bigip import BigIP
   >>> bigip = BigIP('192.168.1.1', 'myuser', 'mypass')
   >>> pool = bigip.ltm.pools.pool.load(partition='Common', name='p1')
   >>> member = pool.members_s.member.load(partition='Common', name='n1:80')


The JSON below shows a :obj:`f5.bigip.ltm.pools.pool.members` object.

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

.. note::

    This is a Resource object because the kind is not a ``collectionstate``.

.. |Collection Section| replace:: :ref:`collection <collection_section>`

.. |Organizing Collection Section| replace:: :ref:`orgianizing collection <organizing_collection_section>`

.. |OrganizingCollection| replace:: :class:`~f5.bigip.resource.OrganizingCollection`

.. |Collection| replace:: :class:`~f5.bigip.resource.Collection`

.. |Resource| replace:: :class:`~f5.bigip.resource.Resource`

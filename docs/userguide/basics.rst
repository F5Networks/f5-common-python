Basic Concepts
==============

Familiarizing yourself with the following underlying basic concepts will help you get up and running with the SDK.

.. include:: SDK_plural_note.rst

REST URIs
---------

You can directly infer REST URIs from the python expressions, and vice versa.

.. topic:: Examples

    .. code-block:: text

        Expression:     bigip = BigIP('a', 'b', 'c')
        URI Returned:   https://a/mgmt/tm/



    .. code-block:: text

        Expression:     bigip.ltm
        URI Returned:   https://a/mgmt/tm/ltm/


    .. code-block:: text

        Expression:     pools1 = bigip.ltm.pools
        URI Returned:   https://a/mgmt/tm/ltm/pool


    .. code-block:: text

        Expression:     pool_a = pools1.create(partition="Common", name="foo")
        URI Returned:   https://a/mgmt/tm/ltm/pool/~Common~foo


REST Endpoints
--------------
A set of basic REST endpoints can be derived from the object's URI and ``kind`` (listed below).

  - |Organizing Collection Section|
  - |Collection Section|
  - |Resource Section|
  - |Subcollection Section|
  - |Subcollection Resource Section|


Dynamic Attributes
------------------

The python object's attribute can be created dynamically based on the JSON returned when querying the REST API.

.. _kind_params_section:

iControl REST ``kind`` Parameters
---------------------------------
Almost all iControl REST API entries contain a parameter named ``kind``. This parameter provides information about the object that lets you know what you should expect to follow it. The iControl REST API uses three types of ``kind``: ``collectionstate``, ``state``, and ``stats``.

.. table::

    +---------------------+--------------------------+-------------------------------------------------+
    | ``kind``            | Associated Objects       | Methods                                         |
    +=====================+==========================+=================================================+
    | ``collectionstate`` | |Organizing Collection|, | |exists|                                        |
    |                     | |Collection|             |                                                 |
    +---------------------+--------------------------+-------------------------------------------------+
    | ``state``           | |Resource|               | |create|, |update|, |refresh|, |delete|,        |
    |                     |                          | |load|, |exists|                                |
    +---------------------+--------------------------+-------------------------------------------------+
    | ``stats``           | |Resource|               | |refresh|, |load|, |exists|                     |
    +---------------------+--------------------------+-------------------------------------------------+


.. methods_section:

Methods
-------

+-----------+---------------+-------------------------------------------------------------------+
| Method    | HTTP Command  | Action(s)                                                         |
+===========+===============+===================================================================+
| |create|  | POST          | | creates a new resource on the device with its own URI           |
+-----------+---------------+-------------------------------------------------------------------+
| |update|  | PUT           | | submits a new configuration to the device resource; sets the    |
|           |               | | Resource attributes to the state reported by the device         |
+-----------+---------------+-------------------------------------------------------------------+
| |refresh| | GET           | | obtains the state of a device resource; sets the representing   |
|           |               | | Python Resource Object; tracks device state via its attributes  |
+-----------+---------------+-------------------------------------------------------------------+
| |delete|  | DELETE        | | removes the resource from the device, sets ``self.__dict__``    |
|           |               | | to ``{'deleted': True}``                                        |
+-----------+---------------+-------------------------------------------------------------------+
| |load|    | GET           | | obtains the state of an existing resource on the device; sets   |
|           |               | | the Resource attributes to match that state                     |
+-----------+---------------+-------------------------------------------------------------------+
| |exists|  | GET           | | checks for the existence of a named object on the BIG-IP        |
+-----------+---------------+-------------------------------------------------------------------+

.. note::

    Available methods are restricted according to the object's ``kind``.





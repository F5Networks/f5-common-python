REST API Endpoints
==================

Overview
--------

REST URI Segments
~~~~~~~~~~~~~~~~~

We'll start exploring the iControl® REST API's endpoints with an example detailing how the :ref:`endpoint types <endpoint_section>` map to the different parts of the URI. The different types of resources used by the SDK shown in the example are explained in detail later in this guide.

**Example:** The URI below returns the JSON for an LTM pool member.

.. include:: uri_code_breakdown.rst

.. table::

    =============   ==================================================
    OC              |Organizing Collection Section|
    Coll            |Collection Section|
    Resource        |Resource Section|
    SC              |Subcollection Section|
    SubColl Resrc   |Subcollection Resource Section|
    =============   ==================================================


.. _endpoint_section:

Endpoints
---------

.. toctree::

    endpoints/organizing_collection
    endpoints/collection
    endpoints/resource
    endpoints/subcollection
    endpoints/subcollection_resource



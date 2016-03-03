REST API Endpoints
==================

Overview
--------

REST URI Segments
~~~~~~~~~~~~~~~~~

We'll start exploring the iControl REST API's endpoints with an example detailing how the :ref:`endpoint types <endpoint_section>` map to the different parts of the URI. The different types of resources used by the SDK shown in the example are explained in detail later in this guide.

**Example:** The URI below returns the JSON for an LTM pool member.

.. include:: uri_code_breakdown.rst

- **OC**:             :ref:`Organizing Collection <organizing_collection_section>`
- **Coll**:           :ref:`Collection <collection_section>`
- **Resource**:       :ref:`Resource <resource_section>`
- **SC**:             :ref:`Subcollection <subcollection_section>`
- **SubColl Resrc**:  :ref:`Subcollection Resource <subcollection_resource_section>`


.. _endpoint_section:

Endpoints
---------

.. toctree::

    endpoints/organizing_collection
    endpoints/collection
    endpoints/resource
    endpoints/subcollection
    endpoints/subcollection_resource



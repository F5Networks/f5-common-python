.. important::

    When using the SDK, you'll notice that :ref:`collection <collection_section>` objects are referenced using the plural version of the |Resource| objects they contain. When the |Resource| object's type is plural (ends in an ``s``), you need to add ``_s`` to the name when referring to the object.

    This ``_s`` rule applies to all object collections where the object in the collection already ends in ``s``.

    **Examples:**

    * LTM Pool objects are collected in :mod:`f5.bigip.ltm.pool.Pools` and are accessible via the path :meth:`f5.bigip.pools.get_collection`.

    * Network Tunnels objects are stored in :class:`f5.bip.net.tunnels.Tunnels_s` and are accessible via :meth:`f5.bigip.net.tunnels_s.get_collection`.



.. important::

   In the SDK, :ref:`collection <collection_section>` objects are usually plural,
   while |Resource| objects are singular.

   When the |Resource| object's corresponding URI is already plural, we append the name
   of the :ref:`collection <collection_section>` with ``_s``.

   **Example:**

   .. table::

      +---------------------------------+---------------------------+---------------------------------+
      | URI                             | Collection                | Resource                        |
      +=================================+===========================+=================================+
      | ``/mgmt/tm/net/tunnels/``       | tm.net.tunnels            | tm.net.tunnels.tunnel           |
      +---------------------------------+---------------------------+---------------------------------+
      | ``/mgmt/tm/ltm/pool``           | tm.ltm.pools              | tm.ltm.pools.pool               |
      +---------------------------------+---------------------------+---------------------------------+
      | ``/mgmt/tm/ltm/pool/members``   | tm.ltm.pool.members_s     | tm.ltm.pool.members_s.members   |
      +---------------------------------+---------------------------+---------------------------------+

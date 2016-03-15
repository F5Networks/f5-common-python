.. _organizing_collection_section:

Organizing Collection
~~~~~~~~~~~~~~~~~~~~~

``kind``: ``collectionstate``

The `iControl REST User Guide <https://devcentral.f5.com/d/the-user-guide-for-the-icontrol-rest-interface-in-big-ip-version-1160>`_ defines an *organizing collection* as a URI that designates all of the ``tmsh`` subordinate modules and components in the specified module. Organizing collections, which appear directly under :mod:`f5.bigip`, correspond to the various modules available on the BIG-IP (for example, :mod:`f5.bigip.ltm`).

The organizing collection names correspond to the items that appear in the drawers on the left-hand side of the BIG-IP configuration utility (the GUI). The module names are abbreviated in the REST API, but the mapping is otherwise pretty straightforward. For example, the SDK module :mod:`f5.bigip.sys` maps to the System drawer in the GUI.

|Organizing Collection| objects do not have configuration parameters. As shown in the example below, the JSON blob received in response to an ``HTTP GET`` for an organizing collection object contains an ``items`` parameter with a list of references to |Collection| and |Resource| objects.

.. topic:: Example

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
            ]
        }



.. _organizing_collection_section:

Organizing Collection
~~~~~~~~~~~~~~~~~~~~~

``kind``: ``collectionstate``

In iControl® REST, the URI represents the tree structure of modules and components in the BIG-IP®. The root is represented by ``mgmt``; the REST API representation of the BIG-IP® module follows.

.. topic:: Example:

    The URI structure for the Traffic Management shell (:dfn:`tmsh`) is ``/mgmt/tm/``.

The REST representations of BIG-IP® modules which contain submodules are called :dfn:`organizing collections`. In the above example, ``/tm/`` is an organizing collection. Its submodules -- 'Statistics', 'iApps', 'DNS', 'Local Traffic', etc. -- are all organizing collections as well.

The F5® SDK follows the same mapping model as the REST API. Organizing collections, which appear under :mod:`f5.bigip`, correspond to the various modules available on the BIG-IP®.

.. topic:: Example:

    * :class:`f5.bigip.tm` maps to ``tmsh``
    * :class:`f5.bigip.tm.sys` maps to 'System'
    * :class:`f5.bigip.tm.ltm` module maps to 'Local Traffic'

|Organizing Collection| objects are not configurable; rather, they contain other submodules which either contain configurable objects (|Collection|) or are configurable objects (|Resource|).

.. topic:: Example:

    ``https://192.168.25.42/mgmt/tm/ltm/`` refers to the BIG-IP® Local Traffic module (organizing collection)
    ``https://192.168.25.42/mgmt/tm/ltm/pool`` refers to the Local Traffic Pools submodule (collection)
    ``https://192.168.25.42/mgmt/tm/ltm/pool/~Common~pool2`` refers to a specific pool (resource)


.. topic:: Example: Perform an ``HTTP GET`` for the ``ltm`` organizing collection object; the JSON blob returned contains a list of references to subordinate objects that are either collections or resources.

    .. code-block:: js

        {
            kind: "tm:ltm:ltmcollectionstate",
            selfLink: "https://localhost/mgmt/tm/ltm?ver=11.6.0",
            items: [
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/auth?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/data-group?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/dns?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/global-settings?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/html-rule?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/message-routing?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/monitor?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/persistence?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/profile?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/default-node-monitor?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/eviction-policy?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/ifile?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/nat?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/node?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/policy?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/policy-strategy?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/pool?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/rule?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/snat?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/snat-translation?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/snatpool?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/traffic-class?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/virtual?ver=11.6.0"
                    }
                },
                {
                    reference: {
                        link: "https://localhost/mgmt/tm/ltm/virtual-address?ver=11.6.0"
                    }
                }
            ]
        }


.. seealso::

    * `F5® iControl® REST User Guide v11.6.0 <https://devcentral.f5.com/d/the-user-guide-for-the-icontrol-rest-interface-in-big-ip-version-1160>`_

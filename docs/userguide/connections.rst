Connections
===========

Connecting to BIG-IP with the SDK is done via :class:`f5.bigip.ManagementRoot`.

.. code-block:: python

    >>> from f5.bigip import ManagementRoot
    >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass')

The required parameters are host, username, and password, respectively.

You can, however, supply one or more of the following kwargs (defaults listed):

.. table::

    ================ =====
    timeout          30
    port             443
    icontrol_version ''
    token            False
    verify           False
    auth_provider    None
    ================ =====

.. topic:: Example: Use token authentication on the nonstandard 4443 tcp port

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1.', 'user', 'pass', port=4443, token=True)

.. topic:: Example: Enable cert verification

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass', verify=True)



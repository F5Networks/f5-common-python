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
    token_to_use     None
    verify           False
    auth_provider    None
    ================ =====

.. topic:: Example: Use token authentication on the nonstandard 4443 tcp port

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1.', 'user', 'pass', port=4443, token=True)

.. topic:: Example: Use existing authentication token

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass', token=True, token_to_use='424CC392BC96AC52A19D32DF65BB1BC80F0EC63F629471C3AFA8A055C52F391B2DC124E17A5E8D8C7F3E91E1D1909629B6BF124747DEF879A1F028129E5486F4'

.. topic:: Example: Enable cert verification

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass', verify=True)



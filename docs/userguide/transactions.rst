Transactions
============

For operations that need multiple successful steps to be considered complete, you can run a transaction. The TransactionContextManager context is utilized with transactions to manage the REST interface requirements.

.. topic:: Example: Update a certificate and key without removing the pair from an SSL profile

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> from f5.bigip.contexts import TransactionContextManager
        >>> mgmt = ManagementRoot('192.168.1.1.', 'user', 'pass', port=4443, token=True)
        >>> mgmt.shared.file_transfer.uploads.upload_file(key)
        >>> mgmt.shared.file_transfer.uploads.upload_file(cert)
        >>> tx = mgmt.tm.transactions.transaction
        >>> with TransactionContextManager(tx) as api:
        ...     key = api.tm.sys.file.ssl_keys.ssl_key.load(name='{0}.key'.format(domain))
        ...     key.sourcePath = 'file:/var/config/rest/downloads/{0}'.format(os.path.basename(key))
        ...     key.update()
        ...     cert = api.tm.sys.file.ssl_certs.ssl_cert.load(name='{0}.crt'.format(domain))
        ...     cert.sourcePath = 'file:/var/config/rest/downloads/{0}'.format(os.path.basename(cert))
        ...     cert.update()


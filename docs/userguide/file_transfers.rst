File Transfers
==============

The file transfer worker allows a client to transfer files through a series of GET operations for downloads and POST operations for uploads. The Content-Range header is used for both as a means to chunk the content. For reference, the workers are:

.. table::

    +---------------------+--------+------------------------------------------------+----------------------------+
    | Description         | Method | URI                                            | File Location              |
    +---------------------+--------+------------------------------------------------+----------------------------+
    | Upload Image        | POST   | /mgmt/cm/autodeploy/sotfware-image-uploads/*   | /shared/images             |
    +---------------------+--------+------------------------------------------------+----------------------------+
    | Upload File         | POST   | /mgmt/shared/file-transfer/uploads/*           | /var/config/rest/downloads |
    +---------------------+--------+------------------------------------------------+----------------------------+
    | Upload UCS          | POST   | /mgmt/shared/file-transfer/ucs-uploads/*       | /var/local/ucs             |
    +---------------------+--------+------------------------------------------------+----------------------------+
    | Download UCS        | GET    | /mgmt/shared/file-transfer/ucs-downloads/*     | /var/local/ucs             |
    +---------------------+--------+------------------------------------------------+----------------------------+
    | Download Image/File | GET    | /mgmt/cm/autodeploy/sotfware-image-downloads/* | /shared/images             |
    +---------------------+--------+------------------------------------------------+----------------------------+

Where the "*" in the URL is the base file name.

.. topic:: Example: Upload a text file

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass')
        >>> mgmt.shared.file_transfer.uploads.upload_file('/Users/citizenelah/Downloads/config.txt')

.. topic:: Example: Download a UCS file

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass')
        >>> mgmt.shared.file_transfer.ucs_downloads.download_file('config.ucs', '/Users/citizenelah/Downloads/config.ucs')


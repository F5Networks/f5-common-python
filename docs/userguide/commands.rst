Commands
========

The |exec_cmd| method is the way to run tmsh commands like run, load, and save via the SDK. It is almost always used in conjunction with an |unnamed resource|.

.. topic:: Example: Save the BIG-IP configuration

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1.', 'user', 'pass')
        >>> mgmt.tm.sys.config.exec_cmd('save')

.. topic:: Example: Merge a file into the BIG-IP configuration

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass')
        >>> options = {}
        >>> options['file'] = '/var/config/rest/downloads/myfile.txt'
        >>> options['merge'] = True
        >>> mgmt.tm.sys.config.exec_cmd('load', options=[options])

In the example above, you need to upload the file you wish to merge prior to executing this command. Also note that in version 12.1+, you will need to update the fileWhitelistPathPrefix attribute in global settings to merge files from this location.

.. topic:: Example: Generate a qkview file without core dumps or log files

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass')
        >>> mgmt.tm.util.qkview.exec_cmd('run', utilCmdArgs='-C --exclude all')

.. topic:: Example: Use the bash utility to print the host routing table

    .. code-block:: python

        >>> from f5.bigip import ManagementRoot
        >>> mgmt = ManagementRoot('192.168.1.1', 'user', 'pass')
        >>> rt_table = mgmt.tm.util.bash.exec_cmd('run', utilCmdArgs='')rt = mgmt.tm.util.bash.exec_cmd('run', utilCmdArgs='-c "netstat -rn"')
        >>> print rt.commandResult
        Kernel IP routing table
        Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
        0.0.0.0         10.10.10.1      0.0.0.0         UG        0 0          0 vlan10
        10.0.2.0        0.0.0.0         255.255.255.0   U         0 0          0 mgmt
        10.10.10.0      0.0.0.0         255.255.255.0   U         0 0          0 vlan10
        127.1.1.0       0.0.0.0         255.255.255.0   U         0 0          0 tmm
        127.7.0.0       127.1.1.253     255.255.0.0     UG        0 0          0 tmm
        127.20.0.0      0.0.0.0         255.255.0.0     U         0 0          0 tmm_bp
        192.168.102.0   0.0.0.0         255.255.255.0   U         0 0          0 vlan102
        192.168.103.0   0.0.0.0         255.255.255.0   U         0 0          0 vlan103

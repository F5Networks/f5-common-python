.. _pools-and-members_code-example:

Coding Example
==============

.. topic:: Managing LTM Pools and Members via the F5 SDK

    .. code-block:: python

        from f5.bigip import ManagementRoot

        # Connect to the BigIP and configure the basic objects
        mgmt = ManagementRoot('10.190.7.161', 'admin', 'admin')
        ltm = mgmt.tm.ltm
        pools = mgmt.tm.ltm.pools
        pool = mgmt.tm.ltm.pools.pool

        # Create a pool
        pool1 = mgmt.tm.ltm.pools.pool.create(name='pool1', partition='Common')

        # Define a pool object and load an existing pool
        pool_obj = mgmt.tm.ltm.pools.pool
        pool_1 = pool_obj.load(partition='Common', name='pool1')

        # We can also skip creating the object and load the pool directly
        pool_2 = mgmt.tm.ltm.pools.pool.load(partition='Common', name='pool1')

        # Make sure 1 and 2 have the same names and generation
        assert pool_1.name == pool_2.name
        assert pool_1.generation == pool_2.generation

        print pool_1.name
        pool1
        print pool_2.name
        pool1
        print pool_1.generation
        209
        print pool_2.generation
        209

        # Update the pool description
        pool_1.description = "This is my pool"
        pool_1.update()

        # Check the updated description
        print pool_1.description
        This is my first pool

        # Since we haven't refreshed pool_2 it shouldn't match pool_1 any more
        print pool_2.description
        This is my pool

        # Refresh pool_2 and check that is now equal
        pool_2.refresh()
        print pool_2.description
        This is my first pool

        print pool_1.generation
        210
        print pool_2.generation
        208

        # Create members on pool_1
        members = pool_1.members_s
        member = pool_1.members_s.members

        m1 = pool_1.members_s.members.create(partition='Common', name='m1:80')
        m2 = pool_1.members_s.members.create(partition='Common', name='m2:80')

        # load the pool members
        m1 = pool_1.members_s.members.load(partition='Common', name='m1:80')
        m2 = pool_1.members_s.members.load(partition='Common', name='m2:80')

        # Get all of the pool members for pool_1 and print their names

        for member in members:
            print member.name

        # Delete our pool member m1
        m1.delete()

        # Make sure it is gone
        if pool_1.members_s.members.exists(partition='Common', name='m1:80'):
            raise Exception("Object should have been deleted")

        # We are done with this pool so remove it from BIG-IP®
        pool_1.delete()

        # Make sure it is gone

        if mgmt_rt.tm.ltm.pools.pool.exists(partition='Common', name='mypool'):
            raise Exception("Object should have been deleted")



.. _pools-and-members_code-example:

Coding Example
==============

.. topic:: Managing LTM Pools and Members via the F5 SDK

    .. code-block:: python

        from f5.bigip import BigIP

        # Connect to the BigIP and configure the basic objects
        bigip = BigIP('10.190.6.253', 'admin', 'default')
        ltm = bigip.ltm
        pools = bigip.ltm.pools.get_collection()
        pool = bigip.ltm.pools.pool

        # Define a pool object and load an existing pool
        pool_obj = bigip.ltm.pools.pool
        pool_1 = pool_obj.load(partition='Common', name='mypool')

        # We can also create the object and load the pool at the same time
        pool_2 = bigip.ltm.pools.pool.load(partition='Common', name='mypool')

        # Print the object
        print pool_1.raw

        # Make sure 1 and 2 have the same names and generation
        assert pool_1.name == pool_2.name
        assert pool_1.generation == pool_2.generation

        # Update the description
        pool_1.description = "This is my pool"
        pool_1.update()

        # Check the updated description
        print pool_1.description

        # Since we haven't refreshed pool_2 it shouldn't match pool_1 any more
        assert pool_1.generation > pool_2.generation

        # Refresh pool_2 and check that is now equal
        pool_2.refresh()
        assert pool_1.generation == pool_2.generation

        print pool_1.generation
        print pool_2.generation

        # Create members on pool_1

        members = pool_1.members_s.get_collection()
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
        assert pool_1.members_s.members.exists(partition='Common', name='m1:80')

        for member in members:
            print member.name

        # We are done with this pool so remove it from bigip
        pool_1.delete()

        # Make sure it is gone
        assert not bigip.ltm.pools.pool.exists(partition='Common', name='mypool')


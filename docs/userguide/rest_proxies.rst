REST Proxies
==============

In the iWorkflow and BIG-IQ products, a feature called a "REST Proxy" is available. This
functionality allows the user of the API to use either of these products as a proxy to
the BIG-IPs under management.

There are a couple of reasons you might want to do this. Among them are,

1. Use BIG-IQ or iWorkflow as a central point of management for your BIG-IP fleet
2. Apply RBAC on the REST endpoints (i.e. limit a user to only be able to modify a
   single BIG-IP LTM pool in a single Partition.

Activation
----------

The REST Proxy must be activated on a remote device before it can be used. If you
are already using some of our automation tooling such as the Ansible modules, then
this is done for you by default.

Information on enabling the REST Proxy for a managed device on iWorkflow is discussed
more `in detail here. https://devcentral.f5.com/wiki/iWorkflow.HowToSamples_enable_rest_proxy.ashx`_

Usage
-----

Using a REST proxy is easy. First, let's take a look at the common usage of BIG-IP.

.. topic:: Common BIG-IP usage

    .. code-block:: python

        from f5.bigip import ManagementRoot

        mgmt = ManagementRoot(
            '<ip_address>', '<username>', '<password>'
        )

        virtuals = mgmt.tm.ltm.virtuals.get_collection()
        print virtuals[0].attrs

Now, we will toss in the REST proxy. In this example we'll use iWorkflow's as our proxy.

.. topic:: Using iWorkflow as a proxy to BIG-IP

    .. code-block:: python

        from f5.iworkflow import ManagementRoot

        mgmt = ManagementRoot(
            '<ip_address>', '<username>', '<password>'
            proxy_to='bigip.localdomain.com'
        )

        virtuals = mgmt.tm.ltm.virtuals.get_collection()
        print virtuals[0].attrs

Let's take a look at what exactly we did there.

First, we want to establish that we're communicating through our proxy device, so instead
of importing BIG-IP's `ManagementRoot`, we instead import iWorkflow's `ManagementRoot`.
So, the first point to make is,

| Import the `ManagementRoot` of the device you want to proxy though.

Next, we created a `ManagementRoot` like we normally would for connecting to iWorkflow.
We added an extra parameter though; the device we want to proxy to. In this case
we specified a managed device name, but we could also have specified a managed
device UUID. So, our second point is,

| Specify the device you want to `proxy_to` as a keyword argument to the `ManagementRoot`

At this point, we can use the proxy object like we would use any other BIG-IP object.
This is handy because you do not need to know any new API model. Just tell the iWorkflow
`ManagementRoot` to proxy to a specific device, and away you go.

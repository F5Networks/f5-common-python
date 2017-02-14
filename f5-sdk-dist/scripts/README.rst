f5 Package Creation and Automation
==================================

Introduction
------------
You've gon the wrong way!  This directory and lower directories are not
actually used in the standard f5-sdk package except to install the .deb and
.rpm packages.

Documentation
-------------
This is a standalone automation feature used by F5's developers to quickly and
efficiently create and test the creation of .deb and .rpm packages for this
repo.  In an instance where users would like to use the functionality of any
scripts under this directory, they agree to do so at their own risk.  F5 does
not support this part of the functionality.

Installation
------------
There is no set means to install anything here.  However, to add dependencies
for the repo, please change the ../setup_requirements.txt file to reflect the
new dependencies.

Running the code under this directory requires docker to be installed and
natively running on the host.

Usage
-----
In order to execute the creation and testing of the creation of the .deb and
.rpm packages, please execute the following:
.. code:: shell
   cd ../; python \*-dist/scripts/build.py

It is expected that a:

.. code:: shell
   ./scripts/config.JSON

Will be generated covering local paths.  From there, a new .rpm and a new .deb
files will be created.  It is also expected that the user will have 2 new
docker images added to their docker images listing.  These images are generated
through this automation and any subsequent containers that use these images
are removed automatically.

Design Patterns
~~~~~~~~~~~~~~~

It is intended for this code to be relatively easy to use and understand;
however, it is not intended for use outside of F5's general purposes of build
and build test validation.

List of Patterns For Contributing Developers
--------------------------------------------

#. Hack this list to make it more correct/complete
    For list additions assign @zancas as the PR reviewer.
#. The call operator ``()`` means: "Try to communicate with the device."
    This is a strong contract we offer the consumer of the SDK. If an SDK
    function is invoked with the call operator ``()`` the program is initiating
    a communication with the device.  That communication may fail before
    reaching the wire, but it has nonetheless been initiated.  Conversely, if
    an SDK user evaluates an SDK expression that *DOES NOT* invoke the ``()``
    call operator, then the SDK does *NOT* initiate a communication with the
    device.  Any extension to the SDK that is not consistent with this contract
    is unlikely to be incorporated into the supported repository.
#. The SDK is stupid
    The SDK doesn't decide things for the consumer, it's
    simply an interface so that Python programs can manipulate device resources
    without implementing custom URI/HTTP/network logic.  Implications:

   #. NO DEFAULTS
       The consumers of this library are themselves Python
       programs.  The Application programmer must say what they mean in their
       SDK-using program.  It violates a critical separation of concerns to add
       default values to the SDK.  Don't do it!  (Unless you have a good
       reason.)
   #. Failures generate exceptions

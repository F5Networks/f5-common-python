Developer Guide
===============



Releasing new versions
----------------------

Releasing new versions can be done in two different ways

* automatically
* manually

In this document I'll outline the steps required for manual release.

Version commit
~~~~~~~~~~~~~~

The version commit is the first step in releasing a new version. This can be done
in a later step, but for ease-of-release I'm putting it at the beginning.

To do this, first decide that you want to release a new version and that **all**
commits for that release are in the branch you're interested in releasing. We do
all work on the `development` branch.

Good, you're now ready.

The final commit will happen now and it is a simple one. You need to change the
following file.

* `f5/__init__.py`

In this file is a single line that specifies the current version of the SDK. For
example,

.. code-block:: python

   # Copyright 2016 F5 Networks Inc.
   #
   # Licensed under the Apache License, Version 2.0 (the "License");
   # you may not use this file except in compliance with the License.
   # You may obtain a copy of the License at
   #
   #    http://www.apache.org/licenses/LICENSE-2.0
   #
   # Unless required by applicable law or agreed to in writing, software
   # distributed under the License is distributed on an "AS IS" BASIS,
   # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   # See the License for the specific language governing permissions and
   # limitations under the License.
   #
   __version__ = '3.0.1'

Your job is to increment that number wisely. What is "wisely"? It means that it is
your duty to know if the fixes and additions in the release warrant a,

* major version change
* minor version change
* patch version change

The details of each of these is described here

* http://semver.org/

Let's assume that we only had a minor release. In that situation, we would change
the version line to look like this.

.. code-block:: python

   __version__ = '3.0.2'

With this change made, add it and commit it back to Github. This is the last commit
before releasing.

Additionally, since this is the last commit, it is important that you *tag* this
release at the current commit. Therefore, you should additionally issue this
command,

.. code-block:: bash

   git tag v3.0.2

And also push that tag upstream because it is what you will tell Github to release
from.

.. code-block:: bash

   git push v3.0.2 upstream

Release draft
~~~~~~~~~~~~~

Now that your release is staged (code-wise) upstream, it is time to begin the
release documentation. The primary vehicle for this is Github Releases.

The release URL can be found here,

* https://github.com/F5Networks/f5-common-python/releases

Your job is to click the **Draft a new release** button at the top right of the
page. When you do this, you will be presented with a screen that asks you for

- Tag version
- Release title
- Describe this release

Additionally, under the description there is an area where you can drag-and-drop
binary files for release.

To fill in the necessary information, first, click the *Tag version* box and
select the name of the tag you created in the last step. It should be at the
top of the list.

Next, fill in the release title. Generally speaking, the value we put in here
is

* Release version __YOUR_VERSION__

Next comes the description of the release. In this description we put some of
the highlights of the release. You can refer to older releases to get different
examples of what is required.

After you have filled out the above information, you want to click the **Save draft**
button. Do not (yet) click the Publish release button. We do this because there
are often other contributors who want to add release notes.

Once you are sure that you are done with all the release draft information from
all the contributors, you can revisit this page and click the **Publish release**
button.

Code release - Setup
~~~~~~~~~~~~~~~~~~~~

Since this is the manual version of the release process, the following is only
relevant when you are doing this by hand.

The first step is setup of the utility that we use to push the information to
the public PyPi servers. That utility is `twine` and can be installed as follows

.. code-block:: bash

   pip install twine

Configuration of twine is easy. The only thing you need to do is to refer to the
template below and put its contents into you `~/.pypirc` file.

.. code-block:: bash

   [distutils]
   index-servers =
     pypi
     pypitest

   [pypi]
   username=f5networks
   password=MyPassword

   [pypitest]
   repository=https://test.pypi.org/legacy/
   username=f5networks
   password=MyPassword

The only information above that **you** will need to provide is the `password`
value. The other information is already public knowledge.

With this information in place, let's build the source code for release to PyPi

Code release - Build
~~~~~~~~~~~~~~~~~~~~

Building code is done using two commands

* `python setup.py sdist`
* `python f5-sdk-dist/build_pkgs.py`
* `md5(sum) f5-sdk-dist/deb_dist/__PACKAGE__.deb > f5-sdk-dist/deb_dist/__PACKAGE__.deb.md5`
* `md5(sum) f5-sdk-dist/rpms/build/__PACKAGE__.rpm > f5-sdk-dist/rpms/build/__PACKAGE__.rpm.md5`

You must run the above commands in the order they are provided.

The first command is responsible for building the source tarball that will be
uploaded to PyPi and used for the `rpm` and `deb` packages we will build next.

Running the first command will produce a new directory called `dist`. In this
directory you will find a single tarball. This is the file that will be uploaded
to PyPi.

Next, you will want to build the `rpm` and `deb` files, as well as the `md5` files
that will accompany them. These files will be published on github with the
release notes.

Run the second command mentioned above. When it runs, it will want to create
a couple of Docker containers. These are Redhat and Debian based containers that
allow us to build the necessary packages.

For example,

.. code-block:: bash

   SEA-ML-RUPP1:f5-common-python trupp$ python f5-sdk-dist/build_pkgs.py
   ['/private/tmp/f5-common-python/f5-sdk-dist']
   Successfully constructed /private/tmp/f5-common-python/setup.cfg and
   /private/tmp/f5-common-python/f5-sdk-dist/deb_dist/stdeb.cfg
   Building packages...
   For Debian...
   For Redhat...
   Completed package builds...
   Initiating install tests...
   Testing Packages...
   Completed install tests
   SEA-ML-RUPP1:f5-common-python trupp$

Doing the above will drop new `rpm` and `deb` files in the following directories,

* `f5-sdk-dist/rpms/build/`
* `f5-sdk-dist/deb_dist/`

The packages additionally need MD5 hash files to accompany them in a release to
allow customers downloading them to be able to verify that what they downloaded
are the real files we published.

To generate the necessary MD5 hash files, refer to the `md5` commands above.

.. note::

   I've included both the Mac (`md5`) and Linux (`md5sum`) variants of the MD5
   hashing command in the above list. **There is not** a command literally called
   `md5(sum)`.

Running the above `md5` commands (supplementing your `rpm` and `deb` names for
`__PACKAGE__`) will create the necessary `.md5` files.

Code release - Upload
~~~~~~~~~~~~~~~~~~~~~

You now have all the artifacts you need to upload. Let's go over them again,
using the example that we've been using up to this point (3.0.2)

* dist/f5-sdk-3.0.2.tar.gz
* f5-sdk-dist/deb_dist/python-f5-sdk_3.0.2-1_1404_all.deb
* f5-sdk-dist/deb_dist/python-f5-sdk_3.0.1-1_1404_all.deb.md5
* f5-sdk-dist/rpms/build/f5-sdk-3.0.2-1.el7.noarch.rpm
* f5-sdk-dist/rpms/build/f5-sdk-3.0.1-1.el7.noarch.rpm.md5

Let's upload them!

First, let's use `twine` to upload to PyPi. This is no more difficult than
the following command.

.. code-block:: bash

   SEA-ML-RUPP1:f5-common-python trupp$ twine upload dist/*
   Uploading distributions to https://upload.pypi.org/legacy/
   Uploading f5-sdk-3.0.1.tar.gz
   SEA-ML-RUPP1:f5-common-python trupp$

Next, is the package files. To upload these, refer back to your Github Releases
page; specifically to the release you made.

You should have the ability to **Edit** your release. On the editing page, near
the bottom in the same location that it was when you first created the Draft,
you will find the area to **Attach files**.

To attach the necessary files, drag and drop them from your filesystem to the
Github page in the specified box.

.. note::

   Having trouble reaching a directory on Mac? Open a terminal, change to the
   directory you want, and then type `open .`. This will open up Finder at the
   exact location you are at and will allow you to drag files to the browser.

With the files attached, you can now click the **Update release** button.

Cake and beer
~~~~~~~~~~~~~

With the above steps complete, you can consider the f5-sdk officially released.

It is important that you do at least one download of the new code to make sure
that what you released was entirely accurate. You can do this in a `virtualenv`
or a Docker container or anything that you have handy.

.. code-block:: bash

   pip install --upgrade f5-sdk

The above command should succeed and allow you to use the SDK as you normally
would.
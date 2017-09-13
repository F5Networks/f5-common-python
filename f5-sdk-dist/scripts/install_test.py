#!/usr/bin/env python
# Copyright 2017 F5 Networks Inc.
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

"""
*** This script, install_test.py, is intentionally titled in this way so that
it does not get auto-grabbed by the tox application. ***

This script is both a standalone as well as a callable/integratable module;
thus, for terms of use, it is a modulino.  It is used to test both .deb and
.rpm build packages.

Future coverage is a always a problem that demands continuous maintenance.  As
such, this script looks to, when run directly, the build.py's
expected_operations-stored variable.

When imported, it is suggested to use the install_test class as an API.
"""

import errno
import glob
import os
import re
import sys
import traceback

from collections import deque
from collections import namedtuple
from inspect import currentframe as cf
from inspect import getframeinfo as gfi

from . import build_expectations

from . terminal import terminal
from . build_exceptions import TestError

# Globals:
builds = build_expectations.Builds()
OperationSettings = builds.OperationSettings
expected_operations = builds.expected_operations
Operation = namedtuple('Operation', 'os_type, os, version, pkg, dockerfl')


class InstallTest(object):
    """InstallTest

This is a package test API.  Basically, this class can be used to test both
rpm and deb build_pkgs packages.  These packages are tested natively, and
there must already exist a:

./*-dist/Docker/<os>/install_test/Dockerfile*<version>

For supportaiblity and expandability, 'trusty' can be interpretted as 14.04
for ubuntu; thus, this script does attempt to swap the word 'trusty' for any
given version when searching for the docker file.  The term 'trusty' can be
used interchangably; however, the actual version number will be searched for
first.
    """
    __os_types = []  # we never use this, but the caller can extract it

    def __init__(self, os_types=[], expected_opts=tuple([])):
        """Creation

install_test(os_types=[], expected_opts=tuple([]), )
    This will construct the object.

    Options:
        os_types - must be a list of operating system types that already exist
            within the expected_operations tuple([]), but are
            specifically tested against **instead of** all of them
        expected_opts - overwrites the tuple([]) expected_opterations for this
            object's instance; thus, replaces the default expected_operations
            that comes from the build_pkgs.py script
    Options are not suggested for general practice of automation, but they can
    be useful for testing purposes.
        """
        self._set_failure_reason = None
        self._set_expected_opts = expected_opts
        self._set_os_types = os_types
        self.collect_dist_dir()
        self.collect_pkgs()

    @property
    def expected_opts(self):
        """expected_opts

Defines the expected_opts tuple([OperationSettings])

This object attr is immutable.
        """
        return self.__expected_opts

    @property
    def failure_reason(self):
        """failure_reason

This attribute informs the caller that a test failure occurred.
        """
        return self.__failure_reason

    @property
    def os_types(self):
        """os_types

Defines the needed os_types to be tested that will be tested during runtime.
Format for this object should follow tuple([str, str,...]).

This object attr is immutable.
        """
        return self.__os_types

    @expected_opts.setter
    def _set_expected_opts(self, opts):
        err_msg = "expected_opts option contains a structure not recognized"
        self.__expected_opts = expected_operations
        if opts:
            if not isinstance(opts, tuple) or \
                    not isinstance(opts[0][0], OperationSettings):
                raise TestError(msg=err_msg, frame=gfi(cf()),
                                errnum=errno.ESPIPE)
            self.__expected_opts = opts

    @failure_reason.setter
    def _set_failure_reason(self, failure_reason):
        self.__failure_reason = failure_reason

    @os_types.setter
    def _set_os_types(self, types):
        if not isinstance(types, list):
            raise TypeError("os_types is not a list!")
        elif not types:
            return
        opts = list()
        for opt in self.expected_opts:
            if opt.os_type in types:
                opts.append(opt)
            else:
                print("Excluding: %s from testing" % opt.os_type)
        self._set_expected_opts = tuple(opts)
        self.__os_types = types

    def collect_dist_dir(self):
        """collect_dist_dir

Collects the distribution directory from where this script was located.
        """
        working = os.path.dirname(os.path.dirname(sys.argv[0]))
        working = no_ddots(working)
        working = os.path.abspath('..') if not working else working
        self.working = working

    def collect_pkgs(self):
        """collect_pkgs

Collects the packages found based upon the discovered dist dir and the list of
tests that are lined up.
        """
        pkgs = deque()
        dist = self.working
        docker = self.working + "/Docker/"
        for opt in self.expected_opts:
            install_test = docker + "/%s/install_test" % opt.os_type
            if opt.os_category == 'debian':
                # not setting a default b/c
                pkg_search = dist + "/deb_dist/*.deb"
                pkg_re = re.compile('_(\d+)_all\.deb')
            elif opt.os_category == 'redhat':
                pkg_search = dist + "/rpms/build/*.rpm"
                pkg_re = re.compile('el(\d+)\.noarch')
            else:
                raise TestError(opt.os_type, frame=gfi(cf()),
                                errnum=errno.ESPIPE,
                                msg='opt.os_type(%s) is not recognized!')
            entropy = glob.glob(pkg_search)
            if entropy:
                for version in opt.versions:
                    found = False
                    for pkg in entropy:
                        basename = os.path.basename(pkg)
                        match = pkg_re.search(basename)
                        if match:
                            found = match.group(1)
                            if found == version.replace('.', ''):
                                dockerfl = \
                                    install_test + "/Dockerfile.*%s" % version
                                entropy = glob.glob(dockerfl)
                                dockerfl = entropy[0] if entropy else ''
                                trusty = install_test + "/Dockerfile.trusty"
                                dockerfl = dockerfl \
                                    if os.path.isfile(dockerfl) else trusty
                                pkgs.append(Operation(opt.os_category,
                                                      opt.os_type, version,
                                                      pkg, dockerfl))
                                found = True
                                break
                        break
                    if not found:
                        self._set_failure_reason = \
                            TestError(opt.os_type, opt.version,
                                      frame=gfi(cf()), errno=errno.ESPIPE,
                                      msg='No pkg found built for')
                        print(str(self.failure_reason))
        self.tst_pkgs = pkgs

    def execute_tests(self):
        """execute_tests

Performs the series of tests specified at object creation via either:
    - Default
        expected_operations
    - Specified os_types
        build_pkgs.expected_oeprations[*].os_type
    - Specific expected_opts
        Custom tuple([OperationSettings])
        """
        if self.failure_reason:
            raise self.failure_reason
        print("Testing Packages...")
        for pkg in self.tst_pkgs:
            self.test(pkg)

    def test(self, pkg):
        """test

Performs a test against a particular install_test.Operation namedtuple.

Outside:
    obj.test(Operation(os_category, os_type, version, pkg_name, dockerfile))

    Currently, os_category is not used and can be a blank str.
        """
        container = "%s%s-%s-pkg-tester" % \
            (pkg.os, pkg.version, os.path.basename(pkg.pkg))
        build_cmd = "docker build -t %s -f %s %s" % \
            (container, pkg.dockerfl, os.path.dirname(pkg.dockerfl))
        wkg = os.path.dirname(os.path.abspath(self.working))
        tst_cmd = "docker run --privileged --rm -v %s:/var/wdir %s %s" % \
            (wkg, container,
             re.sub('.+/([^\/]+-dist/.+)', '/var/wdir/\g<1>', pkg.pkg))
        result = terminal([build_cmd], multi_stmt=True)
        frame = None
        msg = ''
        if result.succeeded:
            result = terminal([tst_cmd], multi_stmt=True)
            if result.succeeded:
                print("Package: %s Test succeeded!" % pkg.pkg)
            else:
                print(result.cli)
                frame = gfi(cf())
                msg = "Failed to perform install test"
        else:
            print(result.cli)
            frame = gfi(cf())
            msg = "Failed to build docker container to test with"
        if frame:
            self._set_failure_reason = \
                TestError(pkg.pkg, msg=msg, frame=frame, errnum=errno.ESPIPE)
            raise self.failure_reason


def no_ddots(wkg):
    """no_ddots

Returns a directory path that does not contain any regression movments in it.
That is to say the /../ FS object 'previous directory' pointer.
    """
    lower = deque()
    if '/../' in wkg:
        triage = wkg.split('/')
        for item in triage:
            if '..' == item:
                lower.pop()
            else:
                lower.append(item)
        working = '/'
        while lower:
            working = working + "%s/" + lower.popleft()
    else:
        working = wkg
    return working if os.path.isdir(working) else wkg


def main():
    """main

The standalone entrypoint to the script.  This will initiate build pkg's tests
on its own.
    """
    try:
        tests = InstallTest()
        tests.execute_tests()
    except TestError as Error:
        print(str(Error))
        exit(1)
        traceback.print_exc()
    except Exception as Error:
        print(str(Error))
        TestError(Error, frame=gfi(cf()), errno=-1)
        print(str(Error))
        traceback.print_exc()


if __name__ == '__main__':
    main()

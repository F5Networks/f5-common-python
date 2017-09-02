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
PURPOSE:
    To generate .rpm and .deb packages and test their integrity.
USAGE:
    ./build.py [os_type;version0,...versionN;package_name]
    ./build.py [--options [opts]]
        Arguments:
            If non-flagged arguments are used, then the following format is
            expected:
                <os version>;[<list of versions>];<package name>
            example:
                'redhat';6,7;f5-sdk-1.2.3-1.el7.noarch.rpm
                This will generate a redhat rpm natively for redhat versions 6
                and 7 with the name 'f5-sdk-1.2.3-1.el7.noarch.rpm'
        Options:
            --os_type - required for the --os_version and specifies a
                particular OS type to be isntalled against [redhat|ubuntu]
            --os_version - specifies the version of the os_type to be created
                and tested for
        NOTE: these options must be accounted for in the
        ../Docker/<os_type>/<os_version> file and directory presence.
    If no options are supplied, then both .rpm and .deb packages are built
    automatically based upon how this script is set under the
    expected_operations variable.
EXPANDABILITY:
    In order to expand this to natively create a .deb or .rpm package on a new
    os_type/os_version combo, it is required to create the Docker directory's
    subsequent directories to match that which already exists.

    Then update the expected_operations varaible in this file to match that
    which already exists.

    Example for ubuntu 15.0's addition:
        mkdir ../Docker/ubuntu/15.0
        cp ../Docker/ubuntu/14.01/* ../Docker/ubuntu/15.0
        vim build.py  # change the expected_operations
            ...
            expected_operations = ... 'ubuntu', ['14.01', '15.0']...
            ...
"""

from __future__ import print_function

import errno
import fcntl
import getopt
import json
import os
import re
import sys
import traceback

from scripts import build_expectations
from scripts import configure
from scripts import construct_setups
from scripts import install_test
from scripts.terminal import terminal

from scripts.build_exceptions import BuildError
from scripts.build_exceptions import DebianError
from scripts.build_exceptions import RedhatError

from inspect import currentframe as cf
from inspect import getframeinfo as gfi


# Globals...
# Keeping from confusing namespace issues...
builds = build_expectations.Builds()
OperationSettings = builds.OperationSettings
expected_operations = builds.expected_operations


def load_json():
    """load_json

Loads the config.JSON file system object's contents and translate it into a
Python object.  This python object is then returned.
    """
    try:
        env = configure.get_env()
        configure.export_to_json(env)
    except SystemExit:
        raise BuildError(msg="configure failed!  Could not build targets!",
                         frame=gfi(cf()), errno=errno.ENOSYS)
    json_fl = os.path.dirname(sys.argv[0]) + "/scripts/config.JSON"
    data = _load_json(json_fl)
    return data


def _load_json(fl):
    data = {}
    if os.path.isfile(fl) and os.access(fl, os.R_OK):
        with open(fl, 'r') as fh:
            data = json.loads(fh.read())
    else:
        print("Unable to open JSON file: " + fl)
        reason = 'Cannot Access!' if os.path.isfile(fl) else \
            "File does not exist!"
        print(reason)
        raise BuildError(fl, reason, msg="Unable to open JSON file",
                         frame=gfi(cf()), errnum=errno.ENODATA)
    return data


def build_image_name(config, os_type, os_version):
    """build_image_name

    Returns a standard docker image name based upon package parameters
    """
    name = "%s%s-%s-builder" % (os_type, os_version, config['project'])
    return name


def _build_package(config, os_type, os_version):
    build_image = build_image_name(config, os_type, os_version)
    cmd = "docker build -t %s %s/Docker/%s/%s 2>&1" % \
        (build_image, config['dist_dir'], os_type, os_version)
    result = terminal([cmd], multi_stmt=True)
    if result.succeeded:
        cmd = 'docker run --rm -v %s:%s %s /var/wdir 2>&1' % \
            (config['working'], '/var/wdir', build_image)
        result = terminal([cmd], multi_stmt=True)
    return result


def build_debian(config, os_versions, os_type='ubuntu'):
    """build_debian

Builds for a specific debian operating system with os version
specified.  By default, it will use os_type='ubuntu'
    """
    def build_pkg(config, os_type, os_version):
        result = _build_package(config, os_type, os_version)
        if not result.succeeded:
            print(result.cli)
            raise DebianError(result, os_type, os_version, frame=gfi(cf()))

    error = 0
    if isinstance(os_versions, str):
        os_version = os_versions
        try:
            build_pkg(config, os_type, os_version)
        except DebianError as error:
            error.print_msg()
    else:
        for os_version in os_versions:
            try:
                build_pkg(config, os_type, os_version)
            except DebianError as error:
                error.print_msg()
    return error


def build_redhat(config, os_versions, os_type='redhat'):
    """build_redhat

Builds for a specific redhat operating system with os version specified. By
default, it will use os_type='redhat'
    """
    def build_pkg(config, os_type, os_version):
        result = _build_package(config, os_type, os_version)
        if not result.succeeded:
            print(result.cli)
            raise RedhatError(result, os_type, os_version, frame=gfi(cf()))

    error = 0
    if isinstance(os_versions, str):
        os_version = os_versions
        try:
            build_pkg(config, os_type, os_version)
        except RedhatError as error:
            error.print_msg()
    else:
        for os_version in os_versions:
            try:
                build_pkg(config, os_type, os_version)
            except RedhatError as error:
                error.print_msg()
    # this can be the last error to be reached!
    return error


def build_packages(config):
    """build_packages

Builds for the expected_operations' OperationSettings entries.

This function is intentionaly blind, dumb and stupid to produce what it can.
However, it should also exit with a non-zero when an error does occur to keep
from the caller thinking that things are 'okay' when they are not.
    """
    error = 0
    print("Building packages...")
    for operation in expected_operations:
        if operation.os_category == 'redhat':
            print("For Redhat...")
            function = build_redhat
        elif operation.os_category == 'debian':
            print("For Debian...")
            function = build_debian
        else:
            # can overwrite a previous error statement, but this does need to
            # be preserved...
            error = BuildError(operation, msg="Unexpected operation specified",
                               frame=gfi(cf()))
            function = Error.print_msg
        # preserve a previous iteration's error, if needed
        for os_version in operation.versions:
            error = function(config, os_version) if not error else error
            if error:
                break
        if error:
            print("A Failure occurred...", str(error))
            break
    if not error:
        print("Completed package builds...")
    return error


def _preliminary_construct(config):
    # this is an internal function; however, allows for quick and easy access
    # to execute these operations...
    error = 0
    construct_setups._construct_cfgs_from_json(config)
    try:
        pass
    except Exception as error:
        print("ASDASD")
        return error
    except SystemExit:
        error = BuildError(
            config['setup_cfg'],
            config['stdeb_cfg'],
            frame=gfi(cf()),
            errno=errno.ESPIPE,
            msg="Could not construct the setup files"
        )
    return error


def get_flagged_args():
    """get_flagged_args

Collects from the execution statement the arguments provided to this script.
The items are then interpretted and returned.  The object expected are the
KvP's:
    --os_type - the operating system type to be built
    --os_version - the operating system version to be built
NOTE: by not using these options, both Debian .deb and Redhat .rpm files are
generated for the operating systems and versions natively as set by a global
variable at the top of this script.
FURTHER NOTE: there should be a
    dist_dir/Docker/<os_type>/<os_version>/DockerFile*
Present for this script to work.
CONFIGURATION:  It is part of the standard for this script to run its own
configuration parameters to generate a:
    dist_dir/scripts/config.JSON
This is a part of a separate script and is executed by this one in an effort
to make this code as translatable from project segment to segment.
    """
    expected = ['os_type', 'os_version']
    arguments = {}
    try:
        opts, adds = \
            getopt.getopt(sys.argv, '', map(lambda x: x + "=", expected))
    except getopt.GetoptError as Error:
        print(str(Error))
        print("Defaulting to standard run...")
        return arguments
    for o, a in opts:
        opt = re.sub('^-+', '', o)
        if opt in expected:
            arguments[opt] = a
    if arguments:
        if 'os_type' not in arguments:
            print("Unsupported means of operation!")
            print("You can either specify both os_type and os_version " +
                  "or just os_type")
            arguments = {}
    return arguments


def get_args():
    global expected_operations
    new_list = list()
    arg_re = re.compile('([^;]+);(\S+)')
    breakout = {'redhat': 'redhat',
                'centos': 'redhat',
                'ubuntu': 'debian',
                'mint': 'debian'}
    for arg in sys.argv[1:]:
        match = arg_re.search(arg)
        if match:
            groups = match.groups()
            category = breakout[groups[0]] if groups[0] in breakout else \
                'redhat'
            new_list.append(OperationSettings(groups[0], category, groups[1]))
    if new_list:
        expected_operations = tuple(new_list)


def handle_flagged_args(args, config):
    """handle_flagged_args

This function will execute the appropriate steps for what arguments have been
given.  This is, essentially, a good "drop in" point for outside code to use
this module as long as args is a dict within the appropriate format or is an
empty dictionary.
    """
    error = None
    os_version = str()
    os_type = str()
    os_category = \
        BuildError(args, msg="Invalid build config", frame=gfi(cf()))
    # we're building for just one, and it should already be in
    # expected_operations...
    for item in expected_operations:
        if item.name == args['os_type']:
            for version in item.versions:
                os_version = version
                os_type = item.os_type
                if item.os_category == 'redhat':
                    os_category = build_redhat
                elif item.os_category == 'debian':
                    os_category = build_debian
                else:
                    error = False
                    os_category = os_category.print_msg
                break
    error = os_category(config, os_version, os_type=os_type) if error \
        else error


def store_json(obj, destination):
    """store_json

Takes in a json-portable object and a filesystem-based destination and stores
the json-portable object as JSON into the filesystem-based destination.

This is blind, dumb, and stupid; thus, it can fail if the object is more
complex than simple dict, list, int, str, etc. type object structures.
    """
    with open(destination, 'r+') as FH:
        fcntl.lockf(FH, fcntl.LOCK_EX)
        json_in = json.loads(FH.read())
        json_in.update(obj)  # obj overwrites items in json_in...
        FH.seek(0)
        FH.write(json.dumps(json_in, sort_keys=True, indent=4,
                            separators=(',', ': ')))


def test_packages(config):
    print("Initiating install tests...")
    test_object = install_test.InstallTest()
    test_object.execute_tests()
    if not test_object.failure_reason:
        print("Completed install tests")
    else:
        raise test_object.failure_reason


def main():
    """main

The standard entry point to this script.

This script will exit with a numeric error statement.  The following are
possible:
    errno.<POSIX> - Please look to the debugging messages and the meaning to
        The standard UNIX/LINUX POSIX meanings
    -1 - An unpredictable error has occurred.  Any number of problems may
        have happened; however, all of them were not predicted by the
        developer.  This is a bug that has been detected.
    0 - Execution, as far as the program is concerned, is complete and has
        been completed successfully.  Any errors that may have resulted,
        resulted without the program's knowledge and was the result of an
        error outside of the developer's ability to predict.
    """
    flagged_args = get_flagged_args()
    working = os.getcwd()
    config = load_json()
    errnum = 0
    error = _preliminary_construct(config)
    if not error and flagged_args:
        error = handle_flagged_args(flagged_args, config)
    elif not error:
        get_args()
        error = build_packages(config)
    error = test_packages(config)
    os.chdir(working)  # no matter where we were... return.
    if error:
        errnum = error.errnum
    return errnum


if __name__ == '__main__':
    errnum = 0
    try:
        errnum = main()
    except BuildError as Error:
        traceback.print_exc()
        print("Build was not successful at either a partial or total level.")
        errnum = errno.ESPIPE if not hasattr(Error, 'errnum') else \
            getattr(Error, 'errnum')
    except Exception as Error:
        traceback.print_exc()
        errnum = -1
        print("An unpredicted error has occurred!")
    else:
        if errnum:
            print("Please look above for error statements on what failed.")
    sys.exit(errnum)

# vim: set fileencoding=utf-8

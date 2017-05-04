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
    A script that performs basic check operations against the provided
    package.  This package should be a standard .deb package that is
    pre-built.  Further, it should already be present on the local filesystem
    along with the repo code pointed to the /var/wdir directory.
USAGE:
    This script is meant to be executed on a server that natively would be
    used to install the provided package.  It is also meant to be executed
    from a docker container, or at the very least, an expendable, virtual
    server in case something is not handled properly.

    THIS SCRIPT IS NOT MEANT to be used as an install script!  It is assumed
    that this script is used exclusively for testing purposes.
EXECUTION:
    ./fetch_and_install_deps.py <working_dir> <debian package>
"""

import errno
import glob
import json
import os
import re
import shutil
import subprocess
import sys

from collections import deque
from collections import namedtuple
from inspect import currentframe as cf
from inspect import getframeinfo as gfi
from inspect import getouterframes as gof

dep_match_re = re.compile('^\s*([\w\-]+)\s\(([=<>]+)\s([^\)]+)')
f5_dependency_re = re.compile('(f5[\-_].+)')
ReqDetails = namedtuple('RegDetails', 'name, oper, version')


class InstallError(Exception):
    """InstallError

This is an exception-class object.  This object can be used to generate logs
for subsequent reporting and use.  It can also be raised in and of itself.
    """
    default_msg = "An unknown error has occurred"
    default_errnum = errno.ESPIPE

    def __init__(self, *args, **kargs):
        self._set_errnum(kargs)
        self._set_frame(kargs)
        self._set_msg(args, kargs)
        super(self.__class__, self).__init__(self.msg)

    def _set_errnum(self, kargs):
        if 'errnum' in kargs:
            self.errnum = kargs['errnum']
        elif 'errno' in kargs:
            self.errnum = kargs['errno']
        else:
            self.errnum = self.default_errnum

    def _set_frame(self, kargs):
        if 'frame' in kargs:
            self.frame = kargs['frame']
        else:
            # gof gets a stack of [inner->outer] tuples. tuple[0] is frame
            self.frame = gfi(gof(cf())[2][0])

    def _set_msg(self, args, kargs):
        msg = ''
        frame = self.frame
        if args:
            msg = ': %s' % (', '.join(args))
        elif 'message' in kargs:
            msg = kargs['message'] + msg
        elif 'msg' in kargs:
            msg = kargs['msg'] + msg
        else:
            msg = self.default_msg + msg
        self.msg = "(%s) %s [%s:%s]" % (str(self.errnum), msg, frame.filename,
                                        str(frame.lineno))


class Dependency(object):
    """Dependency

Creates a dependency object instance.  This object instance will
self-orchestrate the necessary actions to retrieve the dependencie's
requirements for installation.  It does depend on apt-get to retrieve
subsquent dependencies.
    """
    cmd = "apt-get install -y %s"

    def __init__(self, req):
        match = dep_match_re.search(str(req))
        if match:  # easiest that uses existing methods...
            self.name, self.oper, self.version = match.groups()
        else:
            self._set_name = req
            self._set_version = req
            self._set_oper = req
        self._set_req = req

    @property
    def name(self):
        return self.__name

    @property
    def oper(self):
        return self.__oper

    @property
    def req(self):
        return self.__req

    @property
    def version(self):
        return self.__version

    @name.setter
    def _set_name(self, req):
        self.__name = req.name

    @oper.setter
    def _set_oper(self, req):
        self.__oper = req.oper

    @req.setter
    def _set_req(self, req):
        self.__req = req

    @version.setter
    def _set_version(self, req):
        self.__version = req.version

    def install_req(self):
        """install_req

This object method will install the attribute-defined package yielded at
object creation.  This requires running commands at the command prompt.
        """
        if 'python-' not in self.name or '(' in self.name:
            return
        self._install_req()

    def _install_req(self):
        print("Installing %s(v%s)" % (self.name, self.version))
        name = self.pkg_location if hasattr(self, 'pkg_location') \
            else self.name
        results, status = runCommand(self.cmd % name)
        if status:
            raise InstallError(str(self.req), msg="Unable to install dep",
                               frame=gfi(cf()), errno=errno.ESPIPE)


class F5Dependency(Dependency):
    """F5Dependency

Creates a f5_dependency object.  This object will retrieve all relevant
information in regards to what is necessary for the dependency and all of its
subsequent dependencies.

The F5 packages often require further dependencies; thus, there are further
actions to perform for its automated installation.
    """
    cmd = "dpkg -i %s"

    def __init__(self, req):
        super(F5Dependency, self).__init__(req)
        self._set_url()
        self._download_pkg()
        self._consolidate_deps()

    def _consolidate_deps(self):
        try:
            dependencies = read_pkg_reqs(self.pkg_location)
            f5_reqs, other_reqs = categorize_requirements(dependencies)
            handle_f5_dependencies(f5_reqs)
            handle_other_dependencies(other_reqs)
        except Exception:
            raise InstallError(str(self.req), msg="Unable to install req",
                               frame=gfi(cf()), errno=errno.ESPIPE)

    def _download_pkg(self):
        url = self.url
        pkg_name = self.pkg_name
        deps = "/tmp/deps"
        pkg_tmp = deps + "/" + pkg_name
        try:
            os.mkdir(deps)
        except OSError:
            if not os.path.isdir(deps):
                raise InstallError(deps, msg="Unable to create",
                                   frame=gfi(cf()), errno=errno.EIO)
        cmd = "curl -L -o %s %s" % (pkg_tmp, url)
        output, status = runCommand(cmd)
        if status:
            raise InstallError(cmd, msg="Failed to download pkg",
                               errno=errno.ENODATA, frame=gfi(cf()))
        self.pkg_location = "/tmp/deps/%s" % self.pkg_name

    def _set_url(self):
        self.url = "https://github.com/F5Networks/"
        if 'f5-sdk' in self.name:
            self.url = self.url + "f5-common-python/"
        elif 'f5-icontrol-rest' in self.name:
            self.url = self.url + "f5-icontrol-rest/"
        elif 'f5-openstack-agent' in self.name:
            self.url = self.url + "f5-openstack-agent/"
        else:
            self.url = self.url + re.sub('^python-', '', self.name)
        self.url = self.url + "releases/download/v%s/" % \
            re.sub('-\d+', '', self.version)
        version = self.version + "-1" if '-1' not in self.version else \
            self.version
        name = 'python-' + self.name if 'python-' not in self.name else \
            self.name
        pkg_name = "%s_%s_1404_all.deb" % (name, version)
        self.pkg_name = pkg_name
        self.url = self.url + pkg_name

    def install_req(self):
        """install_req

This object method will install the attribute-defined package yielded at
object creation.  This requires running commands at the command prompt.
        """
        self._install_req()


def usage():
    """usage

A function that prints to the CLI a usgae statement for the script.
    """
    print("fetch_dependencies.py working_dir package")


def runCommand(cmd):
    """runCommand

Executes the command provided and returns the stdout and the resulting return
code.  In the event that the execution fails, a return code of 99 is yielded
and the output is redacte to an empty string.
    """
    output = ""
    try:
        output = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Execution failed: [{}]".format(e))
    else:
        return (output, 0)
    return (str(e), 99)


def load_requirements(cfg):
    """load_requirements

Loads the requirements from the file that the 'setup_requirements' KVP
contains.  The argument should provide the dictionary that contains this KVP
    """
    reqs = parse_req(cfg['setup_requirements'])
    return reqs


def categorize_requirements(reqs):
    """categorize_requirements

Takes in a list of dependencies and sorts them between F5 generated items and
standard packages.  Then returns the F5's first, then the others in two
separate deque's.
    """
    f5_specific = deque()
    other = deque()
    for req in reqs:
        if f5_dependency_re.search(req.name):
            f5_specific.append(req)
        else:
            other.append(req)
    return f5_specific, other


def read_pkg_reqs(pkg_name):
    """read_pkg_reqs

Reads in from `dpkg -I` of the package file and parses the output for package
dependencies.
    """
    requires = deque()
    # Get the sdk requirement.
    requiresCmd = "dpkg -I %s" % pkg_name
    (output, status) = runCommand(requiresCmd)

    if status:
        print("Failed to read")
        raise InstallError(pkg_name, msg="Could not read deps from pkg",
                           errnum=errno.EIO, frame=gfi(cf()))

    for line in output.split('\n'):
        if 'Depends' not in line:
            continue
        for dep in output.split(','):
            match = dep_match_re.match(dep)
            if match:
                groups = list(match.groups())
                my_dep = ReqDetails(*groups)
                requires.append(my_dep)
        break
    return requires


def compare_reqs(reqs_from_pkg, requirements):
    """compare_reqs

This function will compare the requirements extracted from the dpkg command's
output against the requirements parsed from the setup_requirements.py.  It
assumes that the dpkg contents are in the first argument and the setup's in
the second.

When a discrepency is found, then an InstallError exception is thrown
    """
    for setup_req in requirements:
        accounted = False
        for pkg_req in reqs_from_pkg:
            if pkg_req.name == str(setup_req.name):
                accounted = True
            elif "python-" + setup_req.name == str(pkg_req.name):
                accounted = True  # special to debian, really...
        if not accounted:
            print("requirements:", map(lambda x: (x.name), requirements))
            print("reqs_from_pkg:", map(lambda y: (y.name), reqs_from_pkg))
            raise InstallError(str(setup_req),
                               msg="Could not find req in pkg",
                               errno=errno.ESPIPE, frame=gfi(cf()))
    for pkg_req in reqs_from_pkg:
        if '(' in pkg_req.name or 'f5-' not in pkg_req.name or 'python-' not \
                in pkg_req.name:
            continue
        accounted = False
        for setup_req in requirements:
            if 'python-' + setup_req.name == pkg_req.name:
                accounted = True
        if not accounted:
            print(pkg_req, requirements)
            raise InstallError(str(pkg_req), msg="Additional req in pkg",
                               errno=errno.ESPIPE, frame=gfi(cf()))


def handle_f5_dependencies(f5_reqs):
    """handle_f5_dependencies

This function orchestrates the proper installation of F5 packages.  As such,
it will attempt to install the most relevant version of the current package.
    """
    version_re = re.compile('(\d+)\.(\d+)\.(\d+)')
    VersionBreakout = namedtuple('VersionBreakout', 'high, medium, low')
    installed = dict()
    pending_check = dict()
    for item in f5_reqs:
        version = item.version if version_re.search(item.version) else \
            item.version + ".0.0"
        version_breakout = \
            VersionBreakout(*version_re.search(version).groups())
        if item.name not in installed and '=' in item.oper:
            req = F5Dependency(item)
            installed[item.name] = version_breakout
            req.install_req()
        elif item.name in installed:
            present = installed[item.name]
            if present.high < version_breakout.high and '<' in item.oper:
                pass
            elif '<' not in item.oper:
                pass
            else:
                raise InstallError(present, item, msg="Version mismatch!",
                                   errnum=errno.ESPIPE, frame=gfi(cf()))
        else:
            pending_check[item.name] = version_breakout  # could expand...
    return


def handle_other_dependencies(other_reqs):
    """handle_other_dependencies

This function orchestrates the installation of non-F5 packages and modules.
    """
    for item in other_reqs:
        req = Dependency(item)
        req.install_req()
    return


def fetch_pkg_dependencies(config, pkg_name):
    """fetch_pkg_dependencies

This function will attempt to install all missing dependencies.  Also, to
assure that the build was successful, the setup_requirements.txt will be
compared to the requirements laid out in the package.

Upon failure, it will return the exception that was thrown at that time, or it
will return 0.  For simplicity of the main(), this method heavily depends upon
the InstallError exception for known scenarios where things may break.
    """
    requirements = load_requirements(config)
    f5_reqs, other_reqs = categorize_requirements(requirements)

    # Copy pkg package to /tmp
    print("Copying package to /tmp install directory")
    try:
        tmp_pkg_name = "/tmp/" + os.path.basename(pkg_name)
        shutil.copyfile(pkg_name, tmp_pkg_name)
    except Exception as error:
        print("Failed")
        return \
            InstallError(str(error), pkg_name, tmp_pkg_name, frame=gfi(cf()),
                         errnum=errno.EIO,
                         msg="Failed to copy f5-sdk package!")
    print("Success")

    print("Compare structured pkg dependencies against what was built")
    try:
        reqs_from_pkg = read_pkg_reqs(tmp_pkg_name)
        compare_reqs(reqs_from_pkg, requirements)
    except InstallError as error:
        print(str(error))
        print("Failed")
        return error

    # handle dependency installation:
    print("Installing Dependencies:")
    try:
        handle_f5_dependencies(f5_reqs)
        handle_other_dependencies(other_reqs)
    except InstallError as error:
        print("Failed")
        return error

    print("Installing Self - %s" % pkg_name)
    try:
        output, result = runCommand('dpkg -i %s 2>&1' % tmp_pkg_name)
        if not result == 0:
            raise IOError("Result was non-zero! [{}:{}]".format(output,
                                                                result))
    except InstallError as error:
        print("Failed to get requirements for %s." % (pkg_name))
        return error
    print("Success")


def parse_req(location):
    mod_read = re.compile('^([^<=>]+)([<=>]+)(\S+)')
    skip_re = re.compile('^\s*#')
    listing = list()
    with open(location, 'r') as fh:
        line = fh.readline()
        while line:
            if skip_re.search(line):
                line = fh.readline()
                continue
            match = mod_read.search(line)
            if match:
                listing.append(ReqDetails(*match.groups()))
            line = fh.readline()
    return listing


def load_config(config_json):
    """load_config

This loads a dist_dir/scripts/config.JSON file that contains the appropriate
mappings required to build the packages and test them.
    """
    data = None
    try:
        with open(config_json, 'r') as fh:
            data = json.loads(fh.read())
    except Exception as Error:
        raise InstallError(str(Error), config_json, frame=gfi(cf()),
                           errno=errno.ESPIPE,
                           msg="Could not laod config.JSON")
    return data


def get_args(argv):
    """get_args

Attempts to map out the input arguments into the anticipated format.  If an
incorrect number of arguments are provided, or if the arguments provided do
not map out properly, then an InstallError will be raised.
    """
    error = None
    try:
        working_dir, package_name = argv
    except IndexError as error:
        pass
    except ValueError as error:
        pass
    except IndexError as error:
        pass
    if not os.path.isdir(working_dir) or not os.access(working_dir, os.R_OK):
        error = InstallError(working_dir, errnum=errno.EIO, frame=gfi(cf()),
                             msg="Directory given cannot be accessed")
    if error:
        InstallError(str(error), msg="Improper list of input arguments",
                     frame=gfi(cf()))
        usage()
        sys.exit(errno.EINVAL)
    return working_dir, package_name


def check_dist_dir(dist_dir):
    """check_dist_dir

This checks the given dist_dir for validity and raises if it is not valid.
    """
    try:
        dist_dir = glob.glob(dist_dir)[0]
    except IndexError:
        raise InstallError(dist_dir, frame=gfi(cf()), errnum=errno.ENOSYS,
                           msg="No dist dir found under the working")
    return dist_dir


def main(args):
    """main

The entrypoint to the script.  The script will exit with a non-zero value in
error.  Any other value indicates that an issue occurred.
    """
    error = None
    working_dir, pkg_name = get_args(sys.argv[1:])
    os.chdir("/var/wdir")

    dist_dir = check_dist_dir(working_dir + "/*-dist")
    try:
        config = load_config(dist_dir + "/scripts/config.JSON")
    except InstallError as error:
        pass
    # Get all files for the package.
    error = fetch_pkg_dependencies(config, pkg_name) if not error else error
    # Instal from the tmp directory.
    if error:
        sys.exit(error.errnum)
    # last chance to check for failure:
    cmd = 'dpkg -l | grep {}'.format(config['project'])
    output, status = runCommand(cmd)
    if status == 0:
        print("passed last check:\n{}".format(output))
        sys.exit(0)
    print("Last check FAILED: {}".format(cmd))
    sys.exit(99)


if __name__ == '__main__':
    main(sys.argv)

# vim: set fileencoding=utf-8

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

from __future__ import print_function

import errno
import getopt
import glob
import json
import os
import re
import sys

from collections import deque
from collections import namedtuple
from pip.req import parse_requirements as p_reqs


def construct_cfgs(**kargs):
    """construct_cfgs

Performs actions to construct either the setup.cfg (rpm) or stdeb.cfg (deb)
files as per the operating system specified.  This construction is done as
per the setup_requirements.txt file from within the working directory
specified.

This is a very tempermental function by design.  It intentionally exits
with a non-zero if/when an error has occurred on its own.  Therefore, it is
not suggested to use this function if you intend to get control back again.
    """
    docker_dir = _check_args(**kargs)
    if not docker_dir or not os.path.isdir(docker_dir):
        print("Unable to determine the %s/%s combo under supported versioning"
              % (kargs['operating_system'], kargs['version']))
        exit_cleanly(error_number=errno.ENOSYS)
    if kargs['operating_system'] == 'redhat':
        _build_setup_cfg(kargs['working_directory'])
    elif kargs['operating_system'] == 'ubuntu':
        _build_stdeb_cfg(kargs['working_directory'])
    else:
        print("Unsure of what to do... operating_system(%s) is not recognized!"
              % kargs['operating_system'])


def _construct_cfgs_from_json(args):
    Args = namedtuple('Args', 'setup, reqs, fmt, start')
    rpm = Args(args['setup_cfg'], args['setup_requirements'], '%s%s',
               'requires = ')
    deb = Args(args['stdeb_cfg'], args['setup_requirements'], '%s (%s), ',
               'Depends:\n     ')
    _construct_file(rpm.setup, rpm.reqs, rpm.fmt, rpm.start)
    _construct_file(deb.setup, deb.reqs, deb.fmt, deb.start)
    print("Successfully constructed %s and\n%s" %
          (args['setup_cfg'], args['stdeb_cfg']))


def _read_in_cfgs(cfg):
    cfgs = deque()
    break_re = re.compile('^[^#\W]')
    req_re = re.compile('^Depends:|^requires\s*=\s*')
    try:
        with open(cfg, 'r') as fh:
            read = True
            line = fh.readline()
            while line:
                read = True if break_re.search(line) and not read else read
                if req_re.search(line):
                    read = False
                if read:
                    cfgs.append(line)
                line = fh.readline()
    except IOError:
        pass  # we then have empty contents... all well...
    return cfgs


def _build_setup_cfg(wkg):
    setup_cfg = wkg + "/setup.cfg"
    setup = wkg + "/setup_requirements.txt"
    fmt = "%s%s"
    _construct_file(setup_cfg, setup, fmt, 'requires = ')


def _build_stdeb_cfg(wkg):
    setup_cfg = glob.glob(wkg + "/*-dist/deb_dist/stdeb.cfg")
    setup = wkg + "/setup_requirements.txt"
    fmt = "%s (%s),"
    if not setup_cfg:
        dist = glob.glob(wkg + "/*-dist")
        if not dist:
            print(str(EnvironmentError("Unable to find a *-dist directory")))
            print("No dist directory under: " + wkg)
            exit_cleanly(error_number=errno.ENOSYS)
        deb_dist = dist[0] + "/deb_dist"
        try:
            os.mkdir(deb_dist)
        except IOError as Error:
            if not os.path.isdir(deb_dist):
                print(str(Error))
                print("Unable to determine the existence of: " + deb_dist)
                exit_cleanly(error_number=errno.ENOSYS)
        setup_cfg = deb_dist + "/stdeb.cfg"
    else:
        setup_cfg = setup_cfg[0]
    _construct_file(setup_cfg, setup, fmt, 'Depends:\n    ')


def _construct_file(setup_cfg, setup, fmt, start):
    if not os.path.isfile(setup) or not os.access(setup, os.R_OK):
        print(setup + " does not exist or is not readable")
        exit_cleanly(error_number=errno.ENOSYS)
    contents = _read_in_cfgs(setup_cfg) if os.path.isfile(setup_cfg) else deque()
    parsed_reqs = list(map(lambda x: (x.req), p_reqs(setup, session="pkg")))
    if not parsed_reqs:
        print("Nothing to do!\n%s\nDoes not contain any reqs parsable!" % setup)
        exit_cleanly(error_number=0)
    try:
        with open(setup_cfg, 'w') as fh:
            if contents:
                while contents:
                    fh.write(contents.popleft())
            fh.write(start)
            for count in range(len(parsed_reqs)):
                req = parsed_reqs[count]
                if 'Depends' in start:
                    # special case for debian...
                    name = str(req.name) if 'python-' in str(req.name) else 'python-' + str(req.name)
                else:
                    name = str(req.name)
                fh.write(fmt % (name, str(req.specifier)))
                if count != len(parsed_reqs) - 1:
                    fh.write('\n    ')
    except IOError as Error:
        print(Error)
        exit_cleanly(error_number=errno.EIO)


def _check_args(operating_system=None, version=None, working_directory=None):
    accepted_docker_dir = None
    try:
        docker_dir = str(working_directory) + "/*-dist/Docker/%s/%s"
    except TypeError as Error:
        print("working_directory is of invalid type! (%s)" %
              str(type(working_directory)))
        exit_cleanly(error_number=errno.EINVAL)
    except Exception as Error:
        print(str(Error))
        print("'%s' is not a valid working_directory!" %
              str(working_directory))
        exit_cleanly(error_number=errno.EINVAL)
    if operating_system not in ['ubuntu', 'redhat']:
        print("'%s' is not a valid or recognized operating_system option" %
              operating_system)
        exit_cleanly(error_number=errno.EINVAL)
    else:
        possible = glob.glob(docker_dir % (operating_system, version))
        if possible:
            accepted_docker_dir = possible[0]
    if not accepted_docker_dir:
        print("(operating_system=%s, version=%s, working_directory=%s)" %
              (operating_system, version, working_directory))
        print("Are not acceptable arguments resulting in a Docker " +
              "file location")
        exit_cleanly()
    return accepted_docker_dir


def exit_cleanly(error_number=0):
    """exit_cleanly

Performs standard error notification and exiting statements as necessary.  This
assures more consistent error handling within the script.
    """
    default = "An Unknown error has occurred!"
    descriptions = \
        {22: 'An improper input error has occurred.  Please see above stmt(s)',
         29: 'An operation failed.  Please see above stmt(s)',
         5: 'An IO Error has occurred.  Pelase see above stmt(s)'}
    try:
        error_number = int(error_number)
    except TypeError:
        stmt = default
        error_number = -1
    if error_number == 0:
        stmt = "No error has been detected!"
    elif not isinstance(error_number, int) and hasattr(errno, error_number):
        error_number = getattr(errno, error_number)
        stmt = descriptions[error_number] if error_number in descriptions \
            else default
    elif error_number in descriptions:
        stmt = descriptions[error_number]
    else:
        stmt = default
    if error_number:
        print("""
%s [--opt [option]]
    With opts:
        working_directory - the full path to the working directory
        operating_system - the full name of the operating system lower case
        version - the version of the operating system

    All of these options must be supplied, and if one is missing or if there is
    no corresponding:
        <working_directory>/*-dist/Docker/<operating_system>/<version>
    Directory, then this script will exit cleanly reporting it as an error.
            """ % sys.argv[0])
    print("(%d) %s" % (error_number, stmt), file=sys.stderr)
    sys.exit(error_number)


def _load_json(json_fl):
    try:
        with open(json_fl, 'r') as fh:
            data = json.loads(fh.read())
    except Exception as Error:
        print(Error)
        print("Unable to read in " + json_fl)
    return data


def get_args():
    """get_args

This function extracts the script arguments within the arguments variable and
interprets their meaning before returning such content.
    """
    expected = ['working_directory', 'operating_system', 'version']
    possible = ['json'].extend(expected)
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', map(lambda x: ('%s=' % x),
                                   possible))
    except getopt.GetoptError as err:
        print(str(err))
        exit_cleanly(error_number=errno.EINVAL)
    arguments = dict()
    for o, a in opts:
        option = re.sub('^-*', '', o)
        if 'json' in option:
            arguments = _load_json(a)
            break
        if option in expected:
            arguments[option] = a
    error = 0
    for item in expected:
        if item not in arguments:
            print("Missing: %s from arguments" % item)
            error = errno.EINVAL
    if error:
        exit_cleanly(error_number=error)
    return arguments


def main():
    """main

The entrypoint function.  This function should also handle any runtime
errors and exceptions in a cleanly fashon.
    """
    try:
        args = get_args()
        if 'setup_cfg' in args and 'stdeb_cfg' in args:
            _construct_cfgs_from_json(args)
        else:
            construct_cfgs(**args)
    except Exception as Error:
        print(str(Error))
        print("Exiting cleanly...")
        exit_cleanly()
    exit_cleanly(error_number=0)


if __name__ == '__main__':
    main()

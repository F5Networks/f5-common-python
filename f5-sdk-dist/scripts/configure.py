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

import errno
import glob
import json
import os
import re
import sys


def add_package(pkg_type, pkg_name, working=None):
    """add_package

Adds a package to the existing config.JSON file.  This is a standalone function
to handle this functionality.  The existing config.JSON is read in and is left
unchanged.
    """
    kvp = {pkg_type: pkg_name}
    working = os.getcwd() if not working else os.path.abspath(working)
    if '-dist/scripts' in working:
        config = working + "/config.JSON"
    elif '-dist' in working:
        config = working + "/scripts/config.JSON"
    else:
        config = working + "/*-dist/scripts/config.JSON"
        entropy = glob.glob(config)
        if entropy:
            config = entropy[0]  # we'll just assume it's the first one...
    print("config", config, 'working', working)
    config = load_config(config)
    config.update(kvp)
    export_to_json(config)


def exit_cleanly(errnum=None):
    """exit_cleanly

Exits the runtime cleanly using SystemExit.  This is the official, handling
exception here as this is mostly meant to be a standalone script.
    """
    default = "An Unknown Error has Occurred!"
    cases = {errno.EINVAL: "Improper or invalid input value",
             errno.ESPIPE: "Could not complete action due to a broken" +
             " dependency",
             errno.ENOSYS: "Could not complete action due to unexpected setup",
             errno.EIO: "Could not access an expected file",
             errno.EPERM: "Could not access an item due to permissions issues",
             -1: default}
    help_stmt = """
%s [--opt [option]]
    With opts:
        working_directory - ONLY use this if you're overwriting `pwd`!
    """ % (sys.argv[0])
    if not errnum:
        errnum = 0
    elif not isinstance(errnum, int) and hasattr(errno, errnum):
        errnum = getattr(errno, errnum)
    try:
        errnum = int(errnum)
    except TypeError:
        errnum = -1
    if errnum == 0:
        help_stmt = ''
        stmt = "Successful in configuration!"
    elif errnum in cases:
        stmt = cases[errnum]
    else:
        stmt = default
    print("%s\n\n%s" % (stmt, help_stmt))


def get_env(working_directory=None):
    """get_env

This function grabs key/value pair items and assigns them for the
config.JSON.  This essentially checks the environment for key locations within
the filesystem.
    """
    working = working_directory if working_directory else os.getcwd()
    dist_dirs = glob.glob(working + "/f5-*-dist")
    print(dist_dirs)
    dist_dir_re = re.compile('/([^/]+)-dist/?')
    if dist_dirs:
        dist_dir = dist_dirs[0]
        match = dist_dir_re.search(dist_dir)
        if match:
            project_name = match.group(1)
        else:
            print("Unrecognized run location:\n" + working)
            exit_cleanly(errnum=errno.EIO)
    elif '-dist/scripts' in working:
        match = dist_dir_re.search(working)
        if match:
            project_name = match.group(1)
    else:
        print("Unable to determine the *-dist directory from " + working)
        exit_cleanly(errnum=errno.ENOSYS)
    stdeb_cfg = dist_dir + "/deb_dist/stdeb.cfg"
    setup_cfg = working + "/setup.cfg"
    stp_reqs = working + "/setup_requirements.txt"
    scripts = dist_dir + "/scripts"
    env = {'working': working, 'dist_dir': dist_dir, 'stdeb_cfg': stdeb_cfg,
           'setup_requirements': stp_reqs, 'setup_cfg': setup_cfg,
           'scripts': scripts, 'project': project_name}
    return env


def export_to_json(env):
    """export_to_json

This function takes in a dictionary object and stores it within the config.JSON
file.
    """
    json_fl = env['scripts'] + "/config.JSON"
    with open(json_fl, 'w') as fh:
        fh.write(json.dumps(env, sort_keys=True, indent=4,
                            separators=(',', ': ')))


def load_config(filename):
    """load_config

This function will take in a file location on the file system and extract the
JSON content found within and return a python-interpretted form of the object.
    """
    config = None
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        with open(filename, 'r') as fh:
            config = json.loads(fh.read())
    return config


def main():
    """main

This is the entrypoint for this script when executed on its own as a standalone
script.
    """
    env = get_env()
    export_to_json(env)


if __name__ == '__main__':
    main()

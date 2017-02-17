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

import glob
import json
import os
import shutil
import subprocess
import sys
import traceback


def get_config(src_dir):
    """get_config

Will first create it's own configuration based upon the environment, then load
and return it.
    """
    config = None
    configure = "%s/*-dist/scripts/configure.py" % src_dir
    entropy = glob.glob(configure)
    if entropy:
        for item in entropy:
            config = os.path.dirname(item) + "/config.JSON"
            if os.path.isfile(config):
                configure = item
                break
    if os.path.isfile(config) and os.path.isfile(configure):
        subprocess.check_output(str("python %s" % configure).split())
        with open(config, 'r') as fh:
            config = json.loads(fh.read())
    else:
        raise EnvironmentError("Exp setup parameters missing!")
    return config


def main():
    """main

Entrypoint to this script.  This will execute the functionality as a standalone
element
    """
    src_dir = sys.argv[1]
    os.chdir(src_dir)
    config = get_config(src_dir)
    cmd = 'python -c "import f5;print(f5.__version__)"'
    version = \
        subprocess.check_output([cmd], shell=True).strip()
    tmp_dist = "/var/deb_dist"
    project = config['project']
    tmp_dist = "/var/deb_dist"
    os_version = "1404"
    deb_dir = "%s/deb_dist" % config['dist_dir']
    print("Building %s debian packages..." % project)
    shutil.copyfile("%s/stdeb.cfg" % (deb_dir), "./stdeb.cfg")
    shutil.copytree(deb_dir, tmp_dist)
    cmd = 'python setup.py --command-packages=stdeb.command sdist_dsc ' + \
        '--dist-dir=%s' % tmp_dist
    print(subprocess.check_output([cmd], shell=True))
    os.chdir("%s/%s-%s" % (tmp_dist, project, version))
    cmd = 'dpkg-buildpackage -rfakeroot -uc -us'.split()
    subprocess.check_output(cmd)  # args will not show up in ps...
    os.chdir(src_dir)
    pkg = "python-%s_%s-1" % (project, version)
    os_pkg = pkg + "_%s_all.deb" % os_version
    pkg = pkg + "_all.deb"
    shutil.copyfile("%s/%s" % (tmp_dist, pkg), "%s/%s" % (deb_dir, os_pkg))
    cmd = "python %s/add_pkg_name.py deb_pkg %s/%s" % \
        (config['scripts'], deb_dir, os_pkg)


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as Error:
        print(str(Error))
        traceback.print_exc()
        sys.exit(29)  # Broken pipe
    except Exception as Error:
        print(str(Error))
        traceback.print_exc()
        sys.exit(-1)  # Unknown
    # for debug and avoiding frustration purposes, it may be useful to add:
    # shutil.rmtree("/var/deb_dist", ignore_errors=True)

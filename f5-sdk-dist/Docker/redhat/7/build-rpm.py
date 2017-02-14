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

from tempfile import mkdtemp


class temp_dir(object):
    def __enter__(self):  # replaces the __init__ here...
        self.tdir = mkdtemp()
        return self

    def __exit__(self, *args):
        shutil.rmtree(self.tdir)

    def chdir(self):
        os.chdir(self.tdir)


def get_config(src_dir):
    """get_config

    Will first create it's own configuration based upon the environment, then
    load and return it.
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


def make_rpms_build(config):
    try:
        os.mkdir(config['dist_dir'] + "/rpms")
    except IOError:
        if not os.path.isdir(config['dist_dir'] + '/rpms'):
            raise
    except OSError:
        if not os.path.isdir(config['dist_dir'] + '/rpms'):
            raise
    rpm_build = config['dist_dir'] + "/rpms/build"
    try:
        os.mkdir(rpm_build)
    except IOError:
        if not os.path.isdir(config['dist_dir'] + '/rpms'):
            raise
    except OSError:
        if not os.path.isdir(config['dist_dir'] + '/rpms'):
            raise
    return rpm_build


def main():
    src_dir = sys.argv[1]
    os.chdir(src_dir)
    config = get_config(src_dir)
    project = config['project']
    os_version = "7"
    print("Building %s redhat packages..." % project)
    with temp_dir() as tdir:
        buildroot = tdir.tdir + "/wdir"
        shutil.copytree(src_dir, buildroot,
                        ignore=lambda d, files: [f for f in files
                                                 if f.startswith('.')])
        os.chdir(buildroot)
        cmd = "python setup.py build bdist_rpm --rpm-base rpmbuild"
        print(subprocess.check_call([cmd], shell=True))
        with open('/root/.rpmmacros', 'w') as fh:
            fh.write('%s_topdir %s/rpmbuild' % ('%', buildroot))
        cmd = "python setup.py bdist_rpm --spec-only --dist-dir rpmbuild/SPECS"
        print(subprocess.check_output([cmd], shell=True))
        cmd = "rpmbuild -ba rpmbuild/SPECS/%s.spec" % project
        print(subprocess.check_output([cmd], shell=True))
        nonarch_pkg = None
        rpm_build = make_rpms_build(config)
        for pkg in glob.glob(buildroot + "/rpmbuild/RPMS/noarch/*.rpm"):
            if '.noarch.rpm' in pkg:
                os_pkg = \
                    pkg.replace(".noarch.rpm", ".el%s.noarch.rpm" % os_version)
                os.rename(pkg, os_pkg)
                pkg = os_pkg
                nonarch_pkg = rpm_build + "/%s" % os.path.basename(pkg)
            new_location = rpm_build + "/%s" % os.path.basename(pkg)
            shutil.copyfile(pkg, new_location)
        os.chdir(src_dir)
    cmd = "python %s/add_pkg_name.py rpm_pkg %s" % \
        (config['scripts'], nonarch_pkg)
    subprocess.check_output([cmd], shell=True)
    if not os.path.isfile(nonarch_pkg):
        print("RPM package could not be created!")
        sys.exit(29)


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as Error:
        print(str(Error))
        traceback.print_exc()
        sys.exit(29)  # ESPIPE
    except Exception as Error:
        print(str(Error))
        traceback.print_exc()
        sys.exit(-1)  # UNKNOWN
    # for debug and avoiding frustration purposes, it may be useful to add:
    # shutil.rmtree("/var/deb_dist", ignore_errors=True)

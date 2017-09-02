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
import re
import shutil
import subprocess
import sys
import traceback

from collections import namedtuple
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


def change_requires(buildroot, config):
    spec = buildroot + "/rpmbuild/SPECS/{}.spec".format(config['project'])
    try:
        with open(spec, 'r') as fh:
            contents = fh.read()
    except IOError as Error:
        print("Could not open spec file! ({})".format(Error))
        raise
    try:
        with open(spec, 'w') as fh:
            for line in contents.split("\n"):
                if 'Requires' in line:
                    old = line.replace("Requires: ", "")
                    Req = namedtuple('Req', 'module, modifier, version')
                    breakout_re = re.compile('([^<=>]+)([<=>]+)([\d]\S+)')
                    change = 'Requires: '
                    modifier_format = "{} {} {}, "
                    for requirement in old.split(' '):
                        match = breakout_re.search(requirement)
                        if match:
                            req = Req(*match.groups())
                            mod = 'python-' + req.module \
                                if 'python-' not in req.module and \
                                'f5-' not in req.module else req.module
                            change = change + \
                                modifier_format.format(mod, req.modifier,
                                                       req.version)
                    line = change
                fh.write("{}\n".format(line))
    except Exception as Error:
        print("Could not handle change in spec file {}".format(Error))
        raise


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
        change_requires(buildroot, config)
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

    cmd = "python ./f5-sdk-dist/add_pkg_name.py rpm_pkg %s" % (nonarch_pkg)
    subprocess.check_output(cmd, shell=True)
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

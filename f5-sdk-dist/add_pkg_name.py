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
import os
import sys

from scripts.configure import add_package


def store(script, pkg_type, pkg_name):
    working = os.path.dirname(script)
    add_package(pkg_type, pkg_name, working=working)


def usage():
    print("%s <pkg_type> <pkg_name>" % sys.argv[0])
    exit(-1)


def main():
    if not len(sys.argv) == 3:
        usage()
    store(*sys.argv)


if __name__ == '__main__':
    main()
    exit(0)

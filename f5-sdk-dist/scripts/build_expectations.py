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

from collections import namedtuple

OperationSettings = namedtuple('OperationSettings',
                               'os_type, os_category, versions')


class Builds(object):
    """Builds

Creates an instance of a global object Builds.  This object can then be used to
extract globals.  This object cannot retain knowledge in regards to its
acknowledged attributes.

These globals are:
expected_operations - retains the build information on what will be built
OperationSettings - A namedtuple used throughout the project that keeps values
    that, if they were mutable, might otherwise be dangerous.
    """
    __OperationSettings = OperationSettings
    # When expanding the following variable, please make sure that you have a
    # Dockerfile that is found under the:
    # repo-dist/Docker/<os>/<os_version>/
    # Directory.  Without this, the script will fail.  The Dockerfile should
    # have its own ENTRYPOINT and handle the installation of the package on its
    # own.
    __expected_operations = \
        tuple([OperationSettings('ubuntu', 'debian', ['14.04']),
               OperationSettings('redhat', 'redhat', ['7'])])

    def __init__(self):
        pass

    @property
    def expected_operations(self):
        """expected_operations

An immutable, static tuple of OperationSettings instances used throughout the
build and test build code to determine what is built through automation.
        """
        return self.__expected_operations

    @property
    def OperationSettings(self):
        """OperationSettings

An immutable, static namedtuple that is used to construct the
expected_operations attribute.

This is also used throughout the project for expected_operations replacements
for its structure.
        """
        return self.__OperationSettings

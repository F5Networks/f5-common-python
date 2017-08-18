# Copyright 2015-2016 F5 Networks Inc.
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

import logging
import os
import pytest
import shutil
import tempfile
import time
import fcntl
from f5.sdk_exception import F5SDKError
from distutils.version import LooseVersion

logger = logging.getLogger()
logger.setLevel(logging.WARNING)


@pytest.fixture(scope='function')
def sigset(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    sig = mgmt_root.tm.asm.signature_sets_s.signature_set.create(
        name=name
    )
    yield sig
    sig.delete()


@pytest.fixture(scope='function')
def sigset2(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    sig = mgmt_root.tm.asm.signature_sets_s.signature_set.create(
        name=name,
        defaultBlock=False
    )
    yield sig
    sig.delete()

from __future__ import absolute_import
# Copyright 2016 F5 Networks Inc.
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

from f5.devtools.source_engine import SourceEngine
from f5.devtools.template_engine import TemplateEngine

import os

UTILSDIR = os.path.abspath(os.path.dirname(__file__))
COMMONPREFIX = os.path.dirname(UTILSDIR)
SOURCE_ROOTDIR = os.path.join(COMMONPREFIX, 'f5', 'bigip')
TEMPLATEDIR = os.path.join(UTILSDIR, 'template_library')
DEVICECONFDIR = os.path.join(UTILSDIR, 'device_configs')


def main():
    temp_eng = TemplateEngine(TEMPLATEDIR, DEVICECONFDIR)
    for fname in os.listdir(DEVICECONFDIR):
        from_templ_src, uri = temp_eng.process_config_from_fname(fname)
        src_eng = SourceEngine(SOURCE_ROOTDIR, from_templ_src, uri)
        src_eng.integrate()

if __name__ == '__main__':
    main()

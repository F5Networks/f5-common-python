# coding=utf-8
#
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

import os

from f5.bigip.mixins import AsmFileMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import PathElement
from f5.sdk_exception import FileMustNotHaveDotISOExtension


class File_Transfer(Collection):
    """BIG-IP® ASM File Transfer collection."""
    def __init__(self, tm):
        super(File_Transfer, self).__init__(tm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [
            Uploads,
            Downloads,
            ]


class Uploads(PathElement, AsmFileMixin):
    """A file upload resource."""
    def __init__(self, file_transfer):
        super(Uploads, self).__init__(file_transfer)
        self._meta_data['object_has_stats'] = False
        self.file_bound_uri = ''

    def upload_file(self, filepathname, **kwargs):
        filename = os.path.basename(filepathname)
        if os.path.splitext(filename)[-1] == '.iso':
            raise FileMustNotHaveDotISOExtension(filename)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._upload_file(filepathname, **kwargs)


class Downloads(PathElement, AsmFileMixin):
    """A file download resource."""
    def __init__(self, file_transfer):
        super(Downloads, self).__init__(file_transfer)
        self._meta_data['object_has_stats'] = False
        self.file_bound_uri = ''

    def download_file(self, filepathname):
        filename = os.path.basename(filepathname)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._download_file(filepathname)

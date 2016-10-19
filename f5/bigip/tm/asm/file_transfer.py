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
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import PathElement
from f5.sdk_exception import F5SDKError


class FileMustNotHaveDotISOExtension(F5SDKError):
    def __init__(self, filename):
        super(FileMustNotHaveDotISOExtension, self).__init__(filename)


class File_Transfer(OrganizingCollection):
    """BIG-IP® ASM Tasks organizing collection."""
    def __init__(self, tm):
        super(File_Transfer, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Uploads,
            Downloads,
            ]


class Uploads(PathElement, AsmFileMixin):
    """A file upload resource."""
    def __init__(self, file_transfer):
        super(Uploads, self).__init__(file_transfer)

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

    def download_file(self, filepathname):
        filename = os.path.basename(filepathname)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._download_file(filepathname)

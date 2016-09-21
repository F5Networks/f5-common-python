# coding=utf-8
#
"""Classes and functions for configuring BIG-IP"""
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

import os

from f5.bigip.mixins import FileUploadMixin
from f5.bigip.resource import PathElement
from f5.sdk_exception import F5SDKError


class FileMustNotHaveDotISOExtension(F5SDKError):
    def __init__(self, filename):
        super(FileMustNotHaveDotISOExtension, self).__init__(filename)


class File_Transfer(PathElement):
    """A PathElement for File_Transfer resources."""
    def __init__(self, shared):
        super(File_Transfer, self).__init__(shared)
        self._meta_data['allowed_lazy_attributes'] = [
            Uploads
        ]


class Uploads(PathElement, FileUploadMixin):
    """A file upload resource."""
    def __init__(self, file_transfer):
        super(Uploads, self).__init__(file_transfer)

    def upload_file(self, filepathname, **kwargs):
        filename = os.path.basename(filepathname)
        if os.path.splitext(filename)[-1] == '.iso':
            raise FileMustNotHaveDotISOExtension(filename)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._upload(filepathname, **kwargs)

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
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from f5.bigip.mixins import FileDownloadMixin
from f5.bigip.mixins import FileUploadMixin
from f5.bigip.resource import PathElement
from f5.sdk_exception import FileMustNotHaveDotISOExtension


class File_Transfer(PathElement):
    """A PathElement for File_Transfer resources."""
    def __init__(self, shared):
        super(File_Transfer, self).__init__(shared)
        self._meta_data['allowed_lazy_attributes'] = [
            Bulk,
            Madm,
            Uploads,
            Ucs_Uploads,
            Ucs_Downloads
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
        self._upload_file(filepathname, **kwargs)

    def upload_stringio(self, stringio, target, **kwargs):
        self.file_bound_uri = self._meta_data['uri'] + target
        self._upload(stringio, **kwargs)

    def upload_bytes(self, bytestring, target, **kwargs):
        self.file_bound_uri = self._meta_data['uri'] + target
        self._upload(StringIO(bytestring), **kwargs)


class Bulk(PathElement, FileUploadMixin, FileDownloadMixin):
    """A file upload resource."""
    def __init__(self, file_transfer):
        super(Bulk, self).__init__(file_transfer)
        self._meta_data['minimum_version'] = '13.0.0'

    def download_file(self, src, dest, **kwargs):
        filename = os.path.basename(src)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._download_file(src, dest, **kwargs)


class Madm(PathElement, FileDownloadMixin):
    """A file upload resource."""
    def __init__(self, file_transfer):
        super(Madm, self).__init__(file_transfer)

    def download_file(self, src, dest, **kwargs):
        filename = os.path.basename(src)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._download_file(src, dest, **kwargs)


class Ucs_Uploads(PathElement, FileUploadMixin):
    def __init__(self, file_transfer):
        super(Ucs_Uploads, self).__init__(file_transfer)

    def upload_file(self, filepathname, **kwargs):
        filename = os.path.basename(filepathname)
        if os.path.splitext(filename)[-1] == '.iso':
            raise FileMustNotHaveDotISOExtension(filename)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._upload_file(filepathname, **kwargs)

    def upload_bytes(self, bytestring, target, **kwargs):
        self.file_bound_uri = self._meta_data['uri'] + target
        self._upload(StringIO(bytestring), **kwargs)


class Ucs_Downloads(PathElement, FileDownloadMixin):
    def __init__(self, file_transfer):
        super(Ucs_Downloads, self).__init__(file_transfer)

    def download_file(self, src, dest, **kwargs):
        filename = os.path.basename(src)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._download_file(src, dest, **kwargs)

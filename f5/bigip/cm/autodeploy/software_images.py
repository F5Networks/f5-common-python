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

from f5.bigip.mixins import FileDownloadMixin
from f5.bigip.mixins import FileUploadMixin
from f5.bigip.resource import PathElement
from f5.sdk_exception import ImageFilesMustHaveDotISOExtension


class Software_Image_Uploads(PathElement, FileUploadMixin):
    """Software image upload resource."""
    def __init__(self, autodeploy):
        super(Software_Image_Uploads, self).__init__(autodeploy)
        self._meta_data['minimum_version'] = '12.0.0'

    def upload_image(self, filepathname, **kwargs):
        filename = os.path.basename(filepathname)
        if os.path.splitext(filename)[-1] != '.iso':
            raise ImageFilesMustHaveDotISOExtension(filename)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._upload_file(filepathname, **kwargs)


class Software_Image_Downloads(PathElement, FileDownloadMixin):
    """Software image download resource."""
    def __init__(self, autodeploy):
        super(Software_Image_Downloads, self).__init__(autodeploy)
        self._meta_data['minimum_version'] = '12.0.0'

    def download_image(self, src, dest, **kwargs):
        filename = os.path.basename(src)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._download_file(filename, dest, **kwargs)

    def download_file(self, src, dest, **kwargs):
        self.download_image(src, dest, **kwargs)

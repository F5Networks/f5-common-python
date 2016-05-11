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


class ImageFilesMustHaveDotISOExtension(F5SDKError):
    def __init__(self, filename):
        super(ImageFilesMustHaveDotISOExtension, self).__init__(filename)


class Software_Image_Uploads(PathElement, FileUploadMixin):
    """Software image upload resource."""
    def __init__(self, autodeploy):
        super(Software_Image_Uploads, self).__init__(autodeploy)

    def upload_image(self, filepathname, **kwargs):
        filename = os.path.basename(filepathname)
        if os.path.splitext(filename)[-1] != '.iso':
            raise ImageFilesMustHaveDotISOExtension(filename)
        self.file_bound_uri = self._meta_data['uri'] + filename
        self._upload(filepathname, **kwargs)
#
#
# class Software_Image_Downloads(PathElement):
#    """Software image download resource."""
#    def __init__(self, autodeploy):
#        super(Software_Image_Downloads, self).__init__(autodeploy)
#
#    def download_image(self, filepathname, **kwargs):
#        filename = os.path.basename(filepathname)
#        session = self._meta_data['icr_session']
#        chunk_size = kwargs.pop('chunk_size', 512 * 1024)
#        self.file_bound_uri = self._meta_data['uri'] + filename
#        with open(filepathname, 'wb') as writefh:
#            start = 0
#            end = chunk_size - 1
#            size = 0
#            current_bytes = 0
#
#            while True:
#                content_range = "%s-%s/%s" % (start, end, size)
#                headers = {'Content-Range': content_range,
#                           'Content-Type': 'application/octet-stream'}
#                req_params = {'headers': headers,
#                              'verify': False,
#                              'stream': True}
#                response = session.get(self.file_bound_uri,
#                                       requests_params=req_params)
#                if response.status_code == 200:
#                    # If the size is zero, then this is the first time through
#                    # the loop and we don't want to write data because we
#                    # haven't yet figured out the total size of the file.
#                    if size > 0:
#                        current_bytes += chunk_size
#                        for chunk in response.iter_content(chunk_size):
#                            writefh.write(chunk)
#
#                # Once we've downloaded the entire file, we can break out of
#                # the loop
#                if end == size:
#                    break
#
#                crange = response.headers['Content-Range']
#
#                #Determine the total number of bytes to read.
#                if size == 0:
#                    size = int(crange.split('/')[-1]) - 1
#
#                    # If the file is smaller than the chunk_size, the BigIP
#                    # will return an HTTP 400. Adjust the chunk_size down to
#                    # the total file size...
#                    if chunk_size > size:
#                        end = size
#
#                    # ...and pass on the rest of the code.
#                    continue
#
#                start += chunk_size
#
#                if (current_bytes + chunk_size) > size:
#                    end = size
#                else:
#                    end = start + chunk_size - 1

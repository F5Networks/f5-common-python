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


from f5.bigip.cm.autodeploy.software_images import Software_Image_Downloads
from f5.bigip.cm.autodeploy.software_images import Software_Image_Uploads
from f5.bigip.resource import OrganizingCollection


class Autodeploy(OrganizingCollection):
    """An organizing collection for Autodeploy resources."""
    def __init__(self, cm):
        super(Autodeploy, self).__init__(cm)
        self._meta_data['allowed_lazy_attributes'] = [
            Software_Image_Downloads,
            Software_Image_Uploads
        ]

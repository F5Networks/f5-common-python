# coding=utf-8
#
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

from f5.bigiq.resource import OrganizingCollection
from f5.bigiq.tm.sys import Sys


class Tm(OrganizingCollection):
    """An organizing collection for TM resources."""
    def __init__(self, bigiq):
        super(Tm, self).__init__(bigiq)
        self._meta_data['allowed_lazy_attributes'] = [
            Sys
        ]

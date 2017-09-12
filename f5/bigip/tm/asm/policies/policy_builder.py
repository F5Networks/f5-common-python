# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

from distutils.version import LooseVersion
from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedOperation


class Policy_Builder(UnnamedResource):
    """BIG-IP® ASM Policy Builder resource."""
    def __init__(self, policy):
        super(Policy_Builder, self).__init__(policy)
        tmos_v = self._meta_data['bigip'].tmos_version
        self._set_kind(tmos_v)

        self._meta_data['required_load_parameters'] = set()
        self._meta_data['object_has_stats'] = False

    def _set_kind(self, tmos_v):
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            self._meta_data['required_json_kind'] = 'tm:asm:policies:policy-builder:pbconfigstate'
        else:
            self._meta_data['required_json_kind'] = 'tm:asm:policies:policy-builder:policy-builderstate'

    def update(self, **kwargs):
        """Update is not supported for Policy Builder resource

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )

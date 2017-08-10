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
#

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import TaskResource
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedOperation


class Iapp(OrganizingCollection):
    def __init__(self, shared):
        super(Iapp, self).__init__(shared)
        self._meta_data['allowed_lazy_attributes'] = [
            Package_Management_Tasks_s
        ]


class Package_Management_Tasks_s(Collection):
    def __init__(self, iapp):
        super(Package_Management_Tasks_s, self).__init__(iapp)
        self._meta_data['object_has_stats'] = False
        self._meta_data['required_json_kind'] = \
            'shared:iapp:package-management-tasks:iapppackagemanagementcollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Package_Management_Task]
        self._meta_data['attribute_registry'] = {
            'shared:iapp:package-management-tasks:iapppackagemanagementtaskstate': Package_Management_Task  # NOQA
        }


class Package_Management_Task(TaskResource):
    def __init__(self, package_management_tasks):
        super(Package_Management_Task, self).__init__(package_management_tasks)
        self._meta_data['required_json_kind'] = \
            'shared:iapp:package-management-tasks:iapppackagemanagementtaskstate'  # NOQA
        self._meta_data['required_creation_parameters'] = {'operation'}

    def create(self, **kwargs):
        if 'operation' not in kwargs:
            error_message = "Missing required params: ['operation']"
            raise MissingRequiredCreationParameter(error_message)

        if kwargs['operation'] == 'INSTALL':
            if 'packageFilePath' not in kwargs:
                error_message = "Missing required params: ['packageFilePath']"
                raise MissingRequiredCreationParameter(error_message)
        return self._create(**kwargs)

    def update(self, **kwargs):
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )

    def cancel(self, **kwargs):
        self._cancel(**kwargs)

    def _cancel(self, **kwargs):
        params = dict(
            status='CANCEL_REQUESTED'
        )
        self.modify(**params)
        if self.status == 'CANCEL_REQUESTED':
            self.__dict__.update({'canceled': True})

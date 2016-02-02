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

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class FolderCollection(Collection):
    def __init__(self, sys):
        super(FolderCollection, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [Folder]
        self._meta_data['collection_registry'] =\
            {'tm:sys:folder:folderstate': Folder}


class Folder(Resource):
    def __init__(self, folder_collection):
        '''Create a folder resource object.

        Folder objects are the same as the partition so we need to deal with
        them slightly differently than other Resources.  For example when
        you refresh/load them you need to use the partition name instead of
        the partition and name because their self link looks something like
        `https://localhost/mgmt/tm/sys/folder/~testfolder`.  Notice that there
        is no ~partition~name format for the object.
        '''
        super(Folder, self).__init__(folder_collection)
        self._meta_data['allowed_lazy_attributes'] = []
        self._meta_data['required_json_kind'] = 'tm:sys:folder:folderstate'
        # refresh() and load() require partition, not name
        self._meta_data['required_refresh_parameters'] = set(('partition',))

    def load(self, **kwargs):
        '''Load the object using the partition name.

        We will pop the name out of kwargs and if there was no partition passed
        in set partition to name.  If the name is "/" we can ignore it
        because the root partition has no name.  It looks like:
        https://localhost/mgmt/tm/sys/folder/~
        '''
        name = kwargs.pop('name', '')
        partition = kwargs.pop('partition', '')
        if name and name != '/' and not partition:
            partition = name
        return self._load(partition=partition, **kwargs)

    def update(self, **kwargs):
        '''Update the object, removing device group if inherited

        If inheritedDevicegroup is the string "true" we need to remove
        deviceGroup from the args before we update or we get the
        following error:

        The floating traffic-group: /Common/traffic-group-1 can only be set on
        /testfolder if its device-group is inherited from the root folder
        '''
        inherit_device_group = self.__dict__.get('inheritedDevicegroup', False)
        if inherit_device_group == 'true':
            self.__dict__.pop('deviceGroup')
        return self._update(**kwargs)

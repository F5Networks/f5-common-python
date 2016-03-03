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

"""BigIP system folder (partition) module

REST URI
    ``http://localhost/mgmt/tm/sys/folder``

GUI Path
    ``System --> Users --> Partition List``

REST Kind
    ``tm:sys:folder:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Folders(Collection):
    """BigIP system folder collection.

    These are what we refer to as ``partition`` in the SDK.
    """
    def __init__(self, sys):
        super(Folders, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [Folder]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:folder:folderstate': Folder}


class Folder(Resource):
    def __init__(self, folder_s):
        '''BigIP system folder resource.

        Folder objects are the same as the partition so we need to deal with
        them slightly differently than other Resources.  For example when
        you refresh/load them you need to use the partition name instead of
        the partition and name because their self link looks something like
        `https://localhost/mgmt/tm/sys/folder/~testfolder`.  Notice that there
        is no ~partition~name format for the object.
        '''
        super(Folder, self).__init__(folder_s)
        self._meta_data['required_json_kind'] = 'tm:sys:folder:folderstate'
        # refresh() and load() require partition, not name
        self._meta_data['required_refresh_parameters'] = set()
        self._meta_data['required_creation_parameters'].update(('subPath',))

    def _load(self, **kwargs):
        name = kwargs.pop('name', '')
        partition = kwargs.pop('partition', '')
        read_session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['container']._meta_data['uri']

        if not name and not partition:
            # Root folder - https://localhost/mgmt/tm/sys/folder/~
            load_uri = base_uri + '~'
        elif not name and partition:
            # Top level - https://localhost/mgmt/tm/sys/folder/~partition
            load_uri = base_uri + '~' + partition
        elif name and not partition:
            # Top level - https://localhost/mgmt/tm/sys/folder/~partition
            load_uri = base_uri + '~' + name
        else:
            # Nested Folder (allow for name to be many folders)
            # https://localhost/mgmt/tm/sys/folder/~partition~f1~f2
            name = name.replace('/', '~')
            load_uri = base_uri + '~' + partition + '~' + name

        response = read_session.get(load_uri, uri_as_parts=False, **kwargs)
        self._local_update(response.json())
        self._activate_URI(self.selfLink)
        return self

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

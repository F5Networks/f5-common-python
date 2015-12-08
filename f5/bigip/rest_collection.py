"""BIG-IP API RESTInterfaceCollection """
# Copyright 2014 F5 Networks Inc.
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

import logging
import os

from f5.bigip import exceptions
from f5.common import constants as const
from f5.common.logger import Log
from requests.exceptions import HTTPError

OBJ_PREFIX = 'uuid_'

LOG = logging.getLogger(__name__)


def log(method):
    """Decorator helping to log method calls."""
    def wrapper(*args, **kwargs):
        """Necessary wrapper """
        instance = args[0]
        LOG.debug('%s::%s called with args: %s kwargs: %s',
                  instance.__class__.__name__,
                  method.__name__,
                  args[1:],
                  kwargs)
        return method(*args, **kwargs)
    return wrapper


class RESTInterfaceCollection(object):
    """Abstract base class for collection objects. """
    @log
    def delete(self, name=None, folder='Common',
               timeout=const.CONNECTION_TIMEOUT):
        """Delete the object """
        if not name:
            return False
        try:
            self.bigip.icr_session.delete(
                self.base_uri,
                folder=folder,
                instance_name=name,
                timeout=timeout)
        except HTTPError as exp:
            if exp.response.status_code == 404:
                return True
            else:
                raise
        return True

    def _delete(self, folder, name, timeout):
        try:
            self.bigip.icr_session.delete(self.base_uri, folder, name, timeout)
        except HTTPError as err:
            if (err.response.status_code == 400
                    and err.response.text.find('is referenced') > 0):
                Log.error('members', err.response.text)
            else:
                raise exceptions.PoolDeleteException(err.response.text)
        else:
            self._del_arp_and_fdb(name, folder)

    @log
    def delete_all(self, folder='Common', startswith="",
                   timeout=const.CONNECTION_TIMEOUT):
        """Delete all things that can start with a string.

        Used to use self.OBJ_PREFIX so now you have to pass it in.
        Maybe this isn't the best thing?

        We need to deal with the prefix in a better way
        """
        params = {
            '$select': 'name,selfLink',
            '$filter': 'partition eq ' + folder,
        }

        # This will raise if there is a HTTPError
        response = self.bigip.icr_session.get(
            self.base_uri, params=params, timeout=timeout)

        items = response.json().get('items', [])
        for item in items:
            # This is where we had startswith(self.OBJ_PREFIX)
            if item['name'].startswith(startswith):
                if not self.delete(item['name'], folder=folder):
                    return False
        return True

    @log
    def exists(self, name=None, folder='Common',
               timeout=const.CONNECTION_TIMEOUT):
        try:
            self.bigip.icr_session.get(
                self.base_uri, folder=folder, instance_name=name,
                params={'$select': 'name'}, timeout=timeout)
        except HTTPError as exp:
            if exp.response.status_code == 404:
                return False
            else:
                raise
        return True

    @log
    def _get_items(self, folder='Common', name='', suffix='/members',
                   select='name', timeout=const.CONNECTION_TIMEOUT, **kwargs):
        items = []
        params = {
            '$select': select,
            '$filter': 'partition eq ' + folder
        }
        try:
            response = self.bigip.icr_session.get(
                self.base_uri, folder, name, params=params,
                timeout=timeout, **kwargs)
        except HTTPError as exp:
            if exp.response.status_code == 404:
                return items
            raise

        items = response.json().get('items', [])
        if select:
            for item in items:
                if select in item:
                    items.append(strip_folder_and_prefix(item[select]))

        return items

    @log
    def _get_named_object(self, name, folder='Common', select='name',
                          timeout=const.CONNECTION_TIMEOUT):
        params = {
            '$select': select,
        }

        # No try here because original code was not doing exceptional things
        # with error messages like self._get()
        response = self.bigip.icr_session.get(self.base_uri,
                                              instance_name=name,
                                              folder=folder,
                                              params=params,
                                              timeout=timeout)
        return response.json().get(select, None)

    @log
    def _set_named_object(self, name, folder='Common', data=None,
                          timeout=const.CONNECTION_TIMEOUT):

        # No try -- let exceptions get raised up
        self.bigip.icr_session.put(self.base_uri, instance_name=name, folder=folder,
                                   data=data, timeout=timeout)

        return True


def prefixed(name):
    """Put object prefix in front of name """
    if not name.startswith(OBJ_PREFIX):
        name = OBJ_PREFIX + name
    return name


def icontrol_folder(method):
    """Returns the iControl folder + object name.

    If a kwarg name is 'name' or else ends in '_name'.

    The folder and the name will be prefixed with the global
    prefix OBJ_PREFIX. If preserve_vlan_name=True is an argument,
    then the 'vlan_name' argument will not be prefixed but the
    other matching arguments will.

    It also sets the iControl active folder to folder kwarg
    assuring get_list returns just the appopriate objects
    for the specific administrative partition. It does this
    for kwarg named 'name', ends in '_name', or 'named_address'.

    If the value in the name already includes '/Common/' the
    decoration honors that full path.
    """
    def wrapper(*args, **kwargs):
        """Necessary wrapper """
        instance = args[0]
        preserve_vlan_name = False
        if 'preserve_vlan_name' in kwargs:
            preserve_vlan_name = kwargs['preserve_vlan_name']
        if 'folder' in kwargs and kwargs['folder']:
            if kwargs['folder'].find('~') > -1:
                kwargs['folder'] = kwargs['folder'].replace('~', '/')
            kwargs['folder'] = os.path.basename(kwargs['folder'])
            if not kwargs['folder'] == 'Common':
                kwargs['folder'] = prefixed(kwargs['folder'])
            if 'name' in kwargs and kwargs['name']:
                if isinstance(kwargs['name'], basestring):
                    if kwargs['name'].find('~') > -1:
                        kwargs['name'] = kwargs['name'].replace('~', '/')
                    if kwargs['name'].startswith('/Common/'):
                        kwargs['name'] = os.path.basename(kwargs['name'])
                        kwargs['name'] = prefixed(kwargs['name'])
                        kwargs['name'] = instance.bigip.set_folder(
                            kwargs['name'], 'Common')
                    else:
                        kwargs['name'] = os.path.basename(kwargs['name'])
                        kwargs['name'] = prefixed(kwargs['name'])
                        kwargs['name'] = instance.bigip.set_folder(
                            kwargs['name'], kwargs['folder'])
            if 'named_address' in kwargs and kwargs['named_address']:
                if isinstance(kwargs['name'], basestring):
                    if kwargs['named_address'].find('~') > -1:
                        kwargs['named_address'] = \
                            kwargs['named_address'].replace('~', '/')
                    if kwargs['named_address'].startswith('/Common/'):
                        kwargs['named_address'] = \
                            os.path.basename(kwargs['named_address'])
                        kwargs['named_address'] = \
                            instance.bigip.set_folder(kwargs['named_address'],
                                                      'Common')
                    else:
                        kwargs['named_address'] = \
                            os.path.basename(kwargs['named_address'])
                        kwargs['named_address'] = \
                            instance.bigip.set_folder(kwargs['named_address'],
                                                      kwargs['folder'])
            for name in kwargs:
                if name.find('_folder') > 0 and kwargs[name]:
                    if kwargs[name].find('~') > -1:
                        kwargs[name] = kwargs[name].replace('~', '/')
                    kwargs[name] = os.path.basename(kwargs[name])
                    if not kwargs[name] == 'Common':
                        kwargs[name] = prefixed(kwargs[name])
                if name.find('_name') > 0 and kwargs[name]:
                    if isinstance(kwargs['name'], basestring):
                        if kwargs[name].find('~') > -1:
                            kwargs[name] = kwargs[name].replace('~', '/')
                        if kwargs[name].startswith('/Common/'):
                            kwargs[name] = os.path.basename(kwargs[name])
                            if name != 'vlan_name' or not preserve_vlan_name:
                                kwargs[name] = prefixed(kwargs[name])
                            kwargs[name] = instance.bigip.set_folder(
                                kwargs[name], 'Common')
                        else:
                            name_prefix = name[0:name.index('_name')]
                            specific_folder_name = name_prefix + "_folder"
                            folder = kwargs['folder']
                            if specific_folder_name in kwargs:
                                folder = kwargs[specific_folder_name]
                            kwargs[name] = os.path.basename(kwargs[name])
                            if name != 'vlan_name' or not preserve_vlan_name:
                                kwargs[name] = prefixed(kwargs[name])
                            kwargs[name] = instance.bigip.set_folder(
                                kwargs[name], folder)
            instance.bigip.set_folder(None, kwargs['folder'])
        return method(*args, **kwargs)
    return wrapper


def icontrol_rest_folder(method):
    """Returns iControl REST folder + object name.

    If a kwarg name is 'name' or else ends in '_name'.

    The folder and the name will be prefixed with the global
    prefix OBJ_PREFIX.
    """
    def wrapper(*args, **kwargs):
        """Necessary wrapper """
        preserve_vlan_name = False
        if 'preserve_vlan_name' in kwargs:
            preserve_vlan_name = kwargs['preserve_vlan_name']

        # Here we make sure the name or folder is not REST formatted,
        # which uses '~' instead of '/'. We change them back to '/'.
        # We normalize the object names to their base name (with no
        # / in the name at all) and then use a common prefix.
        if 'folder' in kwargs and kwargs['folder']:
            if kwargs['folder'] != '/' and kwargs['folder'].find('Common') < 0:
                temp = kwargs['folder'].replace('~', '/')
                kwargs['folder'] = prefixed(os.path.basename(temp))
        if 'name' in kwargs and kwargs['name']:
            if isinstance(kwargs['name'], basestring):
                temp = kwargs['name'].replace('~', '/')
                kwargs['name'] = prefixed(os.path.basename(temp))
            else:
                LOG.warn('attempting to normalize non basestring name. '
                         'Argument: val: ' + str(kwargs['name']))

        for name in kwargs:
            if name.find('_folder') > 0 and kwargs[name]:
                kwargs[name] = kwargs[name].replace('~', '/')
                kwargs[name] = os.path.basename(kwargs[name])
                if not kwargs[name] == 'Common':
                    kwargs[name] = prefixed(kwargs[name])
            if name.find('_name') > 0 and kwargs[name]:
                if isinstance(kwargs[name], basestring):
                    kwargs[name] = kwargs[name].replace('~', '/')
                    kwargs[name] = os.path.basename(kwargs[name])
                    if name != 'vlan_name' or not preserve_vlan_name:
                        kwargs[name] = prefixed(kwargs[name])
                else:
                    LOG.warn('attempting to normalize non basestring name. '
                             ' Argument: name: ' + str(name) +
                             ' val:' + str(kwargs[name]))
        return method(*args, **kwargs)
    return wrapper


def decorate_name(name=None, folder='Common', use_prefix=True):
    """Add "namespace" prefix to names """
    folder = os.path.basename(folder)
    if not folder == 'Common':
        folder = prefixed(folder)
    if name.startswith('/Common/'):
        name = os.path.basename(name)
        if use_prefix:
            name = prefixed(name)
        name = '/Common/' + name
    else:
        name = os.path.basename(name)
        if use_prefix:
            name = prefixed(name)
        name = '/' + folder + '/' + name
    return name


def strip_folder_and_prefix(path):
    """Strip folder and prefix """
    if isinstance(path, list):
        for i in range(len(path)):
            if path[i].find('~') > -1:
                path[i] = path[i].replace('~', '/')
            if path[i].startswith('/Common'):
                path[i] = path[i].replace(OBJ_PREFIX, '')
            else:
                path[i] = \
                    os.path.basename(str(path[i])).replace(OBJ_PREFIX, '')
        return path
    else:
        if path.find('~') > -1:
            path = path.replace('~', '/')
        if path.startswith('/Common'):
            return str(path).replace(OBJ_PREFIX, '')
        else:
            return os.path.basename(str(path)).replace(OBJ_PREFIX, '')


def strip_domain_address(ip_address):
    """Strip domain from ip address """
    mask_index = ip_address.find('/')
    if mask_index > 0:
        return ip_address[:mask_index].split('%')[0] + ip_address[mask_index:]
    else:
        return ip_address.split('%')[0]


def split_addr_port(dest):
    if len(dest.split(':')) > 2:
        # ipv6: bigip syntax is addr.port
        parts = dest.split('.')
    else:
        # ipv4: bigip syntax is addr:port
        parts = dest.split(':')
    return (parts[0], parts[1])

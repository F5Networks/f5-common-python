# Copyright 2016 F5 Networks Inc.

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
#

from f5.utils.decorators import poll_for_exceptionless_callable


def pollster(callable):
    '''Wraps the poll to get attempts and interval applicable for cluster.

    :param callable: callable -- callable to pass into poll
    '''

    return poll_for_exceptionless_callable(callable, 20, 2)


def get_device_info(bigip):
    '''Get device information about a specific BigIP device.

    :param bigip: ManagementRoot object --- device to inspect
    :returns: ManagementRoot object
    '''

    coll = pollster(bigip.tm.cm.devices.get_collection)()
    device = [device for device in coll if device.selfDevice == 'true']
    assert len(device) == 1
    return device[0]


def get_device_names_to_objects(devices):
    '''Map a list of devices to their hostnames.

    :param devices: list -- list of ManagementRoot objects
    :returns: dict -- mapping of hostnames to ManagementRoot objects
    '''

    name_to_object = {}
    for device in devices:
        device_name = get_device_info(device).name
        name_to_object[device_name] = device
    return name_to_object

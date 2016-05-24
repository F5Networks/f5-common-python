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

'''These exceptions for clustering, devicegroup, and trustdomain.'''

from f5.sdk_exception import F5SDKError


class ClusterError(F5SDKError):
    def __init__(self, *args, **kwargs):
        super(ClusterError, self).__init__(*args, **kwargs)


class DeviceGroupError(F5SDKError):
    pass


class TrustDomainError(F5SDKError):
    pass


class AlreadyManagingCluster(ClusterError):
    pass


class ClusterNotSupported(ClusterError):
    pass


class ClusterOperationNotSupported(ClusterError):
    pass


class DeviceAlreadyInTrustDomain(TrustDomainError):
    pass


class MissingRequiredDeviceGroupParameter(ClusterError):
    pass


class NoClusterToManage(ClusterError):
    pass


class DeviceGroupNotSupported(DeviceGroupError):
    pass


class DeviceGroupOperationNotSupported(DeviceGroupError):
    pass


class DeviceNotTrusted(TrustDomainError):
    pass


class TrusteeNotInTrustDomain(TrustDomainError):
    pass


class UnexpectedDeviceGroupState(DeviceGroupError):
    pass


class UnexpectedDeviceGroupDevices(DeviceGroupError):
    pass


class UnexpectedDeviceGroupType(DeviceGroupError):
    pass

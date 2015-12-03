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


class BigIPException(Exception):
    pass


class MinorVersionValidateFailed(BigIPException):
    pass


class MajorVersionValidateFailed(BigIPException):
    pass


class ProvisioningExtraMBValidateFailed(BigIPException):
    pass


class BigIPDeviceLockAcquireFailed(BigIPException):
    pass


class BigIPClusterInvalidHA(BigIPException):
    pass


class BigIPClusterSyncFailure(BigIPException):
    pass


class BigIPClusterPeerAddFailure(BigIPException):
    pass


class BigIPClusterConfigSaveFailure(BigIPException):
    pass


class UnknownMonitorType(BigIPException):
    pass


class MissingVTEPAddress(BigIPException):
    pass


class MissingNetwork(BigIPException):
    pass


class InvalidNetworkType(BigIPException):
    pass


class StaticARPCreationException(BigIPException):
    pass


class StaticARPQueryException(BigIPException):
    pass


class StaticARPDeleteException(BigIPException):
    pass


class ClusterCreationException(BigIPException):
    pass


class ClusterUpdateException(BigIPException):
    pass


class ClusterQueryException(BigIPException):
    pass


class ClusterDeleteException(BigIPException):
    pass


class DeviceCreationException(BigIPException):
    pass


class DeviceUpdateException(BigIPException):
    pass


class DeviceQueryException(BigIPException):
    pass


class DeviceDeleteException(BigIPException):
    pass


class InterfaceQueryException(BigIPException):
    pass


class IAppCreationException(BigIPException):
    pass


class IAppQueryException(BigIPException):
    pass


class IAppUpdateException(BigIPException):
    pass


class IAppDeleteException(BigIPException):
    pass


class L2GRETunnelCreationException(BigIPException):
    pass


class L2GRETunnelQueryException(BigIPException):
    pass


class L2GRETunnelUpdateException(BigIPException):
    pass


class L2GRETunnelDeleteException(BigIPException):
    pass


class MonitorCreationException(BigIPException):
    pass


class MonitorQueryException(BigIPException):
    pass


class MonitorUpdateException(BigIPException):
    pass


class MonitorDeleteException(BigIPException):
    pass


class NATCreationException(BigIPException):
    pass


class NATQueryException(BigIPException):
    pass


class NATUpdateException(BigIPException):
    pass


class NATDeleteException(BigIPException):
    pass


class PoolCreationException(BigIPException):
    pass


class PoolQueryException(BigIPException):
    pass


class PoolUpdateException(BigIPException):
    pass


class PoolDeleteException(BigIPException):
    pass


class RouteCreationException(BigIPException):
    pass


class RouteQueryException(BigIPException):
    pass


class RouteUpdateException(BigIPException):
    pass


class RouteDeleteException(BigIPException):
    pass


class RuleCreationException(BigIPException):
    pass


class RuleQueryException(BigIPException):
    pass


class RuleUpdateException(BigIPException):
    pass


class RuleDeleteException(BigIPException):
    pass


class SelfIPCreationException(BigIPException):
    pass


class SelfIPQueryException(BigIPException):
    pass


class SelfIPUpdateException(BigIPException):
    pass


class SelfIPDeleteException(BigIPException):
    pass


class SNATCreationException(BigIPException):
    pass


class SNATQueryException(BigIPException):
    pass


class SNATUpdateException(BigIPException):
    pass


class SNATDeleteException(BigIPException):
    pass


class SystemCreationException(BigIPException):
    pass


class SystemQueryException(BigIPException):
    pass


class SystemUpdateException(BigIPException):
    pass


class SystemDeleteException(BigIPException):
    pass


class VirtualServerCreationException(BigIPException):
    pass


class VirtualServerQueryException(BigIPException):
    pass


class VirtualServerUpdateException(BigIPException):
    pass


class VirtualServerDeleteException(BigIPException):
    pass


class VLANCreationException(BigIPException):
    pass


class VLANQueryException(BigIPException):
    pass


class VLANUpdateException(BigIPException):
    pass


class VLANDeleteException(BigIPException):
    pass


class VXLANCreationException(BigIPException):
    pass


class VXLANQueryException(BigIPException):
    pass


class VXLANUpdateException(BigIPException):
    pass


class VXLANDeleteException(BigIPException):
    pass

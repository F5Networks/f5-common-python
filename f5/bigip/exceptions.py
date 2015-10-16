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


class MinorVersionValidateFailed(Exception):
    pass


class MajorVersionValidateFailed(Exception):
    pass


class ProvisioningExtraMBValidateFailed(Exception):
    pass


class BigIPDeviceLockAcquireFailed(Exception):
    pass


class BigIPClusterInvalidHA(Exception):
    pass


class BigIPClusterSyncFailure(Exception):
    pass


class BigIPClusterPeerAddFailure(Exception):
    pass


class BigIPClusterConfigSaveFailure(Exception):
    pass


class UnknownMonitorType(Exception):
    pass


class MissingVTEPAddress(Exception):
    pass


class MissingNetwork(Exception):
    pass


class InvalidNetworkType(Exception):
    pass


class StaticARPCreationException(Exception):
    pass


class StaticARPQueryException(Exception):
    pass


class StaticARPDeleteException(Exception):
    pass


class ClusterCreationException(Exception):
    pass


class ClusterUpdateException(Exception):
    pass


class ClusterQueryException(Exception):
    pass


class ClusterDeleteException(Exception):
    pass


class DeviceCreationException(Exception):
    pass


class DeviceUpdateException(Exception):
    pass


class DeviceQueryException(Exception):
    pass


class DeviceDeleteException(Exception):
    pass


class InterfaceQueryException(Exception):
    pass


class IAppCreationException(Exception):
    pass


class IAppQueryException(Exception):
    pass


class IAppUpdateException(Exception):
    pass


class IAppDeleteException(Exception):
    pass


class L2GRETunnelCreationException(Exception):
    pass


class L2GRETunnelQueryException(Exception):
    pass


class L2GRETunnelUpdateException(Exception):
    pass


class L2GRETunnelDeleteException(Exception):
    pass


class MonitorCreationException(Exception):
    pass


class MonitorQueryException(Exception):
    pass


class MonitorUpdateException(Exception):
    pass


class MonitorDeleteException(Exception):
    pass


class NATCreationException(Exception):
    pass


class NATQueryException(Exception):
    pass


class NATUpdateException(Exception):
    pass


class NATDeleteException(Exception):
    pass


class PoolCreationException(Exception):
    pass


class PoolQueryException(Exception):
    pass


class PoolUpdateException(Exception):
    pass


class PoolDeleteException(Exception):
    pass


class RouteCreationException(Exception):
    pass


class RouteQueryException(Exception):
    pass


class RouteUpdateException(Exception):
    pass


class RouteDeleteException(Exception):
    pass


class RuleCreationException(Exception):
    pass


class RuleQueryException(Exception):
    pass


class RuleUpdateException(Exception):
    pass


class RuleDeleteException(Exception):
    pass


class SelfIPCreationException(Exception):
    pass


class SelfIPQueryException(Exception):
    pass


class SelfIPUpdateException(Exception):
    pass


class SelfIPDeleteException(Exception):
    pass


class SNATCreationException(Exception):
    pass


class SNATQueryException(Exception):
    pass


class SNATUpdateException(Exception):
    pass


class SNATDeleteException(Exception):
    pass


class SystemCreationException(Exception):
    pass


class SystemQueryException(Exception):
    pass


class SystemUpdateException(Exception):
    pass


class SystemDeleteException(Exception):
    pass


class VirtualServerCreationException(Exception):
    pass


class VirtualServerQueryException(Exception):
    pass


class VirtualServerUpdateException(Exception):
    pass


class VirtualServerDeleteException(Exception):
    pass


class VLANCreationException(Exception):
    pass


class VLANQueryException(Exception):
    pass


class VLANUpdateException(Exception):
    pass


class VLANDeleteException(Exception):
    pass


class VXLANCreationException(Exception):
    pass


class VXLANQueryException(Exception):
    pass


class VXLANUpdateException(Exception):
    pass


class VXLANDeleteException(Exception):
    pass

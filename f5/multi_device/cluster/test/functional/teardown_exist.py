from f5.bigip import ManagementRoot
from f5.cluster.cluster_manager import ClusterManager

a = ManagementRoot('10.190.20.202', 'admin', 'admin')
b = ManagementRoot('10.190.20.203', 'admin', 'admin')
c = ManagementRoot('10.190.20.204', 'admin', 'admin')

cm = ClusterManager([a, b], 'testing_cluster', 'Common', 'sync-failover')

cm.teardown_cluster()

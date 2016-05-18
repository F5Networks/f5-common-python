from f5.bigip import BigIP
from f5.cluster.cluster_manager import ClusterManager

a = BigIP('10.190.20.202', 'admin', 'admin')
b = BigIP('10.190.20.203', 'admin', 'admin')
c = BigIP('10.190.20.204', 'admin', 'admin')

cm = ClusterManager([a, b], 'testing_cluster', 'Common', 'sync-failover')

cm.teardown_cluster()

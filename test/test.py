import gettext
gettext.install('test')

from oslo.config import cfg
from neutron.plugins.common import constants as plugin_const
from neutron.services.loadbalancer.drivers.f5.bigip.icontrol_driver \
    import iControlDriver, OPTS as icontrol_OPTS

conf = cfg.CONF
conf.register_opts(icontrol_OPTS)

conf.icontrol_hostname = '10.144.64.93,10.144.64.94'
conf.f5_external_physical_mappings = ["default:1.3:True"]
conf.icontrol_config_mode = 'object'

# These should be registered using OPTS in the agent_manager
# but we would rather not import the agent_manager because of
# the class dependencies.
conf.use_namespaces = True
conf.f5_global_routed_mode = False

driver = iControlDriver(conf, False)

service = {'pool': {'id': 'pool_id_1',
                    'status': plugin_const.PENDING_CREATE,
                    'tenant_id': '45d34b03a8f24465a5ad613436deb773'},

           'members': [{'id': 'member_id_1',
                        'status': plugin_const.PENDING_CREATE,
                        'address': '10.10.1.2',
                        'network': {'id': 'net_id_1', 'shared': False},
                        'protocol_port': "80"},

                       {'id': 'member_id_2',
                        'status': plugin_const.PENDING_CREATE,
                        'address': '10.10.1.4',
                        'network': {'id': 'net_id_1', 'shared': False},
                        'protocol_port': "80"}],

           'vip': {'id': 'vip_id_1',
                   'status': plugin_const.PENDING_CREATE,
                   'address': '10.20.1.99',
                   'network': {'id': 'net_id_1', 'shared': False}}}

driver.network_builder.update_rds_cache('3b50e6c7e62945188157dba2723a4890')
driver.network_builder.update_rds_cache('b0347fb9718241f1949f5d350ce55527')
driver.network_builder.update_rds_cache('f8e350caeb8d49f580cb1ef31bd7acd2')

network = {
    "provider:network_type" : "gre",
    "shared" : False,
    "router:external" : False,
    "id" : "dd4f1a05-bd25-4b98-a39e-9a94fdf37a15",
    "tenant_id" : "92162123f3ea4a7ebff7ce8175a28774",
    "name" : "proj_1_net_1_internal",
    "subnets" : [
       "6a431d13-8c6c-4bcb-96a0-a6feca5dc7d8"
    ],
    "provider:physical_network" : None,
    "status" : "ACTIVE",
    "admin_state_up" : True,
    "provider:segmentation_id" : 99
}
subnet = {
    "ip_version" : 4,
    "cidr" : "10.10.3.0/24",
    "name" : "proj_1_sub_1_internal",
    "host_routes" : [],
    "network_id" : "dd4f1a05-bd25-4b98-a39e-9a94fdf37a15",
    "tenant_id" : "92162123f3ea4a7ebff7ce8175a28774",
    "enable_dhcp" : True,
    "dns_nameservers" : [],
    "ipv6_ra_mode" : None,
    "ipv6_address_mode" : None,
    "allocation_pools" : [
       {  
          "end" : "10.10.1.254",
          "start" : "10.10.1.2"
       }
    ],
    "gateway_ip" : "10.10.1.1",
    "shared" : False,
    "id" : "6a431d13-8c6c-4bcb-96a0-a6feca5dc7d8"
}

tenant_id = 'f8e350caeb8d49f580cb1ef31bd7acd2'

driver.conf.max_namespaces_per_tenant=2
driver.network_builder.assign_route_domain(tenant_id, network, subnet)
#driver.sync(service)


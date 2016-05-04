from f5.common.iapp_parser import IappParser as ip

hi = open('/Users/breaux/Documents/f5-openstack-heat-plugins/f5_heat/examples/iapps/hitesh.tmpl').read()

d = ip(hi).parse_template()
import json
print json.dumps(d)

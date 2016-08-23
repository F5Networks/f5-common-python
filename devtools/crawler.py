from __future__ import absolute_import
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

from f5.devtools.code_generator import DEVICECONFDIR

import json
import os

from pprint import pprint as pp
from urlparse import urlparse


class OCCrawler(object):
    def __init__(self, bigip, OC_path_element):
        self.bigip = bigip
        self.session = self.bigip._meta_data[u"icr_session"]
        self.uri = self.bigip._meta_data['uri'] + OC_path_element
        self.configs = [self.session.get(self.uri).json()]
        self.build_referenced_uris()

    def _get_uri_from_OC_item(self, item):
        if u"reference" in item and u"link" in item[u"reference"]:
            return item[u"reference"][u"link"]\
                .replace("localhost",
                         self.bigip._meta_data[u"hostname"])

    def build_referenced_uris(self):
        self.referenced = []
        for item in self.configs[0][u"items"]:
            self.referenced.append(self._get_uri_from_OC_item(item))

    def get_referenced_configs(self):
        for uri in self.referenced:
            self.configs.append(self.session.get(uri).json())


class ConfigWriter(object):
    def __init__(self, config_list, complete_oc_name):
        self.oc_name = complete_oc_name
        self.oc_basename = self.oc_name.split('/')[-1]
        self.configs = config_list

    def _get_fname(self, conf):
        sl = conf[u"selfLink"]
        scheme, netloc, path, params, qargs, frags = urlparse(sl)
        ps = path.split('/')
        if ps[-1] == self.oc_basename:
            return self.oc_basename + '_GET'
        else:
            return self.oc_basename + '_' + ps[-1] + '_GET'

    def dump_configs(self):
        for conf in self.configs:
            fname = self._get_fname(conf)
            if not os.path.exists(os.path.join(DEVICECONFDIR, fname)):
                outname = os.path.join(DEVICECONFDIR, fname) + ".json"
                with open(outname, 'w') as fh:
                    json.dump(conf, fh)


def main():
    from f5.bigip import BigIP
    b = BigIP('10.190.5.7', 'admin', 'admin')
    occrawler = OCCrawler(b, 'ltm/persistence')
    pp(occrawler.referenced)
    occrawler.get_referenced_configs()
    pp(occrawler.configs)
    config_writer = ConfigWriter(occrawler.configs, u"ltm/persistence")
    config_writer.dump_configs()

if __name__ == '__main__':
    main()

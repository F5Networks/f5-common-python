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

import io
import jinja2
import json
from pprint import pprint as pp
import re

import os

UTILSDIR = os.path.abspath(os.path.dirname(__file__))
COMMONPREFIX = os.path.dirname(UTILSDIR)
SOURCE_ROOTDIR = os.path.join(COMMONPREFIX, 'f5', 'bigip')
TEMPLATEDIR = os.path.join(UTILSDIR, 'template_library')
DEVICECONFDIR = os.path.join(UTILSDIR, 'device_configs')


class UnexpectedOCItem(Exception):
    pass


class Kindless(Exception):
    pass


class TemplateEngine(object):
    '''Instantiate this to handle generating Python from JSON

    Currently supports generation of OrganizingCollection, and
    Collection, strings.  Also produces most of Resource classes.
    '''
    def __init__(self, template_dir, config_dir):
        self.OC_pattern =\
            r'tm:(?P<OrgColl>\w+):(?P=OrgColl)collectionstate'
        # Initialize templates
        self.templates = {}
        self._consume_directory(template_dir, self._template_consumer)
        self.license_template = self.templates['license']
        self.import_template = self.templates['imports']

        # Initialize configs
        self.raw_configs = {}
        self.formatted_configs = {}
        self._consume_directory(config_dir, self._config_consumer)

    def _template_consumer(self, STUB, dirname, fnames):
        for fname in fnames:
            if fname.endswith('.tmpl'):
                with io.open(os.path.join(dirname, fname)) as fh:
                    templatekey = fname[:-len('.tmpl')]
                    self.templates[templatekey] = jinja2.Template(fh.read())

    def _config_consumer(self, STUB, dirname, fnames):
        for fname in fnames:
            if fname.endswith('.json'):
                with io.open(os.path.join(dirname, fname)) as fh:
                    configkey = fname[:-len('.json')]
                    self.raw_configs[configkey] = json.load(fh)

    def _consume_directory(self, dirname, consumer):
        os.path.walk(dirname, consumer, self)

    def list_templates(self):
        pp(self.templates.keys())

    def list_raw_configs(self):
        pp(self.raw_configs.keys())

    def process_config(self, config_name):
        try:
            raw_conf = self.raw_configs[config_name]
        except KeyError as ex:
            error_message = "Expected file named %r.json to exist in"\
                            " directory %r" % (config_name, DEVICECONFDIR)
            print(error_message)
            raise ex
        if 'kind' in raw_conf:
            python_as_string = self._process_config_with_kind(raw_conf)
        else:
            raise Kindless(raw_conf)
        return python_as_string

    def _handle_dashes_dots_capitals(self, raw_klass):
        temp_string = '_'.join([x.capitalize() for x in raw_klass.split('-')])
        KlassName = '_'.join([x.capitalize() for x in temp_string.split('.')])
        return KlassName

    def _build_orgcoll_import_dicts(self, raw_conf, klass):
        imports = []
        selfLinkstart = raw_conf[u"selfLink"].partition("?")[0]
        items = raw_conf[u"items"]
        for item in items:
            if item[u"reference"][u"link"].startswith(selfLinkstart):
                tempuri = item[u"reference"][u"link"]
                pre_questionmark = tempuri.partition("?")[0]
                post_selfLink = pre_questionmark[len(selfLinkstart)+1:]
                KlassName = self._handle_dashes_dots_capitals(post_selfLink)
                imports.append({'OC': '.'+klass.lower(),
                                'module': '.'+KlassName.lower(),
                                'klass': KlassName})
            else:
                raise UnexpectedOCItem(item)
        return imports

    def _format_org_collection(self, org_match, kind, raw_conf):
        KlassName =\
            self._handle_dashes_dots_capitals(org_match.group('OrgColl'))
        OC_template = self.templates['OrganizingCollection']
        import_dicts = self._build_orgcoll_import_dicts(raw_conf, KlassName)
        config_dict = {'klass': KlassName,
                       'kind': kind,
                       'import_dicts': import_dicts}
        OrgCollstr = OC_template.render(**config_dict)
        imports_as_str = self.import_template.render(import_dicts=import_dicts)
        imps_as_list = imports_as_str.split('\n')
        imps_as_list.append(
            'from f5.bigip.resource import OrganizingCollection')
        imps_as_list.sort()
        imports = '\n'.join(imps_as_list)
        python_as_string = self.license_template.render()+imports+OrgCollstr
        self.formatted_configs = {KlassName: {'Python_str': python_as_string,
                                              'config_dict': config_dict,
                                              'import_dicts': import_dicts}}
        return python_as_string

    def _build_CollectionName_from_KlassName(self, KlassName):
        if KlassName.endswith('s'):
            CollectionName = KlassName+'_s'
        else:
            CollectionName = KlassName+'s'
        return CollectionName

    def _format_resource(self, kind, raw_conf):
        raw_string = kind.split(':')[-1][:-len('state')]
        assert raw_string == kind.split(':')[-2]
        KlassName = self._handle_dashes_dots_capitals(raw_string)
        container = self._build_CollectionName_from_KlassName(KlassName)
        template = self.templates['Resource']
        python_as_string = template.render(container=container,
                                           klass=KlassName,
                                           kind=kind,
                                           attr_reg_dict={})
        return python_as_string

    def _format_collection(self, kind, raw_conf):
        raw_string = kind.split(':')[-1][:-len('collectionstate')]
        KlassName = self._handle_dashes_dots_capitals(raw_string)
        CollKlassName = self._build_CollectionName_from_KlassName(KlassName)
        member_klass = KlassName
        collection_template = self.templates['Collection']
        memberkind = kind.replace('collection', '')
        config_dict = {'coll_klass': CollKlassName,
                       'member_klass': member_klass,
                       'collection_container': kind.split(':')[-3],
                       'collection_attr_reg_dict': {memberkind: member_klass}}
        import_str = 'from f5.bigip.resource import Collection'
        Collstr = collection_template.render(**config_dict)
        python_as_string = import_str + Collstr
        return python_as_string

    def _format_stats(self, kind, raw_conf):
        klass = kind.split(':')[-1][:-len('stats')]
        print(klass)
        template = self.templates['Stats']
        print(template)
        # XXX
        # return python_as_string

    def _process_config_with_kind(self, raw_conf):
        kind = raw_conf[u"kind"]
        org_match = re.match(self.OC_pattern, kind)
        if org_match:
            return self._format_org_collection(org_match, kind, raw_conf)
        elif 'collectionstate' in kind:
            return self._format_collection(kind, raw_conf)
        elif kind.endswith('stats'):
            return self._format_stats(kind, raw_conf)
        elif kind.endswith('state'):
            return self._format_resource(kind, raw_conf)


def main():
    temp_eng = TemplateEngine(TEMPLATEDIR, DEVICECONFDIR)
    ltm_create_pool = temp_eng.process_config('create_pool_response')
    print(ltm_create_pool)


if __name__ == '__main__':
    main()

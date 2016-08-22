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

'''Source engine container, combines code on filesystem with other sources.'''
from __future__ import print_function

LICENSE_AND_MODULE_DOCSTRING = """# Copyright 2016 F5 Networks Inc.
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
"""
import ast
import io
import os
from urlparse import urlparse


class UnexpectedNodeInFromImports(Exception):
    '''If a nonstring, nonimport is found before imports end raise this.'''
    pass


class SourceEngine(object):
    '''Given a Python source string, and a uri, integrate with modules

    Defines filesystem paths from the uri
    Checks for module based on path
    If no module dump string and done
    If module read in as string
    check class names, if they exist, skip
    Else:
        Handle import integration (additive)
    Append new class
    '''
    def __init__(self, source_root_dir, templ_src_str, selfLinkURI):
        # find/read source from module
        self.root_dir = source_root_dir
        self.module_path = self._build_path_from_URI(selfLinkURI)
        self.src_from_module = self._read_module_source(self.module_path)

        # parse_and_store module source
        self._parse_and_store_src('module', self.src_from_module)

        # parse and store template source
        self.src_from_template = templ_src_str
        self._parse_and_store_src('template', self.src_from_template)

    def _build_path_from_URI(self, selfLinkURI):
        _, _, uri_path, _, _, _ = urlparse(selfLinkURI)
        splits = uri_path.split('/')
        self.org_coll_dir = splits[3]
        if len(splits) > 4:
            self.module_name = splits[4] + '.py'
        else:
            self.module_name = '__init__.py'
        return os.path.join(self.root_dir, self.org_coll_dir, self.module_name)

    def _read_module_source(self, pathname):
        if os.path.isfile(pathname):
            with io.open(pathname, 'r') as fh:
                return fh.read()
        else:
            if not os.path.isdir(os.path.dirname(pathname)):
                os.makedirs(os.path.dirname(pathname))
            return ''

    def _get_ClassDefs(self, target_ast, found):
        for node in ast.walk(target_ast):
            if isinstance(node, ast.ClassDef):
                found[node.name] = node

    def _get_ImportFroms(self, target_ast, found):
        line_numbers = []
        for node in ast.walk(target_ast):
            if isinstance(node, ast.ImportFrom):
                line_numbers.append(node.lineno)
                fullname = 'from ' + node.module + ' import ' +\
                    node.names[0].name
                found[fullname] = node
        if not line_numbers:
            line_numbers.append(-1)
        found['start'] = min(line_numbers)
        found['end'] = max(line_numbers)
        # check for unexpected expressions in ImportFroms block
        for node in ast.walk(target_ast):
            if (getattr(node, 'lineno', False)):
                if node.lineno <= found['end']:
                    if (not isinstance(node, ast.ImportFrom)) and\
                       (not isinstance(node, ast.Str)) and\
                       (not isinstance(node, ast.Expr)):
                        raise UnexpectedNodeInFromImports(node)

    def _parse_and_store_src(self, src_type, src_string):
        print(src_string)
        setattr(self, 'src_from_'+src_type, src_string)
        setattr(self, src_type+'_ast', ast.parse(src_string))
        setattr(self, src_type+'_classdefs', {})
        self._get_ClassDefs(getattr(self, src_type+'_ast'),
                            getattr(self, src_type+'_classdefs'))
        setattr(self, src_type+'_fromimports', {})
        self._get_ImportFroms(getattr(self, src_type+'_ast'),
                              getattr(self, src_type+'_fromimports'))

    def _integrate_importfroms(self):
        start_ind = self.module_fromimports['start']
        end_ind = self.module_fromimports['end']
        fis_to_add = []
        for fromimport in self.template_fromimports:
            if fromimport not in self.module_fromimports:
                fis_to_add.append(fromimport)
        mod_fimport_lines = self.src_from_module_lines[start_ind-1:end_ind]
        mod_fimport_lines.extend(fis_to_add)
        mod_fimport_lines.sort()
        return mod_fimport_lines

    def _clean_template_string(self):
        ftl_raw = self.src_from_template.strip().splitlines()[
            self.template_fromimports['end']:]
        from_template_lines =\
            os.linesep.join(ftl_raw).strip().split(os.linesep)
        from_template_lines[-1] = from_template_lines[-1] + os.linesep
        from_template_lines.insert(0, os.linesep)
        return os.linesep.join(from_template_lines)

    def integrate(self):
        if not os.path.isfile(self.module_path):
            to_mod_string =\
                LICENSE_AND_MODULE_DOCSTRING + self.src_from_template
            with io.open(self.module_path, 'wb') as ofh:
                ofh.write(to_mod_string)
                return
        for key in self.template_classdefs:
            if key in self.module_classdefs:
                print('class: %r already defined!' % key)
                return
        self.src_from_module_lines = self.src_from_module.strip().splitlines()
        importfips_lines = self._integrate_importfroms()
        preamble_lines =\
            self.src_from_module_lines[:self.module_fromimports['start']-1]
        post_imp_lines =\
            self.src_from_module_lines[self.module_fromimports['end']:]
        post_imp_lines[-1] = post_imp_lines[-1]+os.linesep
        preamble_lines.extend(importfips_lines)
        preamble_lines.extend(post_imp_lines)
        module_src = os.linesep.join(preamble_lines)
        new_module_src = module_src + self._clean_template_string()
        os.rename(self.module_path, self.module_path+'.old')
        with io.open(self.module_path, 'wb') as ofh:
            ofh.write(new_module_src)

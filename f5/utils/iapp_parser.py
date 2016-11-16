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

import re

from f5.sdk_exception import F5SDKError


class IappParser(object):

    template_sections = [
        'presentation',
        'implementation',
        'html-help',
        'role-acl'
    ]

    tcl_list_for_attr_re = '{(\s*(\w+)?\s*)+}'
    tcl_list_for_section_re = '(\s*\w+\s*)+'
    section_map = {
        'html-help': 'htmlHelp',
        'role-acl': 'roleAcl'
    }
    attr_map = {
        'requires-modules': 'requiresModules',
        'ignore-verification': 'ignoreVerification',
        'tmpl-signature': 'tmplSignature',
        'requires-bigip-version-min': 'requiresBigipVersionMin',
        'requires-bigip-version-max': 'requiresBigipVersionMax',
        'total-signing-status': 'totalSigningStatus',
        'prerequisite-errors': 'prerequisiteErrors',
        'verification-status': 'verificationStatus',
        'signing-key': 'signingKey',
        'tmpl-checksum': 'tmplChecksum'
    }
    sections_not_required = ['html-help', 'role-acl', 'macro']
    tcl_list_patterns = {
        'requires-modules': tcl_list_for_attr_re,
        'role-acl': tcl_list_for_section_re
    }
    template_attrs = [
        'description',
        'partition',
        'requires-modules',
        'ignore-verification',
        'requires-bigip-version-max',
        'requires-bigip-version-min',
        'signing-key',
        'tmpl-checksum',
        'tmpl-signature',
        'total-signing-status',
        'prerequisite-errors',
        'verification-status',
    ]

    def __init__(self, template_str):
        '''Initialize class.

        :param template_str: string of iapp template file
        :raises: EmptyTemplateException
        '''

        if template_str:
            self.template_str = str(template_str)
        else:
            raise EmptyTemplateException('Template empty or None value.')

    def _get_section_end_index(self, section, section_start):
        '''Get end of section's content.

        In the loop to match braces, we must not count curly braces that are
        within a doubly quoted string.

        :param section: string name of section
        :param section_start: integer index of section's beginning
        :return: integer index of section's end
        :raises: CurlyBraceMismatchException
        '''

        brace_count = 0
        in_quote = False
        in_escape = False

        for index, char in enumerate(self.template_str[section_start:]):
            # This check is to look for items inside of an escape sequence.
            #
            # For example, in the iApp team's iApps, there is a proc called
            # "iapp_get_items" which has a line that looks like this.
            #
            #     set val [string map {\" ""} $val]
            #
            # This will cause this parser to fail because of the unbalanced
            # quotes. Therefore, this conditional takes this into consideration
            #
            if char == '\\' and not in_escape:
                in_escape = True
            elif char == '\\' and in_escape:
                in_escape = False

            if not in_escape:
                if char == '"' and not in_quote:
                    in_quote = True
                elif char == '"' and in_quote:
                    in_quote = False

            if char == '{' and not in_quote:
                brace_count += 1
            elif char == '}' and not in_quote:
                brace_count -= 1

            if brace_count is 0:
                return index + section_start

        if brace_count is not 0:
            raise CurlyBraceMismatchException(
                'Curly braces mismatch in section %s.' % section
                )

    def _get_section_start_index(self, section):
        '''Get start of a section's content.

        :param section: string name of section
        :return: integer index of section's beginning
        :raises: NonextantSectionException
        '''

        sec_start_re = '%s\s*\{' % section

        found = re.search(sec_start_re, self.template_str)
        if found:
            return found.end() - 1

        raise NonextantSectionException(
            'Section %s not found in template' % section
            )

    def _get_template_name(self):
        '''Find template name.

        :returns: string of template name
        :raises: NonextantTemplateNameException
        '''

        start_pattern = "sys application template\s+" \
                        "(\/[\w\.\-]+\/)?" \
                        "(?P<name>[\w\.\-]+)\s*\{"

        template_start = re.search(start_pattern, self.template_str)
        if template_start:
            return template_start.group('name')

        raise NonextantTemplateNameException('Template name not found.')

    def _get_template_attr(self, attr):
        '''Find the attribute value for a specific attribute.

        :param attr: string of attribute name
        :returns: string of attribute value
        '''

        attr_re = '%s\s+.*' % attr

        attr_found = re.search(attr_re, self.template_str)
        if attr_found:
            attr_value = attr_found.group(0).replace(attr, '', 1)
            return attr_value.strip()

    def _add_sections(self):
        '''Add the found and required sections to the templ_dict.'''
        for section in self.template_sections:
            try:
                sec_start = self._get_section_start_index(section)
            except NonextantSectionException:
                if section in self.sections_not_required:
                    continue
                raise
            sec_end = self._get_section_end_index(section, sec_start)
            section_value = self.template_str[sec_start+1:sec_end].strip()
            section, section_value = self._transform_key_value(
                section,
                section_value,
                self.section_map
            )
            self.templ_dict['actions']['definition'][section] = section_value
            self.template_str = self.template_str[:sec_start+1] + \
                self.template_str[sec_end:]

    def _add_cli_scripts(self):
        '''Add the found external sections to the templ_dict.'''

        pattern = "cli script\s+" \
                  "(\/[\w\.\-]+\/)?" \
                  "(?P<name>[\w\.\-]+)\s*\{"
        sections = re.finditer(pattern, self.template_str)

        for section in sections:
            if 'scripts' not in self.templ_dict:
                self.templ_dict['scripts'] = []

            try:
                sec_start = self._get_section_start_index(
                    section.group('name')
                )
            except NonextantSectionException:
                continue

            sec_end = self._get_section_end_index(
                section.group('name'), sec_start
            )
            section_value = self.template_str[sec_start+1:sec_end].strip()

            self.templ_dict['scripts'].append(dict(
                name=section.group('name'),
                script=section_value
            ))

            self.template_str = self.template_str[:sec_start+1] + \
                self.template_str[sec_end:]

    def _add_attrs(self):
        '''Add the found and required attrs to the templ_dict.'''
        for attr in self.template_attrs:
            attr_value = self._get_template_attr(attr)

            if not attr_value:
                continue

            attr, attr_value = self._transform_key_value(
                attr,
                attr_value,
                self.attr_map
            )
            self.templ_dict[attr] = attr_value

    def _parse_tcl_list(self, attr, list_str):
        '''Turns a string representation of a TCL list into a Python list.

        :param attr: string name of attribute
        :param list_str: string representation of a list
        :returns: Python list
        '''

        list_str = list_str.strip()

        if not list_str:
            return []

        if list_str[0] != '{' and list_str[-1] != '}':
            if list_str.find('none') >= 0:
                return list_str

        if not re.search(self.tcl_list_patterns[attr], list_str):
            raise MalformedTCLListException(
                'TCL list for "%s" is malformed. ' % attr
            )

        list_str = list_str.strip('{').strip('}')
        list_str = list_str.strip()
        return list_str.split()

    def _transform_key_value(self, key, value, map_dict):
        '''Massage keys and values for iapp dict to look like JSON.

        :param key: string dictionary key
        :param value: string dictionary value
        :param map_dict: dictionary to map key names
        '''

        if key in self.tcl_list_patterns:
            value = self._parse_tcl_list(key, value)

        if key in map_dict:
            key = map_dict[key]

        return key, value

    def parse_template(self):
        '''Parse the template string into a dict.

        Find the (large) inner sections first, save them, and remove them from
        a modified string. Then find the template attributes in the modified
        string.

        :returns: dictionary of parsed template
        '''

        self.templ_dict = {'actions': {'definition': {}}}

        self.templ_dict['name'] = self._get_template_name()

        self._add_cli_scripts()
        self._add_sections()
        self._add_attrs()

        return self.templ_dict


class EmptyTemplateException(F5SDKError):
    pass


class CurlyBraceMismatchException(F5SDKError):
    pass


class NonextantSectionException(F5SDKError):
    pass


class NonextantTemplateNameException(F5SDKError):
    pass


class MalformedTCLListException(F5SDKError):
    pass

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


class IappParser(object):

    template_sections = [
        u'presentation',
        u'implementation',
        u'html-help',
        u'role-acl'
    ]

    template_attrs = [u'description', u'partition']

    def __init__(self, template_str):
        '''Initialize class.

        :param template_str: string of iapp template file
        :raises: EmptyTemplateException
        '''

        if template_str:
            self.template_str = unicode(template_str)
        else:
            raise EmptyTemplateException('Template empty or None value.')

    def get_section_end_index(self, section, section_start):
        '''Get end of section's content.

        :param section: string name of section
        :param section_start: integer index of section's beginning
        :return: integer index of section's end
        :raises: CurlyBraceMismatchException
        '''

        brace_count = 0

        for index, char in enumerate(self.template_str[section_start:]):
            if char == u'{':
                brace_count += 1
            elif char == u'}':
                brace_count -= 1

            if brace_count is 0:
                return index + section_start

        if brace_count is not 0:
            raise CurlyBraceMismatchException(
                'Curly braces mismatch in section %s.' % section
                )

    def get_section_start_index(self, section):
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

    def get_template_name(self):
        '''Find template name.

        :returns: string of template name
        :raises: NonextantTemplateNameException
        '''

        start_pattern = 'sys application template\s+\w+\s*\{'

        template_start = re.search(start_pattern, self.template_str)
        if template_start:
            split_start = template_start.group(0).split()
            if split_start[3][-1:] == u'{':
                split_start[3] = split_start[3][:-1]
            return split_start[3]

        raise NonextantTemplateNameException('Template name not found.')

    def get_template_attr(self, attr):
        '''Find the attribute value for a specific attribute.

        :param attr: string of attribute name
        :returns: string of attribute value
        '''

        attr_re = '%s\s+.*' % attr

        attr_found = re.search(attr_re, self.template_str)
        if attr_found:
            attr_value = attr_found.group(0).replace(attr, '', 1)
            return attr_value.strip()

    def parse_template(self):
        '''Parse the template string into a dict.

        Find the (large) inner sections first, save them, and remove them from
        a modified string. Then find the template attributes in the modified
        string.

        :returns: dictionary of parsed template
        '''

        templ_dict = {}
        templ = self.template_str

        templ_dict[u'name'] = self.get_template_name()

        for section in self.template_sections:
            sec_start = self.get_section_start_index(section)
            sec_end = self.get_section_end_index(section, sec_start)
            templ_dict[section] = templ[sec_start+1:sec_end].strip()
            templ = templ[:sec_start+1] + templ[sec_end:]

        for attr in self.template_attrs:
            templ_dict[attr] = self.get_template_attr(attr)

        return templ_dict


class EmptyTemplateException(Exception):
    pass


class CurlyBraceMismatchException(Exception):
    pass


class NonextantSectionException(Exception):
    pass


class NonextantTemplateNameException(Exception):
    pass

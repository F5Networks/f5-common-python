import re

class IappParser(object):

    template_sections = [
        'presentation',
        'implementation',
        'html-help',
        'role-acl'
    ]

    template_attrs = ['description', 'partition']

    def __init__(self, template_str):
        '''Initialize class.

        :raises: EmptyTemplateException
        '''
        
        if template_str:
            self.template_str = template_str
        else:
            raise EmptyTemplateException('Template empty or None value.')

    def get_section_end(self, section, section_start):
        '''Get end of section's content.

        :param section_start: string name of template section
        :return: integer index of section's end
        :raises: 
        '''

        brace_count = 0

        for index, char in enumerate(self.template_str[section_start:]):
            if char is '{':
                brace_count += 1
            if char is '}':
                brace_count -= 1
            if brace_count is 0:
                return index + section_start

        if brace_count is not 0:
            raise CurlyBraceMismatchException(
                'Curly braces mismatch in section {}.'.format(section)
                )

    def get_section_start(self, section):
        '''Get start of a section's content.

        :param section: string name of section
        :return: integer index of section's beginning
        :raises: Exception
        '''

        sec_start_re = '%s\s*\{' % section

        for found in re.finditer(sec_start_re, self.template_str):
            if found:
                return found.end() - 1

        raise NonextantSectionException(
            'Section {} not found in template'.format(section)
            )

    def get_template_name(self):
        '''Find template name.

        :returns: string of template name
        :raises: Exception
        '''
        name = ''
        start_pattern = 'sys application template\s+\w+\s*\{
        
        template_start = re.search(start_pattern, self.template_str)
        if template_start:
            split_start = template_start.group(0).split()
            return split_start[3]
        
        raise NonextantTemplateName('Template name not found.')
        
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
        
        :return:
        '''

        templ_dict = {}
        templ = self.template_str
        
        template_name = self.get_template_name()

        for section in self.template_sections:
            sec_start = self.get_section_start(section)
            sec_end = self.get_section_end(section, sec_start)
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

class NonextantTemplateName(Exception):
    pass

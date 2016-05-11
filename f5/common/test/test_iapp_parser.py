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

from f5.common import iapp_parser as ip

import pytest


good_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
  requires-modules { ltm }
}'''

brace_in_quote_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for "" the template
      }
      implementation {
        # TMSH"{}{{}}}}}""{{{{}}"implementation code
      }
      presentation {
        # APL"{}{}{{{{{{" presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
  requires-modules { ltm }
}'''

no_desc_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  partition <partition name>
  requires-modules { ltm }
}'''

empty_rm_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  partition <partition name>
  requires-modules { }
}'''

whitespace_rm_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  partition <partition name>
  requires-modules {}
}'''

none_rm_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  partition <partition name>
  requires-modules none
}'''

no_open_brace_templ = '''sys application template no_open_brace_templ {
  actions {
    definition {
      html-help
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl {security role}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

no_close_brace_templ = '''sys application template no_close_brace_template {
  actions {
    definition {
      html-help {
        # HTML Help for the template
        # Missing closing braces
      implementation {
        # TMSH implementation code
      '''

no_pres_templ = '''sys application template no_pres_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      role-acl {<security role>}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

no_name_templ = '''sys application template  {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

bad_name_templ = '''sys application template bad#updown {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      role-acl {<security role>}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

name_brace_templ = '''sys application template name_next_to_brace{
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      role-acl {security role}
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
}'''

good_attr_templ = '''sys application template good_templ {
  actions {
    definition {
      html-help {}
      implementation {}
      presentation {}
    }
  }
  description <template description>
  partition just_a_partition name
}'''

no_help_templ = '''sys application template good_templ {
  actions {
    definition {
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
  requires-modules { ltm asm }
}'''

dot_name_templ = '''sys application template good.dot.templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
  requires-modules { ltm }
}'''

dot_hyphen_name_templ = '''sys application template good.-dot-hyphen.-templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      presentation {
        # APL presentation language
      }
      role-acl { hello test }
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
  requires-modules { ltm }
}'''

good_templ_dict = {
    u'name': u'good_templ',
    u'description': u'<template description>',
    u'partition': u'<partition name>',
    u'requiresModules': [u'ltm'],
    'actions': {
        'definition': {
            u'htmlHelp': u'# HTML Help for the template',
            u'roleAcl': [u'hello', u'test'],
            u'implementation': u'# TMSH implementation code',
            u'presentation': u'# APL presentation language'
        }
    }
}

brace_in_quote_templ_dict = {
    u'name': u'good_templ',
    u'description': u'<template description>',
    u'partition': u'<partition name>',
    u'requiresModules': [u'ltm'],
    'actions': {
        'definition': {
            u'htmlHelp': u'# HTML Help for "" the template',
            u'roleAcl': [u'hello', u'test'],
            u'implementation': u'# TMSH"{}{{}}}}}""{{{{}}"implementation code',
            u'presentation': u'# APL"{}{}{{{{{{" presentation language'
        }
    }
}

no_help_templ_dict = {
    u'name': u'good_templ',
    u'description': u'<template description>',
    u'partition': u'<partition name>',
    u'requiresModules': [u'ltm', u'asm'],
    'actions': {
        'definition': {
            u'roleAcl': [u'hello', u'test'],
            u'implementation': u'# TMSH implementation code',
            u'presentation': u'# APL presentation language'
        }
    }
}

none_rm_templ_dict = {
    u'name': u'good_templ',
    u'partition': u'<partition name>',
    u'requiresModules': u'none',
    'actions': {
        'definition': {
            u'htmlHelp': u'# HTML Help for the template',
            u'roleAcl': [u'hello', u'test'],
            u'implementation': u'# TMSH implementation code',
            u'presentation': u'# APL presentation language'
        }
    }
}

dot_name_templ_dict = {
    u'name': u'good.dot.templ',
    u'description': u'<template description>',
    u'partition': u'<partition name>',
    u'requiresModules': [u'ltm'],
    'actions': {
        'definition': {
            u'htmlHelp': u'# HTML Help for the template',
            u'roleAcl': [u'hello', u'test'],
            u'implementation': u'# TMSH implementation code',
            u'presentation': u'# APL presentation language'
        }
    }
}


dot_hyphen_name_templ_dict = {
    u'name': u'good.-dot-hyphen.-templ',
    u'description': u'<template description>',
    u'partition': u'<partition name>',
    u'requiresModules': [u'ltm'],
    'actions': {
        'definition': {
            u'htmlHelp': u'# HTML Help for the template',
            u'roleAcl': [u'hello', u'test'],
            u'implementation': u'# TMSH implementation code',
            u'presentation': u'# APL presentation language'
        }
    }
}


@pytest.fixture
def TemplateSectionSetup(request):
    def tearDown():
        prsr.template_sections.remove('notfound')
    request.addfinalizer(tearDown)
    prsr = ip.IappParser(good_templ)
    prsr.template_sections.append('notfound')
    return prsr


def test__init__():
    prsr = ip.IappParser(good_templ)
    assert prsr.template_str == good_templ


def test__init__error():
    prsr = None
    with pytest.raises(ip.EmptyTemplateException) as EmptyTemplateExceptInfo:
        prsr = ip.IappParser('')
    assert EmptyTemplateExceptInfo.value.message == \
        'Template empty or None value.'
    assert prsr is None


def test_get_section_end_index():
    prsr = ip.IappParser(good_templ)
    impl_start = prsr._get_section_start_index(u'implementation')
    impl_end = prsr._get_section_end_index(u'implementation', impl_start)
    templ_impl = unicode('''{
        # TMSH implementation code
      }''')
    assert good_templ[impl_start:impl_end+1] == templ_impl


def test_get_section_start_index_no_open_brace_error():
    prsr = ip.IappParser(no_open_brace_templ)
    with pytest.raises(ip.NonextantSectionException) as \
            NonextantSectionExceptInfo:
        prsr._get_section_start_index(u'html-help')
    assert NonextantSectionExceptInfo.value.message == \
        'Section html-help not found in template'


def test_get_section_end_no_close_brace_error():
    prsr = ip.IappParser(no_close_brace_templ)
    with pytest.raises(ip.CurlyBraceMismatchException) as \
            CurlyBraceMismatchExceptInfo:
        help_start = prsr._get_section_start_index(u'html-help')
        prsr._get_section_end_index(u'html_help', help_start)
    assert CurlyBraceMismatchExceptInfo.value.message == \
        'Curly braces mismatch in section html_help.'


def test_get_template_name():
    prsr = ip.IappParser(good_templ)
    assert prsr._get_template_name() == u'good_templ'


def test_get_template_name_next_to_brace():
    prsr = ip.IappParser(name_brace_templ)
    assert prsr._get_template_name() == u'name_next_to_brace'


def test_get_template_name_error():
    prsr = ip.IappParser(no_name_templ)
    with pytest.raises(ip.NonextantTemplateNameException) as \
            NonextantTemplateNameExceptInfo:
        prsr._get_template_name()
    assert NonextantTemplateNameExceptInfo.value.message == \
        'Template name not found.'


def test_get_template_name_bad_name_error():
    prsr = ip.IappParser(bad_name_templ)
    with pytest.raises(ip.NonextantTemplateNameException) as \
            NonextantTemplateNameExceptInfo:
        prsr._get_template_name()
    assert NonextantTemplateNameExceptInfo.value.message == \
        'Template name not found.'


def test_get_template_name_with_dot():
    prsr = ip.IappParser(dot_name_templ)
    assert prsr.parse_template() == dot_name_templ_dict


def test_get_template_name_with_dot_hyphen():
    prsr = ip.IappParser(dot_hyphen_name_templ)
    assert prsr.parse_template() == dot_hyphen_name_templ_dict


def test_parse_template():
    prsr = ip.IappParser(good_templ)
    assert prsr.parse_template() == good_templ_dict


def test_parse_template_brace_in_quote():
    prsr = ip.IappParser(brace_in_quote_templ)
    assert prsr.parse_template() == brace_in_quote_templ_dict


def test_parse_template_no_section_found(TemplateSectionSetup):
    with pytest.raises(ip.NonextantSectionException) as \
            NonextantSectionExceptInfo:
        TemplateSectionSetup.parse_template()
    assert 'notfound' in TemplateSectionSetup.template_sections
    assert 'Section notfound not found in template' in \
        NonextantSectionExceptInfo.value.message


def test_parse_template_no_section_found_not_required():
    prsr = ip.IappParser(no_help_templ)
    templ_dict = prsr.parse_template()
    assert templ_dict == no_help_templ_dict


def test_get_template_attr():
    prsr = ip.IappParser(good_attr_templ)
    attr = prsr._get_template_attr(u'partition')
    assert attr == u'just_a_partition name'


def test_get_template_attr_attr_not_exists():
    prsr = ip.IappParser(good_attr_templ)
    attr = prsr._get_template_attr(u'bad_attr')
    assert attr is None


def test_attr_no_description():
    prsr = ip.IappParser(no_desc_templ)
    templ_dict = prsr.parse_template()
    assert 'description' not in templ_dict


def test_attr_empty_rm_error():
    prsr = ip.IappParser(empty_rm_templ)
    with pytest.raises(ip.MalformedTCLListException) as ex:
        prsr.parse_template()
    assert 'requires-modules' in ex.value.message


def test_attr_whitespace_rm_error():
    prsr = ip.IappParser(whitespace_rm_templ)
    with pytest.raises(ip.MalformedTCLListException) as ex:
        prsr.parse_template()
    assert 'TCL list for "requires-modules" is malformed. If no elements are '\
        'needed "none" should be used without curly braces.' in \
        ex.value.message


def test_attr_none_rm():
    prsr = ip.IappParser(none_rm_templ)
    templ_dict = prsr.parse_template()
    assert templ_dict == none_rm_templ_dict

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

from f5.utils import iapp_parser as ip

import pytest


good_templ = '''
sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      macro {
        # TMSH macro code
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

slashes_name_templ = '''sys application template /Common/good_slashes_templ {
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

empty_role_acl_templ = '''
sys application template good_templ {
  actions {
    definition {
      html-help {}
      implementation {}
      presentation {}
    }
  }
  requires-modules { }
  description <template description>
  partition <partition name>
}'''

cli_scripts_templ = '''
cli script script.one {
  # TMSH script 1 code
}
cli script script.two {
  # TMSH script 2 code
}
sys application template good_templ {
  actions {
    definition {
      html-help {
        # HTML Help for the template
      }
      implementation {
        # TMSH implementation code
      }
      macro {
        # TMSH macro code
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
  ignore-verification <verification>
  requires-bigip-version-max <max version>
  requires-bigip-version-min <min version>
  signing-key <signing key>
  tmpl-checksum <checksum>
  tmpl-signature <signature>
  prerequisite-errors <errors>
}'''

unbalanced_quote_templ = '''
sys application template unbalanced_quote_templ {
  actions {
    definition {
      html-help {}
      implementation {
        set val [string map {\\" ""} $val]

      }
      presentation {}
      role-acl { hello test }
      run-as <user context>
    }
  }
  description <template description>
  partition <partition name>
  requires-modules { ltm }
}'''


good_templ_dict = {
    'name': 'good_templ',
    'description': '<template description>',
    'partition': '<partition name>',
    'requiresModules': ['ltm'],
    'actions': {
        'definition': {
            'htmlHelp': '# HTML Help for the template',
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH implementation code',
            'presentation': '# APL presentation language'
        }
    }
}

unbalanced__quote_templ_dict = {
    'name': 'good_templ',
    'description': '<template description>',
    'partition': '<partition name>',
    'requiresModules': ['ltm'],
    'actions': {
        'definition': {
            'htmlHelp': '',
            'roleAcl': ['hello', 'test'],
            'implementation': 'set val [string map {\" ""} $val]',
            'presentation': ''
        }
    }
}

brace_in_quote_templ_dict = {
    'name': 'good_templ',
    'description': '<template description>',
    'partition': '<partition name>',
    'requiresModules': ['ltm'],
    'actions': {
        'definition': {
            'htmlHelp': '# HTML Help for "" the template',
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH"{}{{}}}}}""{{{{}}"implementation code',
            'presentation': '# APL"{}{}{{{{{{" presentation language'
        }
    }
}

no_help_templ_dict = {
    'name': 'good_templ',
    'description': '<template description>',
    'partition': '<partition name>',
    'requiresModules': ['ltm', 'asm'],
    'actions': {
        'definition': {
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH implementation code',
            'presentation': '# APL presentation language'
        }
    }
}

none_rm_templ_dict = {
    'name': 'good_templ',
    'partition': '<partition name>',
    'requiresModules': 'none',
    'actions': {
        'definition': {
            'htmlHelp': '# HTML Help for the template',
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH implementation code',
            'presentation': '# APL presentation language'
        }
    }
}

dot_name_templ_dict = {
    'name': 'good.dot.templ',
    'description': '<template description>',
    'partition': '<partition name>',
    'requiresModules': ['ltm'],
    'actions': {
        'definition': {
            'htmlHelp': '# HTML Help for the template',
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH implementation code',
            'presentation': '# APL presentation language'
        }
    }
}


dot_hyphen_name_templ_dict = {
    'name': 'good.-dot-hyphen.-templ',
    'description': '<template description>',
    'partition': '<partition name>',
    'requiresModules': ['ltm'],
    'actions': {
        'definition': {
            'htmlHelp': '# HTML Help for the template',
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH implementation code',
            'presentation': '# APL presentation language'
        }
    }
}

slashes_name_templ_dict = {
    'name': 'good_slashes_templ',
    'description': '<template description>',
    'partition': '<partition name>',
    'requiresModules': ['ltm'],
    'actions': {
        'definition': {
            'htmlHelp': '# HTML Help for the template',
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH implementation code',
            'presentation': '# APL presentation language'
        }
    }
}

cli_scripts_templ_dict = {
    'name': 'good_templ',
    'description': '<template description>',
    'partition': '<partition name>',
    'requiresModules': ['ltm'],
    'ignoreVerification': '<verification>',
    'requiresBigipVersionMax': '<max version>',
    'requiresBigipVersionMin': '<min version>',
    'signingKey': '<signing key>',
    'tmplChecksum': '<checksum>',
    'tmplSignature': '<signature>',
    'prerequisiteErrors': '<errors>',
    'actions': {
        'definition': {
            'htmlHelp': '# HTML Help for the template',
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH implementation code',
            'presentation': '# APL presentation language'
        }
    },
    'scripts': [
        {
            'name': 'script.one',
            'script': '# TMSH script 1 code',
        },
        {
            'name': 'script.two',
            'script': '# TMSH script 2 code',
        },
    ]
}

empty_rm_templ_dict = {
    'name': 'good_templ',
    'partition': '<partition name>',
    'requiresModules': [],
    'actions': {
        'definition': {
            'htmlHelp': '# HTML Help for the template',
            'roleAcl': ['hello', 'test'],
            'implementation': '# TMSH implementation code',
            'presentation': '# APL presentation language'
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
    with pytest.raises(ip.EmptyTemplateException) as ex:
        prsr = ip.IappParser('')
    assert str(ex.value) == 'Template empty or None value.'
    assert prsr is None


def test_get_section_end_index():
    prsr = ip.IappParser(good_templ)
    impl_start = prsr._get_section_start_index('implementation')
    impl_end = prsr._get_section_end_index('implementation', impl_start)
    templ_impl = str('''{
        # TMSH implementation code
      }''')
    assert good_templ[impl_start:impl_end+1] == templ_impl


def test_get_section_start_index_no_open_brace_error():
    prsr = ip.IappParser(no_open_brace_templ)
    with pytest.raises(ip.NonextantSectionException) as ex:
        prsr._get_section_start_index('html-help')
    assert str(ex.value) == 'Section html-help not found in template'


def test_get_section_end_no_close_brace_error():
    prsr = ip.IappParser(no_close_brace_templ)
    with pytest.raises(ip.CurlyBraceMismatchException) as ex:
        help_start = prsr._get_section_start_index('html-help')
        prsr._get_section_end_index('html_help', help_start)
    assert str(ex.value) == 'Curly braces mismatch in section html_help.'


def test_unbalanced_quote_error():
    prsr = ip.IappParser(unbalanced_quote_templ)
    prsr.parse_template()


def test_get_template_name():
    prsr = ip.IappParser(good_templ)
    assert prsr._get_template_name() == 'good_templ'


def test_get_template_name_next_to_brace():
    prsr = ip.IappParser(name_brace_templ)
    assert prsr._get_template_name() == 'name_next_to_brace'


def test_get_template_name_error():
    prsr = ip.IappParser(no_name_templ)
    with pytest.raises(ip.NonextantTemplateNameException) as ex:
        prsr._get_template_name()
    assert str(ex.value) == 'Template name not found.'


def test_get_template_name_bad_name_error():
    prsr = ip.IappParser(bad_name_templ)
    with pytest.raises(ip.NonextantTemplateNameException) as ex:
        prsr._get_template_name()
    assert str(ex.value) == 'Template name not found.'


def test_get_template_name_with_dot():
    prsr = ip.IappParser(dot_name_templ)
    assert prsr.parse_template() == dot_name_templ_dict


def test_get_template_name_with_dot_hyphen():
    prsr = ip.IappParser(dot_hyphen_name_templ)
    assert prsr.parse_template() == dot_hyphen_name_templ_dict


def test_get_template_name_with_slashes():
    prsr = ip.IappParser(slashes_name_templ)
    assert prsr.parse_template() == slashes_name_templ_dict


def test_parse_template():
    prsr = ip.IappParser(good_templ)
    assert prsr.parse_template() == good_templ_dict


def test_parse_template_brace_in_quote():
    prsr = ip.IappParser(brace_in_quote_templ)
    assert prsr.parse_template() == brace_in_quote_templ_dict


def test_count_template_cli_scripts():
    prsr = ip.IappParser(cli_scripts_templ)
    assert prsr.parse_template() == cli_scripts_templ_dict


def test_parse_template_no_section_found(TemplateSectionSetup):
    with pytest.raises(ip.NonextantSectionException) as ex:
        TemplateSectionSetup.parse_template()
    assert 'notfound' in TemplateSectionSetup.template_sections
    assert 'Section notfound not found in template' in str(ex.value)


def test_parse_template_no_section_found_not_required():
    prsr = ip.IappParser(no_help_templ)
    templ_dict = prsr.parse_template()
    assert templ_dict == no_help_templ_dict


def test_get_template_attr():
    prsr = ip.IappParser(good_attr_templ)
    attr = prsr._get_template_attr('partition')
    assert attr == 'just_a_partition name'


def test_get_template_attr_attr_not_exists():
    prsr = ip.IappParser(good_attr_templ)
    attr = prsr._get_template_attr('bad_attr')
    assert attr is None


def test_attr_no_description():
    prsr = ip.IappParser(no_desc_templ)
    templ_dict = prsr.parse_template()
    assert 'description' not in templ_dict


def test_attr_empty_rm():
    prsr = ip.IappParser(empty_rm_templ)
    assert prsr.parse_template() == empty_rm_templ_dict


def test_attr_none_rm():
    prsr = ip.IappParser(none_rm_templ)
    templ_dict = prsr.parse_template()
    assert templ_dict == none_rm_templ_dict

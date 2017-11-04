# coding=utf-8
#
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
"""BIG-IP® system file module

REST URI
    ``http://localhost/mgmt/tm/sys/provision``

GUI Path
    N/A

REST Kind
    ``tm:sys:provision:*``
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import UnnamedResource


class Provision(OrganizingCollection):
    def __init__(self, sys):
        super(Provision, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Afm,
            Am,
            Apm,
            Asm,
            Avr,
            Dos,
            Fps,
            Gtm,
            Ili,
            Ilx,
            Lc,
            Ltm,
            Pem,
            Swg,
            Urldb,
            Vcmp
        ]


class Afm(UnnamedResource):
    """BIG-IP® system provision afm resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Afm, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Am(UnnamedResource):
    """BIG-IP® system provision afm resource

    The am object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Am, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Apm(UnnamedResource):
    """BIG-IP® system provision apm resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Apm, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Asm(UnnamedResource):
    """BIG-IP® system provision asm resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Asm, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Avr(UnnamedResource):
    """BIG-IP® system provision avr resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Avr, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Dos(UnnamedResource):
    """BIG-IP® system provision dos resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Dos, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Fps(UnnamedResource):
    """BIG-IP® system provision fps resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Fps, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Gtm(UnnamedResource):
    """BIG-IP® system provision gtm resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Gtm, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Ili(UnnamedResource):
    """BIG-IP® system provision ili resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Ili, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Ilx(UnnamedResource):
    """BIG-IP® system provision ilx resource

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Ilx, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Lc(UnnamedResource):
    """BIG-IP® system provision lc resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Lc, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Ltm(UnnamedResource):
    """BIG-IP® system provision ltm resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Ltm, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Pem(UnnamedResource):
    """BIG-IP® system provision pem resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Pem, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Swg(UnnamedResource):
    """BIG-IP® system provision swg resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Swg, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Urldb(UnnamedResource):
    """BIG-IP® system provision urldb resource

    The afm object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Urldb, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'


class Vcmp(UnnamedResource):
    """BIG-IP® system provision vcmp resource

    The vcmp object only supports load and update because it is an
    unnamed resource.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, provision):
        super(Vcmp, self).__init__(provision)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:provision:provisionstate'

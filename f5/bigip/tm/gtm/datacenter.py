# coding=utf-8
#
# Copyright 2014-2017 F5 Networks Inc.
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

"""BIG-IP® Global Traffic Manager (GTM) datacenter module.

REST URI
    ``http://localhost/mgmt/tm/gtm/datacenter``

GUI Path
    ``DNS --> GSLB : Data Centers``

REST Kind
    ``tm:gtm:datacenter:*``
"""

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Datacenters(Collection):
    """BIG-IP® GTM datacenter collection"""
    def __init__(self, gtm):
        super(Datacenters, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Datacenter]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:datacenter:datacenterstate': Datacenter}


class Datacenter(Resource, ExclusiveAttributesMixin):
    """BIG-IP® GTM datacenter resource"""
    def __init__(self, dc_s):
        super(Datacenter, self).__init__(dc_s)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:datacenter:datacenterstate'
        self._meta_data['exclusive_attributes'].append(('enabled', 'disabled'))

    def _endis_attrs(self):
        """Manipulate return value to equal negation of set value

        This function (uniquely?!) manipulates response values before the
        consumer has access to them. We think this is dangerous. It is likely
        this function will move once we figure out how to properly annotate
        this RISKY behavior!"

        The BIG-IP REST API for this particular endpoint has two fields
        which are mutually exclusive; disabled and enabled. When using this
        SDK API, you may do the following

            d = api.tm.gtm.datasources.datasource.load(name='foo')
            d.update(enabled=False)

        You might expect that the behavior of the following...

            if d.enabled:
                print("enabled")
            else:
                print("disabled")

        ...would result in "enabled" being printed, but that would not be
        the case; BIG-IP will specify that "enabled" is True and that the
        following is also now True

            d.disabled == True

        This behavior of setting a different variable instead of the one
        that you specified, may not be obvious to the casual user. Therefore,
        this method will set appropriate sister variables to be the negation
        of the variable you set.

        Therefore

            d.enabled = True

        will also do the following automatically

            d.disabled = False

        This behavior will allow the SDK to behave according to most users
        expectations, shown below

            d.update(enabled=False)
            if d.enabled:
                print("enabled")
            else:
                print("disabled")

        which will print the following

            "disabled"

        Likewise, checking for d.disabled would return True.
        Returns:
            None
        """
        if 'disabled' in self.__dict__:
            self.__dict__['enabled'] = not self.__dict__['disabled']
        if 'enabled' in self.__dict__:
            self.__dict__['disabled'] = not self.__dict__['enabled']
        return None

    def create(self, **kwargs):
        inst = self._create(**kwargs)
        inst._endis_attrs()
        return inst

    def load(self, **kwargs):
        kwargs = self._reduce_boolean_pair(kwargs, 'enabled', 'disabled')
        inst = self._load(**kwargs)
        inst._endis_attrs()
        return inst

    def refresh(self, **kwargs):
        kwargs = self._reduce_boolean_pair(kwargs, 'enabled', 'disabled')
        self._refresh(**kwargs)
        self._endis_attrs()
        return self

    def update(self, **kwargs):
        if 'enabled' in kwargs or 'disabled' in kwargs:
            self.__dict__.pop('enabled')
            self.__dict__.pop('disabled')
        self._update(**kwargs)
        self._endis_attrs()

# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""This provides tools that manipulate configurations of device resources.


"""

from six import iteritems
from six.moves.urllib.parse import urlparse


class BaseHandler(object):
    def __init__(self, resource):
        self.resource = resource


class Stats(BaseHandler):
    """Stats handler class

    When this class is first instantiated, it will populate, ['stat']
    attribute with individual stats, that can be accessed via dot notation
    """
    def __init__(self, stats):
        super(Stats, self).__init__(stats)
        self.rdict = self.resource.entries
        self._update_stats()

    def _key_dot_replace(self, rdict):
        """Replace fullstops in returned keynames"""
        temp_dict = {}
        for key, value in iteritems(rdict):
            if isinstance(value, dict):
                value = self._key_dot_replace(value)
            temp_dict[key.replace('.', '_')] = value
        return temp_dict

    def _get_nest_stats(self):
        """Helper method to deal with nestedStats

        as json format changed in v12.x
        """
        for x in self.rdict:
            check = urlparse(x)
            if check.scheme:
                nested_dict = self.rdict[x]['nestedStats']
                tmp_dict = nested_dict['entries']
                return self._key_dot_replace(tmp_dict)

        return self._key_dot_replace(self.rdict)

    def _update_stats(self):
        """Attaches stat attribute to stats object"""
        stat_vals = self._get_nest_stats()
        self.__dict__['stat'] = DottedDict(stat_vals)

    def refresh(self, **kwargs):
        """Refreshes stats attached to an object"""
        self.resource.refresh(**kwargs)
        self.rdict = self.resource.entries
        self._update_stats()


class DottedDict(dict):
    """Helper class

    Allows accessing contents of a given dictionary
    by using object like 'dot' notation.

    @param :rdict Dictionary
    """
    def __init__(self, rdict):
        super(DottedDict, self).__init__()
        self.update(rdict)

    def __getattr__(self, k):
        if isinstance(self[k], dict) and not isinstance(self[k], DottedDict):
            self[k] = DottedDict(self[k])
        return self[k]

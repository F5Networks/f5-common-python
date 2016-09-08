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
import urlparse


class InvalidStatsJsonReturned(KeyError):
    """Returned stats JSON should always contain 'entries' key"""
    pass

class BaseHandler(object):
    def __init__(self, resource):
        self.resource = resource


class Stats(BaseHandler):
    def __init__(self, stats):
        super(Stats, self).__init__(stats)

    @property
    def stats_raw(self):
        """Provides JSON object converted to a python dictionary"""
        return self._get_stats_raw()

    def _key_dot_replace(self, rdict):
        """Replace fullstops in returned keynames"""
        temp_dict = {}
        for key, value in rdict.items():
            if isinstance(value, dict):
                value = self._key_dot_replace(value)
            temp_dict[key.replace('.', '_')] = value
        return temp_dict

    def _get_nest_stats(self, rdict):
        """Helper method to deal with nestedStats

        as json format changed in v12.x
        """
        for x in rdict:
            check = urlparse.urlparse(x)
            if check.scheme:
                nested_dict = rdict[x]['nestedStats']
                tmp_dict = nested_dict['entries']
                return self._key_dot_replace(tmp_dict)

        return self._key_dot_replace(rdict)

    def _get_stats_raw(self):
        """Displays JSON object transformed into python dictionary"""
        read_session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['container']._meta_data['uri'] + 'stats/'
        response = read_session.get(base_uri)
        rdict = response.json()
        return rdict

    def _update_stats(self, rdict):
        """Attaches stat attribute to stats object"""
        if 'entries' not in rdict:
            error = 'Missing "entries" key in returned JSON'
            raise InvalidStatsJsonReturned(error)
        sanitized = self._check_keys(rdict)
        stat_vals = self._get_nest_stats(sanitized['entries'])
        temp_meta = self._meta_data
        self.__dict__['stat'] = DottedDict(stat_vals)
        self._meta_data = temp_meta


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

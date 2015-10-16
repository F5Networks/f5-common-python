# Copyright 2014 F5 Networks Inc.
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

import logging
import sys


class Log(object):
    @staticmethod
    def debug(prefix, msg):
        Log._log('debug', prefix, msg)

    @staticmethod
    def error(prefix, msg):
        Log._log('error', prefix, msg)

    @staticmethod
    def crit(prefix, msg):
        Log._log('crit', prefix, msg)

    @staticmethod
    def info(prefix, msg):
        Log._log('info', prefix, msg)

    @staticmethod
    def _log(level, prefix, msg):
        log_string = prefix + ': ' + msg
        log = logging.getLogger(__name__)
        out_hdlr = logging.StreamHandler(sys.stdout)
        out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        log.addHandler(out_hdlr)

        if level == 'debug':
            log.debug(log_string)
        elif level == 'error':
            log.error(log_string)
        elif level == 'crit':
            log.critical(log_string)
        else:
            log.info(log_string)

        log.removeHandler(out_hdlr)

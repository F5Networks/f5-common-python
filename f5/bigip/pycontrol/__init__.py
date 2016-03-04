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

import re
import suds
from xml.sax import SAXParseException

from f5.sdk_exception import SDKError
# Project info


class F5Error(SDKError):
    def __init__(self, e):
        self.exception = e
        self.msg = str(e)

        if isinstance(e, suds.WebFault):
            try:
                parts = e.fault.faultstring.split('\n')
                # e_source = parts[0].replace("Exception caught in ", "")
                e_type = parts[1].replace("Exception: ", "")
                e_msg = re.sub("\serror_string\s*:\s*", "", parts[4])
                self.msg = "%s: %s" % (e_type, e_msg)
            except IndexError:
                self.msg = e.fault.faultstring
        if isinstance(e, SAXParseException):
            self.msg = "Unexpected server response. %s" % e.message

    def __str__(self):
        return self.msg

# Copyright 2016 F5 Networks Inc.

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
#

from functools import wraps
import time

from f5.utils.util_exceptions import UtilError


class MaximumAttemptsReached(UtilError):
    def __init__(self, *args, **kwargs):
        super(MaximumAttemptsReached, self).__init__(*args, **kwargs)


def poll_for_exceptionless_callable(callable, attempts, interval):
    '''Poll with a given callable for a specified number of times.

    :param callable: callable to invoke in loop -- if no exception is raised
                    the call is considered succeeded
    :param attempts: number of iterations to attempt
    :param interval: seconds to wait before next attempt
    '''

    @wraps(callable)
    def poll(*args, **kwargs):
        for attempt in range(attempts):
            try:
                return callable(*args, **kwargs)
            except Exception as ex:
                if attempt == attempts-1:
                    raise MaximumAttemptsReached(ex)
                time.sleep(interval)
                continue
    return poll

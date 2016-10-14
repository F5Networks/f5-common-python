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
'''A base exception for all exceptions in this library.'''


class F5SDKError(Exception):
    '''Import and subclass this exception in all exceptions in this library.'''
    def __init__(self, *args, **kwargs):
        super(F5SDKError, self).__init__(*args, **kwargs)


class UnsupportedMethod(F5SDKError):
    """Raise this if a method supplied is unsupported."""
    pass


class NodeStateModifyUnsupported(F5SDKError):
    '''Modify of node with state=unchecked is unsupported.'''
    pass

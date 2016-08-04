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

import pytest

from f5.bigip.contexts import TransactionContextManager
from f5.bigip.contexts import TransactionSubmitException


class TestTransaction(object):
    def test_create_empty(self, mgmt_root):
        tx = mgmt_root.tm.transactions.transaction
        with pytest.raises(TransactionSubmitException) as ex:
            # Do not remove this "NOQA". It is suppressing a flake8
            # exception that would be raised about "not using the
            # 'api' variable".
            #
            # This is, however, exactly what we want to do in this
            # test. By not using the 'api' variable, I am forcing
            # this context to raise the expected exception, and testing
            # that that exception is raised.
            with TransactionContextManager(tx) as api:  # NOQA
                pass
        assert "there is no command to commit in the transaction" \
               in str(ex.value.message)

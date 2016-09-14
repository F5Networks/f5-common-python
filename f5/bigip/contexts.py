# coding=utf-8
#
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


import copy
import logging

from f5.sdk_exception import F5SDKError


class TransactionSubmitException(F5SDKError):
    pass


class TransactionContextManager(object):
    def __init__(self, transaction, validate_only=False):
        """Initialize a new Transaction context

        Args:
            validate_only (bool): Will not commit the transaction, but only
                validate that it will succeed or not.

        Attributes:
            transaction (Transaction): The transaction object that was sent
                to the context manager
            validate_only (bool): Specifies whether the transaction should
                commit itself upon `__exit__` or whether the commands in the
                transaction should just be checked to make sure they don't
                raise an error.
            bigip (dict): A reference to the dictionary containing the BIG-IP
                mgmt_root
            icr (iControlRESTSession): A reference to the dictionary
                containing the iControl REST session
            original_headers (dict): A deep copy of all the headers that were
                originally part of the iControl REST session. A copy is needed
                so that we can revert back to them after the transaction has
                been committed, since the only way to commit the transaction
                is to set the X-F5-REST-Coordination-Id to the value of the
                transaction ID of the transaction.
        """
        self.transaction = transaction
        self.validate_only = validate_only
        self.bigip = transaction._meta_data['bigip']
        self.icr = self.bigip._meta_data['icr_session']
        self.original_headers = copy.deepcopy(self.icr.session.headers)

    def __enter__(self):
        """Begins a new transaction context

        When a transaction begins, this method will automatically be called
        to set up the transaction.

        Transaction IDs are automatically retrieved for you and the
        appropriate headers are set so that operations in the Transaction
        Context will reference the transaction.

        Headers are preserved so that after you exit the transaction, you will
        be able to use the API object as you normally would.
        """

        self.transaction = self.transaction.create()

        self.icr.session.headers.update({
            'X-F5-REST-Coordination-Id': str(self.transaction.transId)
        })
        return self.bigip

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Commit a transaction upon Context Manager exit

        Upon exit, the transaction will attempt to be committed. If the commit
        fails, the transaction will automatically be rolled back by the server
        performing the transaction.

        :param exc_type: The type of exception raised
        :param exc_value: Value of the exception raised
        :param exc_tb: Traceback
        NOTE: If the context exits without an exception, all three of the
        parameters will be None
        :returns: void
        """

        self.icr.session.headers = dict()
        if exc_tb is None:
            try:
                self.transaction.modify(state="VALIDATING",
                                        validateOnly=self.validate_only)
            except Exception as e:
                logging.debug(e)
                raise TransactionSubmitException(e)
            finally:
                self.icr.session.headers = self.original_headers
        self.icr.session.headers = self.original_headers

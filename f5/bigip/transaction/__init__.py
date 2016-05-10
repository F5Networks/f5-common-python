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

"""BIG-IP® system dns module

REST URI
    ``http://localhost/mgmt/tm/transaction``

REST Kind
    ``tm:transaction*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Transactions(Collection):
    """This class is a context manager for iControl transactions.

    Upon successful exit of the with statement, the transaction will be
    submitted, otherwise it will be rolled back.

    NOTE: This feature was added to BIGIP in version 11.0.0.

    Example:
    > bigip = BigIP(<args>)
    > tx = bigip.transactions.transaction
    > with TransactionContextManager(tx) as api:
    >     api.net.pools.pool.create(name="foo")
    >     api.sys.dbs.db.update(name="setup.run", value="false")
    >     <perform actions inside a transaction>
    >
    > # transaction is committed when you exit the "with" statement.
    """
    def __init__(self, api):
        super(Transactions, self).__init__(api)
        self._meta_data['allowed_lazy_attributes'] = [Transaction]
        self._meta_data['attribute_registry'] = \
            {'tm:transactionstate': Transaction}


class Transaction(Resource):
    def __init__(self, transactions):
        super(Transaction, self).__init__(transactions)
        self._meta_data['required_json_kind'] = 'tm:transactionstate'
        self._meta_data['required_creation_parameters'] = set()

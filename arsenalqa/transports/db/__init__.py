"""
* Copyright 2020 Wargaming Group Limited
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
"""

from functools import reduce

from pypika import Query, Table
from sqlalchemy import create_engine

from arsenalqa.base.transports import BaseTransport


class SingleEngine:
    urls = {}

    def __new__(cls, url):
        session = cls.urls.get(url)
        if session is None:
            session = create_engine(url)
            session.connect()
            cls.urls[url] = session
        return session


class Db(BaseTransport):
    """
    Parameters:
        host(str): optional first part of url
        url(str): db url. Url and host are used if session parameter is None only
        table(str): database tablename
        session(kombu.Connection): optional. Instance of kombu Connection object
        query: default pypika.Query type.
        model(Model): default FakeModel. Model which will be used in transport for send data and wrap response by default
    """

    def __init__(self, host=None, url=None, table=None, session=None, query=Query, **kwargs):
        super(Db, self).__init__(host=host, url=url, **kwargs)
        self.session = session or SingleEngine(self.prepare_url(host, url))
        self.table = Table(table)
        self.query = query

    def _join_filter(self, kwargs):
        _kwargs = self.model.data_filter()
        _kwargs.update(kwargs)
        return _kwargs

    def insert(self, data=None):
        """Method for insertion your data into database

        Parameters:
            data(any): optional. Parameter for overriding self.model
        """
        data = self.chose_data(data)
        return self.execute(str(self.query.into(self.table).columns(*data.keys()).insert(*data.values())))

    def get(self, **kwargs):
        """ Select single filtered raw from database. Raises Exception if raws count != 1. By default this method filters
        raw from database by self.model.model_filter() method + "filter_kwargs"

        Parameters:
            **kwargs: parameters for method all

        Returns:
            prepared response(usually Model instance)
        """
        result = self.all(**self._join_filter(kwargs))
        if len(result) != 1:
            raise Exception('Rows count for get method != 1: {}'.format(result))
        return result[0]

    def __reduce_kwargs(self, kwargs):
        return reduce(lambda x, y: x & y, [(getattr(self.table, key) == value) for key, value in kwargs.items()])

    def all(self, wrapper=None, limit=10, offset=0, **kwargs):
        """Method for selecting list of filtered raws. By default this method filters raws from table by "filter_kwargs".
        Filter_kwargs are used with "AND" operator: {"id": 1, "name": "Jhon"} == WHERE id=1 AND name=`Jhon`

        Parameters:
            limit(int): default 10. Limit of selected and filtered raws
            offset(int): default 0. Table raws start position
            **filter_kwargs: kwargs for filter raws from table by table fields

        Returns:
            ListObject of Models
        """
        wrapper = wrapper or self.model.wrap
        statement = self.query.from_(self.table).select('*')
        if kwargs:
            statement = statement.where(self.__reduce_kwargs(kwargs))
        statement = statement.limit(limit).offset(offset)
        return wrapper([dict(i) for i in self.execute(str(statement))])

    def update(self, data=None, **kwargs):
        """Method for updating raws  in table. By default all raws filters by two criteria: self.model.data_filter() +
        kwargs. But kwargs overrides self.model.data_filter().

        Parameters:
            data(dict): optional. Parameter for overriding self.model
            **kwargs: filter criteria for updating
        >>> model.data = {"name": "Jhon", "id": "1"}  # right now in database
        >>> model.data = {"name": "Andrew", "id": "1"}  # our update
        >>> model.db.update(name="Jhon")  # will update raw in table with id=1 and name="Jhon" to id=1 and name="Andrew"
        """
        kwargs = self._join_filter(kwargs)
        data = self.chose_data(data)
        if not kwargs:
            raise Exception('Filter criteria are required for update!')
        statement = self.query.update(self.table)
        for key, value in data.items():
            statement = statement.set(key, value)
        statement = statement.where(self.__reduce_kwargs(kwargs))
        return self.execute(str(statement))

    def delete(self, **kwargs):
        """Method for deleting raws  in table. By default all raws filters by two criteria: self.model.data_filter() +
        kwargs. But kwargs overrides self.model.data_filter().

        Parameters:
             **kwargs: filter criteria for deleting
        """
        kwargs = self._join_filter(kwargs)
        if not kwargs:
            raise Exception('Filter criteria are required for deletion!')
        return self.execute(str(self.query.from_(self.table).delete().where(self.__reduce_kwargs(kwargs))))

    def execute(self, statement, **kwargs):
        """Single point to work with database. Executes query strings to database from others methods

        Parameters:
            statement(str): sql query
            **kwargs: kwargs for sqlalchemy engine execute method
        """
        return self.session.execute(statement, **kwargs)

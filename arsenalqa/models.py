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

from collections.abc import MutableMapping

from arsenalqa.base.iterables import ListObject
from arsenalqa.base.utils import Dummy
from arsenalqa.fields import Field


class DataDescriptor:

    def __get__(self, instance, owner):
        if instance is not None:
            if getattr(instance, '_data', None) is None:
                setattr(instance, '_data', {})
            return getattr(instance, '_data')
        return {}

    def __set__(self, instance, value):
        setattr(instance, '_data', value)


class Model(MutableMapping):

    data = DataDescriptor()
    _filter_fields = frozenset()
    _fields = frozenset()

    def __init__(self, **kwargs):
        """
        Parameters:
            kwargs: key-value for flexible instance attributes addition
        """
        for key, value in kwargs.items():
            self[key] = value

    @classmethod
    def transform_incoming_data(cls, data):
        """Method for transform incoming data from transport

        Args:
            data(Any): argument of any type, which should be represented in list or dict.

        Returns:
            Union[list, dict]

        """
        return data

    @classmethod
    def _wrap(cls, data):
        new_class = cls()
        new_class.data = data
        return new_class

    @classmethod
    def wrap(cls, data):
        """Method for wrap incoming data to new instance of model or list of model instances

        Args:
            data(Any): data for wrap. Uses with transform_incoming_data method

        Returns:
            Union[Model, List[Model]]
        """
        data = cls.transform_incoming_data(data)
        if isinstance(data, list):
            return ListObject(wrapper=cls._wrap, data=data)
        return cls._wrap(data)

    def alter(self, keep_fields=None, clean_fields=None, **new_fields) -> 'Model':
        """Creates new model type(AlteredModel) and new instance of AlteredModel.
        Add new or clear current fields for model.

        Args:
            keep_fields(list): if exists all fields except "keep_fields" will be removed
            clean_fields(list): if exists all fields except "clean_fields" will be presented
            **new_fields: add new fields with value to AlteredModel

        Returns:
            AlteredModel

        >>> class MyModel(Model):
        >>>     id = Field()
        >>>     name = Field()
        >>>
        >>> my_model = MyModel()
        >>> my_model.id = 1
        >>> my_model.name = 'test'
        >>> print(my_model.alter(keep_fields=['id']))
        M:{'id': 1}
        >>> print(my_model.alter(clean_fields=['id']))
        M:{'name': 'test'}
        >>> print(my_model.alter(keep_fields=['id'], new_field='new value'))
        M:{'new_field': 'new value', 'id': 1}
        """
        fields = self._fields
        if clean_fields:
            fields -= frozenset(clean_fields)
        if keep_fields:
            fields = keep_fields
        AlteredModel = type(
            'Altered{}'.format(self.__class__.__name__),
            (self.__class__,),
            {i: Field() for i in new_fields.keys()}
        )
        model = AlteredModel.wrap(new_fields)
        [setattr(model, field, getattr(self, field)) for field in fields]
        return model

    @classmethod
    def get_field_key(cls, field):
        """ Returns key name from dict data

        >>> class MyModel(Model):
        >>>
        >>>     id = Field(name='name+id')
        >>>
        >>> my_model = MyModel()
        >>> my_model.id = 1
        >>> print(my_model)
        M:{'name+id': 1}
        >>> print(my_model.id)
        1
        >>> print(MyModel.get_field_key('id'))
        name+id
        """
        return cls.__dict__[field].name

    def model_filter(self):
        """
        >>> class MyModel(Model):
        >>>     id = Field(filter_field=True, name='not_id')
        >>>     name = Field()
        >>>
        >>> my_model = MyModel()
        >>> my_model.id = 1
        >>> my_model.name = 'test'
        >>> print(my_model.model_filter())
        {'id': 1}
        """
        dct = {}
        for i in self._filter_fields:
            try:
                dct[i] = getattr(self, i)
            except AttributeError:
                pass
        return dct

    def data_filter(self):
        """
        >>> class MyModel(Model):
        >>>     id = Field(filter_field=True, name='not_id')
        >>>     name = Field()
        >>>
        >>> my_model = MyModel()
        >>> my_model.id = 1
        >>> my_model.name = 'test'
        >>> print(my_model.data_filter())
        {'not_id': 1}
        """
        dct = {}
        for i in self._filter_fields:
            name = self.get_field_key(i)
            try:
                dct[name] = self.data[name]
            except KeyError:
                pass
        return dct

    def __str__(self):
        return 'M:{}'.format(self.data)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for elem in self._fields:
            if getattr(self, elem, Dummy) != Dummy:
                yield elem

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(f'Model: {self.__class__.__name__} has no Field: {item}')

    def __setitem__(self, key, value):
        if key not in self._fields:
            raise KeyError(f'Model: {self.__class__.__name__} has no Field: {key}')
        setattr(self, key, value)

    def __delitem__(self, key):
        try:
            delattr(self, key)
        except AttributeError:
            raise KeyError(f'Model: {self.__class__.__name__} has no Field: {key}')

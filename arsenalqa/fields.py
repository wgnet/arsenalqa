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

from datetime import datetime, date, time

from dateutil.parser import parse

from arsenalqa.base.iterables import (
    ListObject,
)
from arsenalqa.base.fields import BaseField


class Field(BaseField):
    """
    Parameters:
        name(str): key name for dict data
        filter_field(bool): if True, this field will be used for searching in transports like db or amqp
    """

    def __get__(self, instance, owner):
        if instance is not None:
            try:
                return self._wrap(instance, owner, instance.data[self.name])
            except KeyError:
                raise AttributeError(
                    "'{type}' object has no attribute '{name}'".format(type=instance.__class__.__name__, name=self.name)
                )
            except TypeError:
                raise AttributeError(
                    'list indices must be integers or slices, not str:\n Your data: \n {}'.format(instance.data)
                )
        raise AttributeError(
            "Must be used with '{owner}' instance, not a type.".format(owner=owner.__name__, name=self.name)
        )

    def __set__(self, instance, value):
        instance.data[self.name] = self._unwrap(instance, value)

    def __delete__(self, instance):
        del instance.data[self.name]


class ModelField(Field):
    """
    Parameters:
        model(Model): type for wrap subdict from dict data. If None - wraps subdict in current model
        **kwarg: Field parameters
    """

    def __init__(self, model=None, **kwargs):
        super(ModelField, self).__init__(**kwargs)
        self.model = model

    def chose_wrapper(self, owner):
        return self.model or owner

    def unwrap(self, instance, value):
        return getattr(value, 'data', value)

    def wrap(self, instance, owner, value):
        return self.chose_wrapper(owner).wrap(value)


class ListModelField(ModelField):
    """
    Uses Like ModelField, but for sublist of dicts in dict data
    """

    def unwrap(self, instance, value):
        if isinstance(value, list):
            return [super(ListModelField, self).unwrap(instance, i) for i in value]
        return getattr(value, 'data', value)

    def wrap(self, instance, owner, value):
        return ListObject(data=value, wrapper=self.chose_wrapper(owner).wrap)


class DateTimeField(Field):
    """
    Dates formatting. From dict data reads all datetime formats without mask. For saving used mask parameter fmt

    Parameters:
        fmt(str): mask for saving datetime format
    """

    def __init__(self, fmt='%Y-%m-%dT%H:%M:%S.%f', **kwargs):
        super(DateTimeField, self).__init__(**kwargs)
        self.fmt = fmt

    def unwrap(self, instance, value):
        if isinstance(value, (date, datetime, time)):
            return value.strftime(self.fmt)
        return value

    def wrap(self, instance, owner, value):
        return parse(value)


class TimeStampField(Field):
    """
    Transform datetime to timestamp and back

    Parameters:
        accuracy: number type accuracy for saving in dict data
    """

    def __init__(self, accuracy=float, **kwargs):
        super(TimeStampField, self).__init__(**kwargs)
        self.accuracy = accuracy

    def unwrap(self, instance, value):
        if isinstance(value, datetime):
            return self.accuracy(value.timestamp())
        return value

    def wrap(self, instance, owner, value):
        return datetime.fromtimestamp(float(value))

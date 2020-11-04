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

from collections.abc import MutableSequence

from arsenalqa.base.exceptions import UniqueNotFoundError
from arsenalqa.base.utils import compare_attrs


class ListObject(MutableSequence):

    def __init__(self, data=None, wrapper=None):
        self.data = data or []
        self.wrapper = wrapper or dict

    @staticmethod
    def unwrap(p_object):
        return getattr(p_object, 'data', p_object)

    def wrap(self, elem: dict):
        return self.wrapper(elem)

    def __iter__(self):
        for elem in self.data:
            yield self.wrap(elem)

    def __str__(self):
        return 'I:{}'.format(self.data)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        return self.wrap(self.data[key])

    def __setitem__(self, key, value):
        self.data[key] = self.unwrap(value)

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return bool(self.data)

    def __eq__(self, other):
        for i, j in zip(self, other):
            if i != j:
                return False
        return True

    def append(self, p_object):
        self.data.append(self.unwrap(p_object))

    def filter_by_attrs(self, **attrs):
        result = type(self)(wrapper=self.wrapper)
        for i in self:
            if compare_attrs(i, **attrs):
                result.append(i)
        return result

    def unique_by_attrs(self, **attrs):
        result = self.filter_by_attrs(**attrs)
        if len(result) == 1:
            return result[0]
        raise UniqueNotFoundError(self, attrs, result)

    def unique_by_model(self, model):
        return self.unique_by_attrs(**model.model_filter())

    def get_attrs(self, *attrs):
        return [[getattr(i, j) for j in attrs] for i in self]

    def get_attr(self, attr):
        return [getattr(i, attr) for i in self]

    def pop(self, i=-1):
        return self.data.pop(i)

    def extend(self, listobject):
        self.data.extend([self.unwrap(i) for i in getattr(listobject, 'data', listobject)])

    def insert(self, index, object) -> None:
        self.data.insert(index, getattr(object, 'data', object))
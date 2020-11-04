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

from abc import ABCMeta, abstractmethod


class BaseField:

    __metaclass__ = ABCMeta

    def __init__(self, name=None, filter_field=False):
        self.name = name
        self.filter_field = filter_field

    @abstractmethod
    def __get__(self, instance, owner):
        pass

    @abstractmethod
    def __set__(self, instance, value):
        pass

    def _unwrap(self, instance, value):
        if value is None:
            return value
        return self.unwrap(instance, value)

    def unwrap(self, instance, value):
        return value

    def _wrap(self, instance, owner, value):
        if value is None:
            return value
        return self.wrap(instance, owner, value)

    def wrap(self, instance, owner, value):
        return value

    def __set_name__(self, owner, name):
        owner._fields |= frozenset((name, ))
        if self.filter_field is True:
            owner._filter_fields |= frozenset((name,))
        if self.name is None:
            self.name = name

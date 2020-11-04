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

import importlib


RAW = 'raw'


class Serializer:
    registered = {}

    @classmethod
    def register(cls, name):
        if isinstance(name, str):
            module = importlib.import_module(name)
        else:
            module = name
        cls.registered[name] = module
        return module

    @classmethod
    def get_serializer(cls, name):
        return cls.registered.get(name) or cls.register(name)

    @classmethod
    def dumps(cls, target, serializer=RAW, **kwargs):
        if serializer.lower() == RAW:
            return target
        return cls.get_serializer(serializer).dumps(target, **kwargs)

    @classmethod
    def loads(cls, target, serializer=RAW, **kwargs):
        if serializer.lower() == RAW:
            return target
        return cls.get_serializer(serializer).loads(target, **kwargs)

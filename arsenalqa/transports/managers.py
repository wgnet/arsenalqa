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


class TransportManager:
    """
    Manager for linking transport instance to model instance.
    Otherwise manager creates new transport instance for model class everytime.

    Args:
        transport: Transport type
        **kwargs: named arguments for __init__ method of transport

    >>> class MyModel(Model):
    >>>    http = TransportManager(Http, url='http://example.com')

    >>> my_model = MyModel()
    >>> my_model.http  # One instance Http linked to one MyModel instance
    >>> my_model.http  # Still the same instances
    >>> my_model_class = MyModel
    >>> my_model_class.http  # creates instance Http linked to MyModel class
    >>> my_model_class.http  # creates new instance Http linked to MyModel class
    """

    def __init__(self, transport, **kwargs):
        self.transport = transport
        self.kwargs = kwargs

    def __get__(self, instance, owner):
        transport = self.transport(**self.kwargs)
        if instance is not None:
            setattr(instance, self.name, transport)
            transport.model = instance
            return transport
        transport.model = owner
        return transport

    def __set_name__(self, owner, name):
        self.name = name

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

import asyncio

from arsenalqa.base.transports import BaseTransport
from websockets.client import connect

from arsenalqa.transports import Serializer


class AsyncWebsocket(BaseTransport):

    async def init(self, host=None, url=None, session=None, **kwargs):
        self.session = session or await connect(self.prepare_url(host=host, url=url), **kwargs)

    async def send(self, message=None, serializer=None, **serializer_kwargs):
        return await self.session.send(self.prepare_request(data=message, serializer=serializer, **serializer_kwargs))

    async def recv(self, wrapper=None, serializer=None, timeout=3, **serializer_kwargs):
        return self.prepare_response(
            response=await asyncio.wait_for(self.session.recv(), timeout=timeout),
            wrapper=wrapper,
            serializer=serializer,
            **serializer_kwargs
        )

    def prepare_request(self, data, serializer, **serializer_kwargs):
        serializer = serializer or self.serializer
        data = Serializer.dumps(
            target=data if data is not None else self.model.data,
            serializer=serializer,
            **serializer_kwargs
        )
        return data

    def prepare_response(self, response, wrapper, serializer, **serializer_kwargs):
        serializer = serializer or self.serializer
        wrapper = wrapper or self.model.wrap
        return wrapper(Serializer.loads(target=response, serializer=serializer, **serializer_kwargs))

    async def close(self, *args, **kwargs):
        return await self.session.close(*args, **kwargs)


class WebSocket(AsyncWebsocket):
    
    """
    Parameters:
        host(str): optional first part of url
        url(str): amqp url. Url and host are used if session parameter is None only
        session(websockets.client.connect): optional. Instance of websockets Client
        loop: loop for running websockets async Client
        model(Model): default FakeModel. Model which will be used in transport for send data and wrap response by default
        serializer(str): default "json". Name of serializer module which should have two methods: dumps and loads
    """

    loop = asyncio.get_event_loop()

    def __init__(self, host=None, url=None, session=None, loop=None, **kwargs):
        super(WebSocket, self).__init__(host=host, url=url, **kwargs)
        self.loop = loop or asyncio.get_event_loop()
        self.loop.run_until_complete(self.init(host=host, url=url, session=session, **kwargs))

    def send(self, **kwargs):
        """Method for sending message by websocket

        Parameters:
            message(any): optional. Parameter for overriding self.model. Could be Model type or Python type(dict, list, etc.)
            serializer(str): optional. Parameter for overriding self.serializer
            **serializer_kwargs: optional arguments for serializer module
        """
        return self.loop.run_until_complete(super().send(**kwargs))

    def recv(self, **kwargs):
        """
        Parameters:
            wrapper(callable): callable object for wrapping deserialized response message(usually Model.wrap class method)
            serializer(str): optional. Parameter for overriding self.serializer
            timeout(int): default 3s. If host doesn't sends message in timeout, then client closes connection with exception
            **serializer_kwargs: optional arguments for serializer module
        """
        return self.loop.run_until_complete(super().recv(**kwargs))

    def echo(self, message=None, wrapper=None, serializer=None, timeout=3, **serializer_kwargs):
        """ Method which joins send and recv methods together. Sends message first, then receives response from host

        Parameters:
            message(any): optional. Parameter for overriding self.model. Could be Model type or Python type(dict, list, etc.)
            wrapper(callable): callable object for wrapping deserialized response message(usually Model.wrap class method)
            serializer(str): optional. Parameter for overriding self.serializer
            timeout(int): default 3s. If host doesn't sends message in timeout, then client closes connection with exception
            **serializer_kwargs: optional arguments for serializer module
        """
        self.send(message=message, serializer=serializer, **serializer_kwargs)
        return self.recv(wrapper=wrapper, serializer=serializer, timeout=timeout, **serializer_kwargs)

    def close(self, *args, **kwargs):
        """Method for closing self.session connection

        Parameters:
            *args: args for websockets Client close method
            *kwargs: kwargs for websockets Client close method
        """
        return self.loop.run_until_complete(super().close(*args, **kwargs))

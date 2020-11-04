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

from kombu import Connection, Queue, Producer
from waiter import wait as waiter

from arsenalqa.base.utils import compare_attrs
from arsenalqa.base.iterables import ListObject
from arsenalqa.base.transports import BaseTransport


class Amqp(BaseTransport):
    """
    Parameters:
        host(str): optional first part of url
        url(str): amqp url. Url and host are used if session parameter is None only
        exchange(str): amqp exchange name
        routing_key(str): amqp routing key. Used for queue declaration and message publishing
        queue(str): amqp queue name. Used for queue declaration and getting messages.
        session(kombu.Connection): optional. Instance of kombu Connection object
        model(Model): default FakeModel. Model which will be used in transport for send data and wrap response by default
    """
    
    def __init__(self, host=None, url=None, exchange=None, routing_key=None, queue=None, session=None, **kwargs):
        super(Amqp, self).__init__(host=host, url=url, **kwargs)
        self.exchange = exchange
        self.routing_key = routing_key
        self.queue = queue
        self.session = session or Connection(self.prepare_url(host=host, url=url))

    def choose_arg(self, **kwargs):
        return [j if j is not None else getattr(self, i, None) for i, j in kwargs.items()]

    def declare(self, queue=None, exchange=None, routing_key=None, **kwargs):
        """Queue declaration. All arguments are optional.

        Parameters:
            queue(str): optional. Default self.queue
            exchange(str): optional. Default self.exchange
            routing_key(str): optional. Default self.routing_key
            **kwargs: kombu.Queue.declare parameters

        Returns:
            queue name
        """
        queue, exchange, routing_key = self.choose_arg(queue=queue, exchange=exchange, routing_key=routing_key)
        with self.session as session:
            name = Queue(
                channel=session,
                name=queue,
                exchange=exchange,
                routing_key=routing_key,
                **kwargs
            ).declare()
        return name

    def publish(self, message=None, exchange=None, routing_key=None,  **kwargs):
        """Method for message publishing. All arguments are optional.

        Parameters:
            message(any): optional. Parameter for overriding self.model. Could be Model type or Python type(dict, list, etc.)
            exchange(str): optional. Parameter for overriding self.exchange
            routing_key(str): optional. Parameter for overriding self.routing_key
            **kwargs: kombu.Producer.publish parameters
        """
        exchange, routing_key = self.choose_arg(exchange=exchange, routing_key=routing_key)
        with self.session as session:
            return Producer(channel=session).publish(
                body=self.chose_data(message), exchange=exchange, routing_key=routing_key, **kwargs
            )

    def get(self, **kwargs):
        """Method for getting single filtered message. Raises Exception if messages count != 1. By default this method filters
        message from queue by self.model.model_filter() method + "filter_kwargs"

        Parameters:
            **kwargs: parameters for method all

        Returns:
            prepared response(usually Model instance)
        """
        _kwargs = self.model.model_filter()
        _kwargs.update(kwargs)
        result = self.all(
            **_kwargs
        )
        if len(result) != 1:
            raise Exception('Messages count for get method != 1: {}'.format(result))
        return result[0]

    def all(self, timeout=3, **kwargs):
        """Method for getting list of filtered messages. By default this method filters message from queue by "filter_kwargs"

        Parameters:
            timeout(int): default=3s. How much time to waiting for first message with the same search criteria
            queue(str): default self.queue. Parameter for overriding self.queue
            no_ack(bool): default True. See kombu.Consumer.no_ack attribute
            accept(str): default None. See kombu.Consumer.accept attribute
            wrapper(callable): default sefl.model.wrap. Callable object for wrapping deserialized response.message
            raw_response(bool): default False. If True, method returns raw kombu response. In this case all transformations and checks will be ignored
            **filter_kwargs: kwargs for filter messages from queue by message attributes

        Returns:
            ListObject of Models
        """
        try:
            return waiter([0.1] * 10 * timeout).poll(
                lambda x: x,
                self._all,
                **kwargs
                )
        except StopIteration:
            raise StopIteration(
                'After {timeout}s timeout, there are no results '
                'matching you filter criteria.(Empty List)'.format(timeout=timeout)
            )

    @staticmethod
    def __all_raw(queue, no_ack=True, accept=None):
        lst = []
        while True:
            msg = queue.get(no_ack=no_ack, accept=accept)
            if not msg:
                break
            lst.append(msg)
        return lst

    def __all_wrapped(self, queue, no_ack=True, accept=None, wrapper=None, **filter_kwargs):
        wrapper = wrapper or self.model.wrap
        lst = ListObject(wrapper=wrapper)
        while True:
            msg = queue.get(no_ack=False, accept=accept)
            if not msg:
                break
            model = wrapper(msg.decode())
            if compare_attrs(model, **filter_kwargs):
                lst.append(model)
                if no_ack:
                    msg.ack()
        return lst

    def _all(self, queue=None, no_ack=True, accept=None, wrapper=None, raw_response=False, **filter_kwargs):
        queue, = self.choose_arg(queue=queue)
        with self.session as session:
            queue = Queue(channel=session, name=queue)
            return (
                self.__all_raw(queue, no_ack=no_ack, accept=accept) if raw_response
                else self.__all_wrapped(queue, no_ack=no_ack, accept=accept, wrapper=wrapper, **filter_kwargs)
            )

    def purge(self, queue=None, **kwargs):
        """ Purge queue

        Parameters:
            queue(str): default self.queue. Parameter for overriding self.queue
            **kwargs: kwargs for kombu.Queue.purge method
        """
        queue, = self.choose_arg(queue=queue)
        with self.session as session:
            Queue(channel=session, name=queue).purge(**kwargs)

    def delete(self, queue=None, **kwargs):
        """ Delete queue

        Parameters:
            queue(str): default self.queue. Parameter for overriding self.queue
            **kwargs: kwargs for kombu.Queue.delete method
        """
        queue, = self.choose_arg(queue=queue)
        with self.session as session:
            Queue(channel=session, name=queue).delete(**kwargs)

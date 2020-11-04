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

from requests.sessions import merge_setting
from requests.structures import CaseInsensitiveDict

from requests import Session

from arsenalqa.base.exceptions import assert_response_status
from arsenalqa.base.transports import BaseTransport, FakeModel
from arsenalqa.transports import Serializer


class Http(BaseTransport):
    """
    Parameters:
        host(str): optional first part of url
        url(str): url with "format" like mask: "http://example.com/users/{id}/". In this example "id" takes from model.data. If model attribute "id" will be blank, then url looks like "http://example.com/users/"
        session(requests.Session): optional. Instance of requests Session object
        model(Model): default FakeModel. Model which will be used in transport for send data and wrap response by default
        serializer(str): default "json". Name of serializer module which should have two methods: dumps and loads
    """
    
    def __init__(self, session=None, **kwargs):
        super(Http, self).__init__(session=session or Session(), **kwargs)

    def prepare_request(self, data=None, headers=None, serializer=None, **serializer_kwargs):
        """Method for data preparation before sending. Used in "request" method.

        Parameters:
            data(any): optional. Data for sending. If None, then self.model will be used
            headers(dict): optional. Parameter for overriding default requests.Session.headers
            serializer(str): optional. Parameter for overriding self.serializer
            **serializer_kwargs: optional arguments for serializer module

        Returns:
            serialized data, headers
        """
        data = Serializer.dumps(
            target=self.chose_data(data),
            serializer=serializer, **serializer_kwargs
        )
        headers = headers or {}
        return data, headers

    def prepare_response(self,
                         response,
                         method,
                         url,
                         expected_status,
                         wrapper,
                         headers,
                         params,
                         data,
                         raw_response,
                         serializer,
                         **serializer_kwargs
                         ):
        """Method for response preparation before returning. Used in "request" method

        Parameters:
            response(requests.Response): raw response from web
            expected_status(int): optional. Status for response assertion. If None assertion will be skipped
            wrapper(callable): callable object for wrapping deserialized response.content(usually Model.wrap class method)
            raw_response(bool): if True, method returns requests.Response object. In this case all transformations and checks will be ignored
            ------------------------------------
            method: request parameter for Assertion error report
            url: request parameter for Assertion error report
            headers: request parameter for Assertion error report
            params: request parameter for Assertion error report
            data: request parameter for Assertion error report
            ------------------------------------
            serializer(str): optional. Parameter for overriding self.serializer
            **serializer_kwargs: optional arguments for serializer module

        Returns:
            prepared response(usually Model instance)
        """
        if raw_response:
            return response
        wrapper = wrapper or self.model.wrap
        assert_response_status(
            response=response,
            method=method,
            url=url,
            expected_status=expected_status,
            headers=headers,
            params=params,
            data=data,
        )
        return wrapper(Serializer.loads(target=response.content, serializer=serializer, **serializer_kwargs))

    def get(self, **kwargs):
        """Http GET method

        Parameters:
            **kwargs: parameters for request method.
        """
        return self.request('GET', **kwargs)

    def post(self, **kwargs):
        """Http POST method

        Parameters:
            **kwargs: parameters for request method.
        """
        return self.request('POST', **kwargs)

    def options(self, **kwargs):
        """Http OPTIONS method

        Parameters:
            **kwargs: parameters for request method.
        """
        return self.request('OPTIONS', **kwargs)

    def head(self, **kwargs):
        """Http HEAD method

        Parameters:
            **kwargs: parameters for request method.
        """
        return self.request('HEAD', **kwargs)

    def put(self, **kwargs):
        """Http PUT method

        Parameters:
            **kwargs: parameters for request method.
        """
        return self.request('PUT', **kwargs)

    def patch(self, **kwargs):
        """Http PATCH method

        Parameters:
            **kwargs: parameters for request method.
        """
        return self.request('PATCH', **kwargs)

    def delete(self, **kwargs):
        """Http DELETE method

        Parameters:
            **kwargs: parameters for request method.
        """
        return self.request('DELETE', **kwargs)

    def request(self, method=None, url=None, data=None, headers=None,
                expected_status=None, wrapper=None, raw_response=False,
                params=None, serializer=None, host=None, **kwargs):
        """Main method for data transformation and transferring

        Parameters:
            method(str): http method name
            host(str): optional. Parameter for overriding self.host
            url(str): optional. Parameter for overriding self.url
            data(any): optional. Parameter for overriding self.model. Could be Model type or Python type(dict, list, etc.)
            headers(dict): optional. Parameter for merging with Session.headers
            expected_status(int): optional. Status for response assertion. If None assertion will be skipped
            wrapper(callable): default sefl.model.wrap. Callable object for wrapping deserialized response.content
            raw_response(bool): default False. If True, method returns requests.Response object. In this case all transformations and checks will be ignored
            params(dict): optional. requsts.Session.get params parameter
            serializer(str): optional. Parameter for overriding self.serializer
            **kwargs: requests.Session.request method kwargs

        Returns:
            prepared response(usually Model instance)
        """
        serializer = serializer or self.serializer
        url = self.prepare_url(host, url)
        data, headers = self.prepare_request(data=data, headers=headers, serializer=serializer)
        _response = self.session.request(method=method, url=url, data=data, headers=headers, params=params, **kwargs)
        response = self.prepare_response(
            response=_response,
            method=method,
            url=url,
            expected_status=expected_status,
            wrapper=wrapper,
            headers=merge_setting(headers, self.session.headers, dict_class=CaseInsensitiveDict),
            params=merge_setting(params, self.session.params),
            data=data,
            raw_response=raw_response,
            serializer=serializer
        )
        return response

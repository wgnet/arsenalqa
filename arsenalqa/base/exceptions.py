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


def assert_response_status(method, url, headers, params, data, response, expected_status):
    if expected_status and expected_status != response.status_code:
        error = ResponseStatusAssertionError(
            method, url, headers, params, data, response.content, expected_status, response.status_code
        )
        raise error


class ResponseStatusAssertionError(AssertionError):

    def __init__(self, method, url, headers, params, data, response, expected_status, actual_status):
        self.response = response
        self.expected_status = expected_status
        self.actual_status = actual_status
        self.method = method
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        super(ResponseStatusAssertionError, self).__init__(self.message)

    @property
    def message(self):
        return (
            '\nMethod: {}\nResponse: {}\nExpected response code: {}\n'
            'Actual response code: {}\nUrl: {}\nHeaders: {}\nParams: {}\nData: {}\n'.format(
                self.method,
                self.response,
                self.expected_status,
                self.actual_status,
                self.url,
                self.headers,
                self.params,
                self.data
            )
        )


class UniqueNotFoundError(ValueError):
    
    def __init__(self, obj, kwargs, result):
        msg = 'Unique object not found!\n' \
              'List: {obj}\n' \
              'Filter: {kwargs}\n' \
              'Result: {result}'.format(kwargs=kwargs, obj=obj, result=result)
        super(UniqueNotFoundError, self).__init__(msg)
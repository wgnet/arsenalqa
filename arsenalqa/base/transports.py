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

from urllib.parse import urljoin, urlparse

from arsenalqa.base.utils import SafeFormatDict
from arsenalqa.models import Model


class FakeModel(Model):

    @classmethod
    def wrap(cls, data):
        return data


class BaseTransport:

    def chose_data(self, data):
        if data is not None:
            return getattr(data, 'data', data)
        return getattr(self.model, 'data', self.model)

    def __init__(self, host=None, url=None, session=None, model=None, serializer='json'):
        self.session = session
        self.host = host
        self.url = url
        self.model = model if model is not None else FakeModel()
        self.serializer = serializer

    def prepare_url(self, host=None, url=None):
        host = host or self.host
        url = url or self.url
        url = urljoin(host, url)
        url = urlparse(url.format_map(SafeFormatDict(self.model)))
        url = url._replace(path=url.path.replace('//', '/'))
        return url.geturl()


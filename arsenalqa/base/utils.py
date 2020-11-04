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


def compare_attrs(instance, **attrs):
    for j, k in attrs.items():
        if getattr(instance, j, None) != k:
            return False
    return True


class SafeFormatDict(dict):

    def __init__(self, seq):
        try:
            super(SafeFormatDict, self).__init__(seq)
        except TypeError:
            super(SafeFormatDict, self).__init__(getattr(seq, 'data', {}))

    def __missing__(self, key):
        return ''


class Dummy:
    pass

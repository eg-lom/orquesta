# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import six

from stevedore import extension

from orchestra import states


def register_functions(ctx):
    mgr = extension.ExtensionManager(
        namespace='orchestra.expressions.functions',
        invoke_on_load=False
    )

    registered = []

    for name in mgr.names():
        try:
            func = mgr[name].plugin
            ctx.register_function(func, name=name)
            registered.append(name)
        except Exception:
            continue

    return registered


def json_(s):
    if isinstance(s, dict):
        return s

    if not isinstance(s, six.string_types):
        raise TypeError('Given object is not typeof string.')

    return json.loads(s)


def task_state_(context, task_name):
    task_states = context['__task_states'] or {}

    return task_states.get(task_name, states.UNKNOWN)
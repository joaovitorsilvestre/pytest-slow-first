=================
pytest-slow-first
=================

.. image:: https://img.shields.io/pypi/v/pytest-slow-first.svg
    :target: https://pypi.org/project/pytest-slow-first
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-slow-first.svg
    :target: https://pypi.org/project/pytest-slow-first
    :alt: Python versions

.. image:: https://ci.appveyor.com/api/projects/status/github/joaovitorsilvestre/pytest-slow-first?branch=master
    :target: https://ci.appveyor.com/project/joaovitorsilvestre/pytest-slow-first/branch/master
    :alt: See Build Status on AppVeyor

## What it does?

Allow to run your test suite with tests ordered by their duration on last successful run.

## How it can make your suite run faster?

Before all, these benefits only appear when running this plugin alongside with [pytest-xdist](https://github.com/pytest-dev/pytest-xdist).

Imagine a suit with 6 tests. Each one takes some amount of time to run. Ex:

<img src="./docs/assets/test_suite.png?raw=true" alt="Alt text" title="Optional title" style="width: 60% !important;">

By running this suite with Xdist with 2 workers, running tests at default order, the load of each worker will be like:

<img src="./docs/assets/only_xdist.png?raw=true" alt="Alt text" title="Optional title"  style="width: 70% !important;">

The problem with this approath is that demanding tests very often will go to same worker.

When this happens, the total time spend running your suit will be longer that necessary, because, as you can se in the above image,
there are workers hanging without any more tests to run.

<img src="./docs/assets/xdist_and_slow_first.png?raw=true" alt="Alt text" title="Optional title"  style="width: 60% !important;">

Requirements
------------

* TODO


Installation
------------

You can install "pytest-slow-first" via `pip`_ from `PyPI`_::

    $ pip install pytest-slow-first


Usage
-----
```python
import os
import json

def slow_first_save_durations(durations_data: str):
    assert json.loads(durations_data)
    with open('{file_to_save}', 'w') as f:
        f.write(durations_data)

def slow_first_load_durations():
    if os.path.exists('{file_to_save}'):
        with open('{file_to_save}', 'r') as f:
            return f.read()
```

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-slow-first" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/joaovitorsilvestre/pytest-slow-first/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project

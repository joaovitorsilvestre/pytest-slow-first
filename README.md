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

Allow to run the

----

Features
--------

![Alt text](./docs/assets/test_suite.png?raw=true "Title")

![Alt text](./docs/assets/only_xdist.png?raw=true "Title")

![Alt text](./docs/assets/xdist_and_slow_first.pn?raw=true "Title")

![plot](./docs/assets/xdist_and_slow_first.pn?raw=true)

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

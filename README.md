# pytest-slow-first

[![PyPI Version](https://img.shields.io/pypi/v/pytest-slow-first.svg?raw=True)](https://pypi.org/project/pytest-slow-first/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pytest-slow-first.svg?raw=True)](https://pypi.org/project/pytest-slow-first/)

## Overview

`pytest-slow-first` is a pytest plugin that optimizes test suite execution by sorting tests based on their duration from the last run. This ensures that slower tests run first, leading to more efficient utilization of resources when used in conjunction with [pytest-xdist](https://github.com/pytest-dev/pytest-xdist).

## How It Works

When running your test suite with this plugin, it saves the duration of each test in a file. On subsequent runs, tests are sorted based on the time they took to execute in the last run. This sorting minimizes the overall test suite execution time.

Running tests with `pytest-xdist` with multiple workers, evenly distributing slower tests among workers becomes crucial. Without this plugin, the default order may lead to inefficient resource utilization. `pytest-slow-first` addresses this issue by ensuring that slower tests are evenly distributed, reducing the total execution time.

### Example

Consider a test suite with six tests, each taking varying amounts of time to run:
<img src="https://github.com/joaovitorsilvestre/pytest-slow-first/blob/master/docs/assets/test_suite.png?raw=true" alt="Suite with 6 tests and their times" title="Example of test suite" style="width: 60% !important;">

Running this suite with two workers using only `pytest-xdist` might result in uneven distribution:

<img src="https://github.com/joaovitorsilvestre/pytest-slow-first/blob/master/docs/assets/only_xdist.png?raw=true" alt="Suite running with xdist" title="Only xdist" style="width: 70% !important;">

However, with `pytest-slow-first`, the same suite will be executed more efficiently and takes less time to finish, as shown below:

<img src="https://github.com/joaovitorsilvestre/pytest-slow-first/blob/master/docs/assets/xdist_and_slow_first.png?raw=true" alt="Suite with 6 tests running with xdist + slow-first" title="Xdist + slow-first" style="width: 60% !important;">

## Usage

To use `pytest-slow-first` alongside `pytest-xdist`, simply add the `--slow-first` option:

```bash
pytest tests --slow-first -n3  # using along side xdist
```

The plugin initializes by running your suite as usual the first time. On subsequent runs, it sorts tests based on the time taken in the previous run.

### Multiple runs
The plugin's results file is cumulative. If a test run already exists in the file, its duration will be updated.

### Custom File Location
By default, the plugin saves test durations in a file named pytest-slow-first.json in the current directory. You can change the location by setting the SLOW_FIRST_PATH environment variable:

```bash
export SLOW_FIRST_PATH=/tmp/pytest-slow-first.json pytest --slow-first
```

Installation
------------

You can install "pytest-slow-first" via `pip`:

    $ pip install pytest-slow-first

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT` license, "pytest-slow-first" is free and open source software.


Issues
------

If you encounter any problems, please `file an issue` along with a detailed description.

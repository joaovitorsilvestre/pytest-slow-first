pytest-slow-first
=================

![Python versions](https://img.shields.io/pypi/v/pytest-slow-first.svg?raw=True)
![Python versions](https://img.shields.io/pypi/pyversions/pytest-slow-first.svg?raw=True)

## What it does?

Execute your test suite with tests ordered by their durations on last successful run.

</br>
</hr>

## How it can make your suite run faster?

Before all, these benefits only appear when running this plugin alongside with [pytest-xdist](https://github.com/pytest-dev/pytest-xdist).

Taking this into acount, now imagine a suite with 6 tests. Each one takes some amount of time to run. Ex:

<img src="./docs/assets/test_suite.png?raw=true" alt="Alt text" title="Optional title" style="width: 60% !important;">

By running this suite with Xdist with 2 workers, tests at default order, the load of each worker would be like:

<img src="./docs/assets/only_xdist.png?raw=true" alt="Alt text" title="Optional title"  style="width: 70% !important;">

The problem with this approath is that demanding tests very often will go to same worker.

When this happens, the total time spend running your suit will be longer that necessary, because, as you can se in the above image,
there are workers hanging without any more tests to run.

This plugin will ensure that slowers tests run first and the total duration of the same suite will look like this:

<img src="./docs/assets/xdist_and_slow_first.png?raw=true" alt="Alt text" title="Optional title"  style="width: 60% !important;">

### How it works?

This plugin will save the duration of each of your tests in a file or wherever you want. 
In the next time you run it, tests will be sorted by time spend in the last run, making your whole suite take less time to complete. 

</br>
</hr>

Usage
-----

You just need to define two functions inside your conftest.py file: `slow_first_save_durations` and `slow_first_load_durations`.

The first one is to save results of current run and the second one is to load the same results in the folowing run. Allowing this plugin to sort execuntion of tests based in these results.

Example of `conftest.py` file:
```python
import os, json


def slow_first_load_durations():
    if os.path.exists('/tmp/tests_duration'):
        with open('/tmp/tests_duration', 'r') as f:
            return f.read()
    else:
        # Durations not found. Run with default order
        return None

def slow_first_save_durations(durations_data: str):
    with open('/tmp/tests_duration', 'w') as f:
        f.write(durations_data)
```

#### Explanation

1. First, `slow_first_load_durations` will be called before your tests starts running, it will load the durantion of the tests
of the previous run. 

    * **obs**: if its the first time using this plugin or if you can't load the results, this function must return None.

2. If `slow_first_load_durations` finds data, it returns the content and slow-first plugin will sort your tests, otherwise 
the test suite will run at default order.

3. If the suit runs with success, `slow_first_save_durations` is going to be called with durations as argument. This function must save the results
in a way that `slow_first_load_durations` can load in the next run.

### Running with pytest-slow-first plugin
Finally, activate the plugin by passing `--slow-first` as paramter of pytest command:

```bash
pytest tests --slow-first -n3  # using along side xdist
```

</br>
</hr>

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

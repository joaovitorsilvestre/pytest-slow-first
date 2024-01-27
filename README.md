pytest-slow-first
=================

![Python versions](https://img.shields.io/pypi/v/pytest-slow-first.svg?raw=True)
![Python versions](https://img.shields.io/pypi/pyversions/pytest-slow-first.svg?raw=True)

## What it does?

Sort tests by their duration on the last run. Making slow tests run first.
</br>
</hr>

## How can it make your suite run faster?

Before all, these benefits only appear when running this plugin alongside with [pytest-xdist](https://github.com/pytest-dev/pytest-xdist).

Taking this into acount, now imagine a suite with 6 tests. Each one takes some amount of time to run. Ex:

<img src="./docs/assets/test_suite.png?raw=true" alt="Alt text" title="Optional title" style="width: 60% !important;">

By running this suite with Xdist with 2 workers, tests at default order, the load of each worker would be like:

<img src="./docs/assets/only_xdist.png?raw=true" alt="Alt text" title="Optional title"  style="width: 70% !important;">

The problem with this approath is that demanding tests very often will go to same worker.

When this happens, the total time spend running your suit will be longer that necessary, because, as you can se in the above image,
there are workers hanging without any more tests to run.

This plugin will ensure that slowers tests run first and are evenly distributed between workers. Now the execution of the same suite will look like this:

<img src="./docs/assets/xdist_and_slow_first.png?raw=true" alt="Alt text" title="Optional title"  style="width: 60% !important;">

### How it works?

This plugin will save the duration of each of your tests in a file or wherever you want. 
In the next time you run it, tests will be sorted by time spend in the last run, making your whole suite take less time to complete. 

</br>
</hr>

### Running with pytest-slow-first plugin
Finally, activate the plugin by passing `--slow-first` as paramter of pytest command:

```bash
pytest tests --slow-first -n3  # using along side xdist
```

</br>
</hr>

THis plugin will save the duration of each of your tests in a file named `pytest-slow-first.json` in the current directory.
You can change the location by setting the enviroment variable `SLOW_FIRST_PATH` to the path you want.
Ex: `export SLOW_FIRST_PATH=/tmp/pytest-slow-first.json pytest --slow-first`

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

# -*- coding: utf-8 -*-
import json

from _pytest.config import ExitCode


def test_enabled_slow_first(testdir):
    from pytest_slow_first import SlowFirst

    testdir.makepyfile("""
        from time import sleep
    
        def test1():
            sleep(0.1)
            
        def test2():
            sleep(0.3)
        
        def test3():
            sleep(0.2)
    """)

    file_to_save = testdir.tmpdir.join('pytest-slow-first.json')

    testdir.makeconftest("")

    # 1º theres no previous durention saved, the first run will run
    # tests in the order they are defined
    result = testdir.runpytest('--slow-first', '-v')

    result.stdout.fnmatch_lines([
        '*::test1 PASSED*',
        '*::test2 PASSED*',
        '*::test3 PASSED*',
    ])
    assert result.ret == 0

    with open(f'{file_to_save}', 'r') as f:
        slow_first = SlowFirst.deserialize(f.read())
        assert (
            slow_first.get_order('test_enabled_slow_first.py::test2') >
            slow_first.get_order('test_enabled_slow_first.py::test3') >
            slow_first.get_order('test_enabled_slow_first.py::test1')
        )

    # 2º Run tests again. Now tests must run in the order of the durations
    result = testdir.runpytest('--slow-first', '-v')

    result.stdout.fnmatch_lines([
        '*::test2 PASSED*',
        '*::test3 PASSED*',
        '*::test1 PASSED*',
    ])
    assert result.ret == 0

    # 3º Run again, but without the slow first plugin.
    # Tests must run in normal order
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines([
        '*::test1 PASSED*',
        '*::test2 PASSED*',
        '*::test3 PASSED*',
    ])
    assert result.ret == 0


def test_different_format(testdir):
    from pytest_slow_first import SlowFirst

    testdir.makepyfile("""
        def test1():
            sleep(0.1)
    """)

    file_oprevious_run = testdir.tmpdir.join('pytest-slow-first.json')
    with open(f'{file_oprevious_run}', 'w') as f:
        json.dump({"format_version": "0.0.1", "tests": []}, f)

    testdir.makeconftest("")

    # 1º Must exit with error because the format version is not compatible
    result = testdir.runpytest('--slow-first', '-v')

    assert result.ret == ExitCode.USAGE_ERROR

# -*- coding: utf-8 -*-
import importlib
import json
import logging
import os
from typing import Union, Dict

import pytest
from _pytest.config import ExitCode

FORMAT_VERSION = '1.0.0'
SLOW_FIRST_PATH = os.environ.get('SLOW_FIRST_PATH', 'pytest-slow-first.json')


def log_slow_first(message: str):
    logging.getLogger().info(f"[pytest-slow-first] {message}")


class SlowFirstRequiredFunctionNotImplemented(Exception):
    pass


class ConftestModuleNotFound(Exception):
    pass


def _get_slow_first_from_config(config):
    return getattr(config, 'slow_first')


class Test:
    nodeid: str
    setup_duration: Union[float, None]
    call_duration: Union[float, None]
    teardown_duration: Union[float, None]

    def __init__(self, nodeid: str, setup_duration: float = None, call_duration: float = None, teardown_duration: float = None):
        self.nodeid = nodeid
        self.setup_duration = setup_duration
        self.call_duration = call_duration
        self.teardown_duration = teardown_duration

    @property
    def total_duration(self) -> float:
        return self.setup_duration + self.call_duration + self.teardown_duration

    def set_duration(self, kind: str, duration: float):
        setattr(self, f"{kind}_duration", duration)

    def serialize(self) -> Dict[str, Union[str, float]]:
        return {'nodeid': self.nodeid, 'setup_duration': self.setup_duration,
                'call_duration': self.call_duration, 'teardown_duration': self.teardown_duration}

    @staticmethod
    def deserialize(data: dict) -> "Test":
        return Test(**data)


class SlowFirst:
    _tests_by_name: Dict[str, Test]
    enabled: bool

    def __init__(self, tests_by_name: Dict[str, Test] = None, enabled: bool = False):
        self._tests_by_name = tests_by_name or {}
        self.enabled = enabled

    def save(self):
        log_slow_first("Saving testes durations")
        with open(SLOW_FIRST_PATH, 'w') as f:
            f.write(self.serialize())

    @staticmethod
    def load():
        if os.path.exists(SLOW_FIRST_PATH):
            with open(SLOW_FIRST_PATH, 'r') as f:
                data = f.read()
            log_slow_first("Loaded testes durations from previous run. Applying order")
        else:
            log_slow_first("No previous run found. Skipping order")
            return None

        return SlowFirst.deserialize(data)

    def serialize(self) -> str:
        return json.dumps({
            'format_version': FORMAT_VERSION,
            'tests': [test.serialize() for test in self._tests_by_name.values()]
        })

    @staticmethod
    def deserialize(data: str) -> "SlowFirst":
        data = json.loads(data)

        if data['format_version'] != FORMAT_VERSION:
            pytest.exit(
                reason=f"[pytest-slow-first] The format version of {SLOW_FIRST_PATH} "
                       f"is not compatible with this version of pytest-slow-first. "
                       f"Please delete {SLOW_FIRST_PATH} and run tests again.",
                returncode=ExitCode.USAGE_ERROR
            )

        return SlowFirst({test.nodeid: test for test in map(Test.deserialize, data['tests'])})

    def set_duration(self, name: str, kind: str, duration: float):
        test = self._tests_by_name.get(name)

        if test:
            test.set_duration(kind, duration)
        else:
            test = Test(name)
            self._tests_by_name[test.nodeid] = test
            test.set_duration(kind, duration)

    def get_order(self, test_name: str) -> float:
        test = self._tests_by_name.get(test_name)
        if test:
            return test.total_duration
        else:
            return 0


def pytest_addoption(parser):
    group = parser.getgroup('slow-first')
    group.addoption(
        '--slow-first',
        action='store_true',
        dest='slow_first',
        default=False,
        help='Enable pytest-slow-first plugin and prioritize running the slowest tests first.'
    )


def pytest_collection_modifyitems(session, config, items):
    slow_first = _get_slow_first_from_config(config)

    if not slow_first.enabled:
        return

    prev_run_slow_first = SlowFirst.load()

    if prev_run_slow_first:
        logging.getLogger().info("Sorting tests by durations from last run")
        items.sort(
            key=lambda item: prev_run_slow_first.get_order(item.nodeid),
            reverse=True
        )


def pytest_report_teststatus(report, config):
    if report.passed is True:
        _get_slow_first_from_config(config).set_duration(report.nodeid, report.when, report.duration)


def pytest_sessionstart(session):
    using_slow_first = session.config.getoption('--slow-first')
    setattr(session.config, 'slow_first', SlowFirst(enabled=using_slow_first))


def pytest_terminal_summary(exitstatus, config):
    slow_first = _get_slow_first_from_config(config)

    if exitstatus == 0:
        slow_first.save()

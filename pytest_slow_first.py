# -*- coding: utf-8 -*-
import importlib
import json
import logging


class SlowFirstRequiredFunctionNotImplemented(Exception):
    pass


class ConftestModuleNotFound(Exception):
    pass


def _get_slow_first_from_config(config):
    return getattr(config, 'slow_first')


class Test:
    def __init__(self, name, setup_duration: float = None, call_duration: float = None, teardown_duration: float = None):
        self.name = name
        self.setup_duration = setup_duration
        self.call_duration = call_duration
        self.teardown_duration = teardown_duration

    @property
    def total_duration(self):
        return self.setup_duration + self.call_duration + self.teardown_duration

    def set_duration(self, kind: str, duration: float):
        setattr(self, f"{kind}_duration", duration)

    def serialize(self):
        return {'name': self.name, 'setup_duration': self.setup_duration,
                'call_duration': self.call_duration, 'teardown_duration': self.teardown_duration}

    @staticmethod
    def deserialize(data: dict):
        test = Test(data['name'])
        test.setup_duration = data['setup_duration']
        test.call_duration = data['call_duration']
        test.teardown_duration = data['teardown_duration']
        return test


class SlowFirst:
    def __init__(self, tests_by_name: dict = None, enabled: bool = False):
        self._tests_by_name = tests_by_name or {}
        self.enabled = enabled

        if enabled:
            self._validate_conftest_functions_are_defined()

    def save(self):
        logging.getLogger().info("Saving testes durations")
        self._get_conftest_module().slow_first_save_durations(self.serialize())

    @staticmethod
    def load():
        logging.getLogger().info("Loading testes durations of previous run")
        data = SlowFirst._get_conftest_module().slow_first_load_durations()

        if not data:
            return None

        return SlowFirst.deserialize(data)

    def serialize(self) -> str:
        return json.dumps(list(map(Test.serialize, self._tests_by_name.values())))

    @staticmethod
    def deserialize(data: str):
        return SlowFirst({test.name: test for test in map(Test.deserialize, json.loads(data))})

    def set_duration(self, name: str, kind: str, duration: float):
        test = self._tests_by_name.get(name)

        if test:
            test.set_duration(kind, duration)
        else:
            test = Test(name)
            self._tests_by_name[test.name] = test
            test.set_duration(kind, duration)

    def get_order(self, test_name: str):
        test = self._tests_by_name.get(test_name)
        if test:
            return test.total_duration
        else:
            return 0

    @staticmethod
    def _get_conftest_module():
        return importlib.import_module('conftest')

    @staticmethod
    def _validate_conftest_functions_are_defined():
        try:
            conftest = SlowFirst._get_conftest_module()
        except ModuleNotFoundError as e:
            raise ConftestModuleNotFound('slow_first plugin was not able to load conftest module') from e

        if not hasattr(conftest, 'slow_first_save_durations'):
            raise SlowFirstRequiredFunctionNotImplemented(
                'slow_first_save_durations function is not defined in conftest.py'
            )

        if not hasattr(conftest, 'slow_first_load_durations'):
            raise SlowFirstRequiredFunctionNotImplemented(
                'slow_first_load_durations function is not defined in conftest.py'
            )


def pytest_addoption(parser):
    group = parser.getgroup('slow-first')
    group.addoption(
        '--slow-first',
        action='store_true',
        dest='slow_first',
        default=False,
        help='If given, will enable tests sorting by durations from last run.'
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

import os
import sys
from contextlib import contextmanager
from typing import Optional, List, Tuple

import pytest

from flywheel.runner_pytest.abstract_class import AbstractRunnerPytest


class RunnerPytest1(AbstractRunnerPytest):
    def __init__(self):
        self._failures = []

    def get_pytest_failure(self, n: int, module: str) -> Tuple[str, str]:
        self._run_tests(module)
        failure_detail = self._retrieve_nth_failure_result(n)
        test_code = self._retrieve_test_code_from_failure(n)
        return failure_detail, test_code

    @contextmanager
    def _suppress_output(self):
        original_stdout, original_stderr = sys.stdout, sys.stderr
        with open(os.devnull, 'w') as fnull:
            sys.stdout = fnull
            sys.stderr = fnull
            yield
        sys.stdout, sys.stderr = original_stdout, original_stderr

    def _get_pytest_args(self, test_file: str, implementation_number: Optional[int]) -> List[str]:
        implementation = implementation_number if implementation_number is not None else 'default'
        return [test_file, f"--implementation={implementation}"]

    def _run_tests(self, test_file: str, implementation_number: Optional[int] = None) -> None:
        with self._suppress_output():
            plugins = [self._ResultCollector(self._failures)]
            pytest_args = self._get_pytest_args(test_file, implementation_number)
            pytest.main(pytest_args, plugins=plugins)

    def _retrieve_nth_failure_result(self, n: int) -> str:
        return self._failures[n].longreprtext

    def _retrieve_test_code_from_failure(self, n: int) -> str:
        # Implement code to retrieve the test code
        # This is a placeholder, add actual logic to get the test code
        return "Test code placeholder"

    class _ResultCollector:
        def __init__(self, failures):
            self._failures = failures

        def pytest_runtest_logreport(self, report):
            if report.failed:
                self._failures.append(report)

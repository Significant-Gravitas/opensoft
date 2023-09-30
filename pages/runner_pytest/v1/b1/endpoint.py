import os
import sys
from contextlib import contextmanager
from typing import List, Optional

import pytest
from fastapi import APIRouter

from pages.runner_pytest.v1.models import AbstractRunnerPytest

# from pages.runner_pytest.models import AbstractRunnerPytest

router = APIRouter()


from fastapi import Query


@router.get("/pytest_failures/")
def get_pytest_failures(n: int = Query(...), path: Optional[str] = None):
    return RunnerPytest1().get_pytest_failure(n, path)


class RunnerPytest1(AbstractRunnerPytest):
    def __init__(self):
        self._failures = []

    def get_pytest_failure(self, n: int, path: str) -> str:

        self._run_tests(path)
        failure_detail = self._retrieve_nth_failure_result(n)
        return failure_detail

    @contextmanager
    def _suppress_output(self):
        original_stdout, original_stderr = sys.stdout, sys.stderr
        with open(os.devnull, "w") as fnull:
            sys.stdout = fnull
            sys.stderr = fnull
            yield
        sys.stdout, sys.stderr = original_stdout, original_stderr

    def _get_pytest_args(
        self, test_path: str, implementation_number: Optional[int]
    ) -> List[str]:

        implementation = (
            implementation_number if implementation_number is not None else "default"
        )
        return [test_path, f"--implementation={implementation}"]

    def _run_tests(
        self,
        test_path: str = None,
        implementation_number: Optional[int] = None,  # Make test_path default to None
    ) -> None:

        with self._suppress_output():
            if test_path:  # Only adjust the path if it's provided
                test_path = os.path.relpath(test_path, os.getcwd())

            plugins = [self._ResultCollector(self._failures)]
            current_file_dir = os.path.dirname(os.path.realpath(__file__))
            parent_dir = os.path.dirname(current_file_dir)

            pytest_args = (
                [test_path, "--mock"] if test_path else ["--mock"]
            )  # Adjust pytest arguments based on test_path

            pytest.main(pytest_args, plugins=plugins)

    def _retrieve_nth_failure_result(self, n: int) -> str:
        if len(self._failures) > n:
            return self._failures[n].longreprtext
        else:
            return None

    class _ResultCollector:
        def __init__(self, failures):
            self._failures = failures

        def pytest_runtest_logreport(self, report):
            print(f"Test {report.nodeid} ended with {report.outcome}")
            if report.failed:
                self._failures.append(report)

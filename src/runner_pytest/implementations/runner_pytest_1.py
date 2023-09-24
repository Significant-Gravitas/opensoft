import os
import re
import sys
from contextlib import contextmanager
from typing import List, Optional, Tuple

import pytest

from src.runner_pytest.abstract_class import AbstractRunnerPytest


class RunnerPytest1(AbstractRunnerPytest):
    def __init__(self):
        self._failures = []

    def get_pytest_failure(self, n: int, path: str) -> Tuple[str, str]:

        self._run_tests(path)
        failure_detail = self._retrieve_nth_failure_result(n)
        test_code = self._retrieve_test_code_from_failure(n)
        return failure_detail, test_code

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
        self, test_path: str, implementation_number: Optional[int] = None
    ) -> None:

        with self._suppress_output():
            test_path = os.path.relpath(test_path, os.getcwd())

            plugins = [self._ResultCollector(self._failures)]
            current_file_dir = os.path.dirname(os.path.realpath(__file__))
            parent_dir = os.path.dirname(current_file_dir)

            pytest_args = [test_path, "--mock"]

            pytest.main(pytest_args, plugins=plugins)

    def _retrieve_nth_failure_result(self, n: int) -> str:
        if len(self._failures) > n:
            return self._failures[n].longreprtext
        else:
            return None

    def _retrieve_test_code_from_failure(self, n: int) -> str:
        if len(self._failures) > n:
            report = self._failures[n]

            if (
                hasattr(report.longrepr, "reprtraceback")
                and hasattr(report.longrepr.reprtraceback, "reprentries")
                and report.longrepr.reprtraceback.reprentries
            ):
                test_code_lines = report.longrepr.reprtraceback.reprentries[0].lines
                test_code = "\n".join(test_code_lines)
                return test_code

            test_name_raw = report.nodeid.split("::")[-1]
            test_name_match = re.match(r"(\w+)", test_name_raw)
            if not test_name_match:
                return None
            test_name = test_name_match.group(1)

            test_file_path = (
                report.longrepr.reprcrash.path
                if hasattr(report.longrepr, "reprcrash")
                else str(report.longrepr.filename)
            )

            with open(test_file_path, "r") as f:
                lines = f.readlines()

            test_code = ""
            inside_test = False
            for line in lines:
                if f"def {test_name}(" in line:
                    inside_test = True
                if inside_test:
                    test_code += line
                if (
                    inside_test
                    and f"def {test_name}(" not in line
                    and "def test_" in line
                ):
                    break

            return test_code
        else:
            return None

    class _ResultCollector:
        def __init__(self, failures):
            self._failures = failures

        def pytest_runtest_logreport(self, report):
            print(f"Test {report.nodeid} ended with {report.outcome}")
            if report.failed:
                self._failures.append(report)

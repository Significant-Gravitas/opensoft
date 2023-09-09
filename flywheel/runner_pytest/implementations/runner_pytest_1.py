import os
import re
import sys
from contextlib import contextmanager
from typing import Optional, List, Tuple

import pytest

from flywheel.runner_pytest.abstract_class import AbstractRunnerPytest


class RunnerPytest1(AbstractRunnerPytest):
    def __init__(self):
        self._failures = []

    def get_pytest_failure(self, n: int, path: str) -> Tuple[str, str]:
        # Changed from module to path
        self._run_tests(path)
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

    def _get_pytest_args(self, test_path: str, implementation_number: Optional[int]) -> List[str]:
        # Changed from test_file to test_path
        implementation = implementation_number if implementation_number is not None else 'default'
        return [test_path, f"--implementation={implementation}"]  # Changed from test_file to test_path

    def _run_tests(self, test_path: str, implementation_number: Optional[int] = None) -> None:
        # Changed from test_file to test_path
        with self._suppress_output():
            test_path = os.path.relpath(test_path, os.getcwd())

            plugins = [self._ResultCollector(self._failures)]
            current_file_dir = os.path.dirname(os.path.realpath(__file__))
            parent_dir = os.path.dirname(current_file_dir)
            # empty_pytest_ini_path = os.path.join(parent_dir, 'empty_pytest.ini')


            pytest_args = [test_path, "--mock"]

            # pytest_args = self._get_pytest_args(test_path, implementation_number)  # Changed from test_file to test_path
            pytest.main(pytest_args, plugins=plugins)

    def _retrieve_nth_failure_result(self, n: int) -> str:
        if len(self._failures) > n:
            return self._failures[n].longreprtext
        else:
            return None  # or some other default value


    def _retrieve_test_code_from_failure(self, n: int) -> str:
        if len(self._failures) > n:
            report = self._failures[n]

            # Extracting the test code directly from the report
            if hasattr(report.longrepr, 'reprtraceback') and \
               hasattr(report.longrepr.reprtraceback, 'reprentries') and \
               report.longrepr.reprtraceback.reprentries:
                test_code_lines = report.longrepr.reprtraceback.reprentries[0].lines
                test_code = "\n".join(test_code_lines)
                return test_code

            # Backup extraction in case the above isn't available
            # Extracting the test name from the report while stripping off fixture or parametrized information
            test_name_raw = report.nodeid.split("::")[-1]
            test_name_match = re.match(r"(\w+)", test_name_raw)  # Matches the first word characters
            if not test_name_match:
                return None  # Couldn't find the test name format
            test_name = test_name_match.group(1)

            # Update the file path extraction as per the new requirement
            test_file_path = report.longrepr.reprcrash.path

            # Read the test file and search for the function definition
            with open(test_file_path, 'r') as f:
                lines = f.readlines()

            test_code = ""
            inside_test = False
            for line in lines:
                if f"def {test_name}(" in line:
                    inside_test = True
                if inside_test:
                    test_code += line
                if inside_test and f"def {test_name}(" not in line and "def test_" in line:
                    break  # End of the test function

            return test_code
        else:
            return None  # or some other default value






    class _ResultCollector:
        def __init__(self, failures):
            self._failures = failures

        def pytest_runtest_logreport(self, report):
            print(f"Test {report.nodeid} ended with {report.outcome}")  # Debugging line
            if report.failed:
                self._failures.append(report)


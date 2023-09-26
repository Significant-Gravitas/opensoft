import io
import os
from contextlib import redirect_stdout

import pytest

from src.runner_pytest.implementations.runner_pytest_1 import RunnerPytest1

@pytest.fixture
def runner_pytest():
    return RunnerPytest1()

def test_no_stdout_from_run_tests(runner_pytest):
    f = io.StringIO()
    with redirect_stdout(f):
        absolute_path = os.path.abspath("src/module_fixture")
        runner_pytest.get_pytest_failure(n=0, path=absolute_path)

    output = f.getvalue()
    assert output == ""


def test_retrieve_test_code(runner_pytest):

    _, test_code = runner_pytest.get_pytest_failure(n=0, path="src/module_fixture")
    assert test_code is not None

    expected_code_fragment = """def test_should_fail_one(module_fixture):"""

    assert expected_code_fragment in test_code

    non_expected_code_fragment = """def test_should_fail_two(module_fixture):"""

    assert non_expected_code_fragment not in test_code


def test_retrieve_second_test_code(runner_pytest):
    _, test_code = runner_pytest.get_pytest_failure(n=1, path="src/module_fixture")
    assert test_code is not None

    expected_method_code = """def test_should_fail_one(module_fixture):
    assert False


@pytest.mark.mock
def test_should_fail_two(module_fixture):
"""

    assert expected_method_code in test_code


def test_same_test_multiple_failures(runner_pytest):
    first_run = runner_pytest.get_pytest_failure(n=0, path="src/module_fixture")
    second_run = runner_pytest.get_pytest_failure(n=0, path="src/module_fixture")
    assert first_run == second_run


def test_empty_test_file(runner_pytest):
    failure_detail, test_code = runner_pytest.get_pytest_failure(
        n=0, path="src/empty_test_file"
    )
    assert failure_detail is None
    assert test_code is None

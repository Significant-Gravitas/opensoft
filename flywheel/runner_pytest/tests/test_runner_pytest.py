import io
import os
from contextlib import redirect_stdout


def test_no_stdout_from_run_tests(runner_pytest):
    f = io.StringIO()
    with redirect_stdout(f):
        absolute_path = os.path.abspath("flywheel/module_fixture")
        runner_pytest.get_pytest_failure(n=0, path=absolute_path)

    output = f.getvalue()
    assert output == ""


def test_retrieve_test_code(runner_pytest):

    _, test_code = runner_pytest.get_pytest_failure(n=0, path="flywheel/module_fixture")
    assert test_code is not None

    expected_code_fragment = """def test_should_fail_one(module_fixture):"""

    assert expected_code_fragment in test_code

    non_expected_code_fragment = """def test_should_fail_two(module_fixture):"""

    assert non_expected_code_fragment not in test_code


def test_retrieve_second_test_code(runner_pytest):
    _, test_code = runner_pytest.get_pytest_failure(n=1, path="flywheel/module_fixture")
    assert test_code is not None

    expected_method_code = """    @pytest.mark.mock
    def test_should_fail_two(module_fixture):
    
        dummy_var_1 = 1
        dummy_var_2 = 2
        dummy_var_3 = 3
        dummy_var_4 = 4
        dummy_var_5 = 5
        dummy_var_6 = 6
        dummy_var_7 = 7
        dummy_var_8 = 8
        dummy_var_9 = 9
        dummy_var_10 = 10
    
        dummy_list = [dummy_var_1, dummy_var_2, dummy_var_3]
        dummy_dict = {"key1": dummy_var_4, "key2": dummy_var_5, "key3": dummy_var_6}
    
        dummy_list.append(dummy_var_7)
        dummy_list.extend([dummy_var_8, dummy_var_9])
        dummy_dict["key4"] = dummy_var_10
    
        dummy_var_1 = 1
        dummy_var_2 = 2
        dummy_var_3 = 3
        dummy_var_4 = 4
        dummy_var_5 = 5
        dummy_var_6 = 6
        dummy_var_7 = 7
        dummy_var_8 = 8
        dummy_var_9 = 9
        dummy_var_10 = 10
    
        dummy_list = [dummy_var_1, dummy_var_2, dummy_var_3]
        dummy_dict = {"key1": dummy_var_4, "key2": dummy_var_5, "key3": dummy_var_6}
    
        dummy_list.append(dummy_var_7)
        dummy_list.extend([dummy_var_8, dummy_var_9])
        dummy_dict["key4"] = dummy_var_10
    
        dummy_var_1 = 1
        dummy_var_2 = 2
        dummy_var_3 = 3
        dummy_var_4 = 4
        dummy_var_5 = 5
        dummy_var_6 = 6
        dummy_var_7 = 7
        dummy_var_8 = 8
        dummy_var_9 = 9
        dummy_var_10 = 10
    
        dummy_list = [dummy_var_1, dummy_var_2, dummy_var_3]
        dummy_dict = {"key1": dummy_var_4, "key2": dummy_var_5, "key3": dummy_var_6}
    
        dummy_list.append(dummy_var_7)
        dummy_list.extend([dummy_var_8, dummy_var_9])
        dummy_dict["key4"] = dummy_var_10
    
>       assert False
E       assert False"""

    assert expected_method_code in test_code


def test_same_test_multiple_failures(runner_pytest):
    first_run = runner_pytest.get_pytest_failure(n=0, path="flywheel/module_fixture")
    second_run = runner_pytest.get_pytest_failure(n=0, path="flywheel/module_fixture")
    assert first_run == second_run


def test_empty_test_file(runner_pytest):
    failure_detail, test_code = runner_pytest.get_pytest_failure(
        n=0, path="flywheel/empty_test_file"
    )
    assert failure_detail is None
    assert test_code is None

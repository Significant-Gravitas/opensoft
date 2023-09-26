import pytest


@pytest.mark.mock
def test_sould_succeed_three(module_fixture):
    assert True


@pytest.mark.mock
def test_should_fail_one(module_fixture):
    assert False


@pytest.mark.mock
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

    assert False

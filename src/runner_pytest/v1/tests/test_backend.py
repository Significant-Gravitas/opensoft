import io
import os
from contextlib import redirect_stdout

import pytest
import requests

from src.runner_pytest.v1.b1.endpoint import RunnerPytest1


@pytest.mark.asyncio
@pytest.fixture
def runner_pytest():
    return RunnerPytest1()

@pytest.mark.asyncio
async def test_retrieve_first_failure(client):
    url = 'http://localhost:8000/pytest_failures'
    path = os.path.abspath("src/module_fixture")
    query_parameters = {
        'n': 0,
        'path': path,
    }
    response = await client.get(
        "/pytest_failures/",
        params=query_parameters
    )

    assert response.status_code == 200
    result = response.json()
    assert result is not None

    assert "AssertionError" in result
    assert """@pytest.mark.mock
    def test_should_fail_one(module_fixture):
>       assert False
E       assert False""" in result

@pytest.mark.asyncio
async def test_retrieve_second_failure(client):
    path = os.path.abspath("src/module_fixture")
    query_parameters = {
        'n': 1,
        'path': path,
    }
    response = await client.get(
        "/pytest_failures/",
        params=query_parameters
    )

    assert response.status_code == 200
    result = response.json()
    assert result is not None

    expected_code_fragment = """@pytest.mark.mock
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

    assert expected_code_fragment in result

@pytest.mark.asyncio
async def test_empty_test_file(client):
    query_parameters = {
        'n': 0,
        'path': "src/empty_test_file",
    }

    response = await client.get(
        "/pytest_failures/",
        params=query_parameters
    )
    result = response.json()
    assert result is None

@pytest.mark.asyncio
async def test_without_path_provided(client):
    query_parameters = {
        'n': 0
    }

    response = await client.get(
        "/pytest_failures/",
        params=query_parameters
    )

    assert response.status_code == 200
    result = response.json()

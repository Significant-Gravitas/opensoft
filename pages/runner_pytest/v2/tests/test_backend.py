import os

import pytest

from pages.runner_pytest.v1.b1.endpoint import RunnerPytest1


@pytest.mark.asyncio
@pytest.fixture
def runner_pytest():
    return RunnerPytest1()


@pytest.mark.asyncio
async def test_retrieve_first_failure(client):
    url = "http://localhost:8000/pytest_failures"
    query_parameters = {
        "n": 0,
        "path": "pages/module_fixture",
    }
    response = await client.get("/pytest_failures/", params=query_parameters)

    assert response.status_code == 200
    result = response.json()
    assert result is not None
    assert "assert False" in result
    assert "AssertionError" in result


@pytest.mark.asyncio
async def test_retrieve_second_failure(client):
    path = os.path.abspath("pages/module_fixture")
    query_parameters = {
        "n": 1,
        "path": path,
    }
    response = await client.get("/pytest_failures/", params=query_parameters)

    assert response.status_code == 200
    result = response.json()
    assert result is not None

    assert "assert False" in result
    assert "AssertionError" in result


# @pytest.mark.asyncio
# async def test_empty_test_file(client):
#     query_parameters = {
#         'n': 0,
#         'path': "pages/empty_test_file",
#     }
#
#     response = await client.get(
#         "/pytest_failures/",
#         params=query_parameters
#     )
#     result = response.json()
#     assert result is None
#
# @pytest.mark.asyncio
# async def test_without_path_provided(client):
#     query_parameters = {
#         'n': 0
#     }
#
#     response = await client.get(
#         "/pytest_failures/",
#         params=query_parameters
#     )
#
#     assert response.status_code == 200
#     result = response.json()

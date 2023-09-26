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
async def test_retrieve_test_code(client):
    url = 'http://localhost:8000/pytest_failures'
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

    expected_code_fragment = """def test_should_fail_one(module_fixture):"""

    assert expected_code_fragment in result

    non_expected_code_fragment = """def test_should_fail_two(module_fixture):"""

    assert non_expected_code_fragment not in result

@pytest.mark.asyncio
async def test_retrieve_second_test_code(client):
    query_parameters = {
        'n': 1,
        'path': "src/module_fixture",
    }

    response = await client.get(
        "/pytest_failures/",
        params=query_parameters
    )
    result = response.json()
    assert result is not None

    expected_method_code = """file /Users/merwanehamadi/code/flywheel/src/module_fixture/tests/test_module_fixture_negative.py, line 9
  @pytest.mark.mock
  def test_should_fail_one(module_fixture):
E       fixture 'module_fixture' not found
>       available fixtures: anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, clear_db_after_test, doctest_namespace, event_loop, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, setup_db_session, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, unused_tcp_port, unused_tcp_port_factory, unused_udp_port, unused_udp_port_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/Users/merwanehamadi/code/flywheel/src/module_fixture/tests/test_module_fixture_negative.py:9"""

    assert expected_method_code in result

@pytest.mark.asyncio
async def test_same_test_multiple_failures(client):
    query_parameters = {
        'n': 0,
        'path': "src/module_fixture",
    }

    response = await client.get(
        "/pytest_failures/",
        params=query_parameters
    )
    first_run = response.json()

    response = await client.get(
        "/pytest_failures/",
        params=query_parameters
    )
    second_run = response.json()

    assert first_run == second_run

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

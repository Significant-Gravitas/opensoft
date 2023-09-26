import asyncio
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import MetaData
from sqlmodel import Session, SQLModel

from src import engine
from src.app import app


def pytest_addoption(parser):
    parser.addoption(
        "--implementation",
        action="store",
        default="all",
    )
    parser.addoption(
        "--mock", action="store_true", default=False, help="Run mock tests"
    )


import re

def get_backend_iterations(script_location: Path):
    pattern = re.compile(r'^b\d+$')
    all_folders = [entry.name for entry in script_location.iterdir() if entry.is_dir()]
    backend_iterations = [folder for folder in all_folders if pattern.match(folder)]
    return [f"http://127.0.0.1:8000/{script_location.name}/{folder}" for folder in backend_iterations]

def pytest_generate_tests(metafunc):
    if "client" in metafunc.fixturenames:
        # Get the path of the current test file
        test_file_path = Path(metafunc.module.__file__)

        # Adjust the path to reach the target directory based on your structure
        target_path = test_file_path.parent.parent

        backends = get_backend_iterations(target_path)
        metafunc.parametrize("client", backends, indirect=True)


@pytest.fixture
def client(request):
    base_url = request.param  # This is already a string URL now

    # Create an instance of AsyncClient with the parameterized base URL
    ac = AsyncClient(app=app, base_url=base_url)

    def fin():
        # Close the client when done
        asyncio.get_event_loop().run_until_complete(ac.aclose())

    # Use the finalizer to ensure the client is closed after usage
    request.addfinalizer(fin)

    return ac


def pytest_runtest_setup(item):
    if "mock" in item.keywords and not item.config.getoption("--mock"):
        pytest.skip("Skipped mock test because --mock option was not provided")


@pytest.fixture(scope="session", autouse=True)
def setup_db_session():
    from src.user_feedback.v1 import abstract_class

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield


@pytest.fixture(scope="function", autouse=True)
def clear_db_after_test():
    yield
    clear_database()


def clear_database():
    with Session(engine) as session:

        meta = MetaData()
        meta.reflect(bind=engine)

        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())

        session.commit()

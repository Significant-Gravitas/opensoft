import pytest
from sqlalchemy import MetaData
from sqlmodel import SQLModel, Session

from flywheel import engine
from flywheel.configurator_pytest.implementations.configurator_pytest_1 import ConfiguratorPytest1


def pytest_addoption(parser):
    parser.addoption(
        "--implementation",
        action="store",
        default="all",
    )
    parser.addoption("--mock", action="store_true", default=False, help="Run mock tests")


def pytest_generate_tests(metafunc):
    configurator = ConfiguratorPytest1()
    module, to_parameterize = configurator.setup_parameterization(metafunc)
    metafunc.parametrize(module, to_parameterize, indirect=True)

def pytest_runtest_setup(item):
    if "mock" in item.keywords and not item.config.getoption("--mock"):
        pytest.skip("Skipped mock test because --mock option was not provided")

@pytest.fixture(scope="session", autouse=True)
def setup_db_session():
    SQLModel.metadata.create_all(engine)
    yield

@pytest.fixture(scope="function", autouse=True)
def clear_db_after_test():
    yield  # This will first run the test function
    clear_database()  # Cleanup logic after the test finishes


def clear_database():
    with Session(engine) as session:
        # Reflect the tables
        meta = MetaData()
        meta.reflect(bind=engine)

        # Delete all records from all tables
        for table in reversed(meta.sorted_tables):  # reverse to respect FK dependencies
            session.execute(table.delete())

        session.commit()

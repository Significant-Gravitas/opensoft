import pytest
from sqlalchemy import MetaData
from sqlmodel import Session, SQLModel

from src import engine
from src.configurator_pytest.implementations.configurator_pytest_1 import (
    ConfiguratorPytest1,
)


def pytest_addoption(parser):
    parser.addoption(
        "--implementation",
        action="store",
        default="all",
    )
    parser.addoption(
        "--mock", action="store_true", default=False, help="Run mock tests"
    )


def pytest_generate_tests(metafunc):
    if "user_feedback_v2" not in str(metafunc.module) and "crud_module_v1" not in str(metafunc.module)  and "crud_module_v2" not in str(metafunc.module):
        configurator = ConfiguratorPytest1()
        module, to_parameterize = configurator.setup_parameterization(metafunc)
        metafunc.parametrize(module, to_parameterize, indirect=True)


def pytest_runtest_setup(item):
    if "mock" in item.keywords and not item.config.getoption("--mock"):
        pytest.skip("Skipped mock test because --mock option was not provided")


@pytest.fixture(scope="session", autouse=True)
def setup_db_session():
    from src.user_feedback_v2 import abstract_class

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

import pytest

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

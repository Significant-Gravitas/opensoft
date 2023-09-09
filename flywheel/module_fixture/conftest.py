import glob
import os

from flywheel.configurator_pytest.implementations.configurator_pytest_1 import ConfiguratorPytest1


# def pytest_generate_tests(metafunc):
#     configurator = ConfiguratorPytest1()
#     module, to_parameterize = configurator.setup_parameterization(metafunc)
#     metafunc.parametrize(module, to_parameterize, indirect=True)
#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--implementation",
#         action="store",
#         default="all",
#     )

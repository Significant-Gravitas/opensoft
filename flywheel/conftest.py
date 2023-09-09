import glob
import os

from flywheel.configurator_pytest.implementations.configurator_pytest_1 import ConfiguratorPytest1


def pytest_addoption(parser):
    parser.addoption(
        "--implementation",
        action="store",
        default="all",
    )

def convert_to_camel_case(s):
    # Split the string at the underscore
    parts = s.split('_')

    # Capitalize each part
    camel_case_parts = [part.capitalize() for part in parts]

    # Join them together without spaces
    return ''.join(camel_case_parts)

def pytest_generate_tests(metafunc):
    # Get script and folder
    script_folder = os.path.dirname(str(metafunc.definition.fspath))
    script_folder_relative = os.path.relpath(script_folder, os.getcwd())
    script_folder_parent_relative = os.path.dirname(script_folder_relative)
    folder = metafunc.config.args[0] if metafunc.config.args and metafunc.config.args[0].split("/")[-1] != "flywheel" else script_folder_parent_relative

    configurator = ConfiguratorPytest1()
    module, to_parameterize = configurator.prepare_for_parameterization(metafunc, folder)
    if module != 'battleship':
        test = "ok"
    metafunc.parametrize(module, to_parameterize, indirect=True)

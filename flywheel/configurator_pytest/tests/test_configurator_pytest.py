import io
import os
from contextlib import redirect_stdout

import pytest


# def test_absolute_path_handling(configurator_pytest):
#     # Define the folder location
#     cwd = os.getcwd()  # Get the current working directory
#     mock_folder = os.path.join(cwd, "flywheel", "module_fixture")
#
#     # Execute the method
#     module, to_parameterize = configurator_pytest.prepare_for_parameterization(None, mock_folder)
#
#     # Validate the module name and parameterization
#     assert module == "module_fixture"
#     assert set(cls.__name__ for cls in to_parameterize) == {"ImplOne", "ImplTwo"}
#
# def test_only_accepts_absolute_paths(configurator_pytest):
#     # Define a relative folder location
#     mock_folder = "flywheel/module_fixture"
#
#     # Expect a ValueError to be raised
#     with pytest.raises(ValueError) as excinfo:
#         configurator_pytest.prepare_for_parameterization(None, mock_folder)
#
#     # Check the message in the raised ValueError
#     assert "Only absolute paths are allowed" in str(excinfo.value)

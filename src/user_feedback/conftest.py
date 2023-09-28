# from pathlib import Path
#
# from src.conftest import get_backend_iterations
#
#
# def pytest_generate_tests(metafunc):
#     if "client" in metafunc.fixturenames:
#         # Get the path of the current test file
#         test_file_path = Path(metafunc.module.__file__)
#
#         # Adjust the path to reach the target directory based on your structure
#         target_path = test_file_path.parent.parent
#
#         backends = get_backend_iterations(target_path)
#         metafunc.parametrize("client", backends, indirect=True)

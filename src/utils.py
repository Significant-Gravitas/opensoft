import re


def get_backend_iterations(script_location):
    pattern = re.compile(r'^b\d+$')
    all_folders = [entry.name for entry in script_location.iterdir() if entry.is_dir()]
    backend_iterations = [folder for folder in all_folders if pattern.match(folder)]
    return [f"http://127.0.0.1:8000/{script_location.name}/{folder}" for folder in backend_iterations]

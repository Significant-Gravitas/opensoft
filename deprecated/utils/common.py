import os
import re

MODULE = "battleship"


def get_latest_number_from_files(directory="EXAMPLE/implementations"):

    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]

    files.sort()

    if not files:
        return None

    latest_file = files[-1]

    match = re.search(r"(\d+)", latest_file)
    if match:
        return int(match.group(1))
    else:
        return None


#
# IMPLEMENTATION_NUMBER = get_latest_number_from_files(
#     f"src/{MODULE}/implementations"
# )

failures = []


def print_file_content(filepath):
    with open(filepath, "r") as f:
        content = f.read()
        return content + "\n" + "-" * 40 + "\n"

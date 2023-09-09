import os
import re
import sys

import pytest

MODULE = "battleship"
def get_latest_number_from_files(directory="EXAMPLE/implementations"):
    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Sort the files alphabetically
    files.sort()

    # If there are no files, return None
    if not files:
        return None

    # Take the latest file
    latest_file = files[-1]

    # Extract number from the file name using regex
    match = re.search(r'(\d+)', latest_file)
    if match:
        return int(match.group(1))
    else:
        return None

IMPLEMENTATION_NUMBER = get_latest_number_from_files(f"flywheel/{MODULE}/implementations")

failures = []


def print_file_content(filepath):
    with open(filepath, "r") as f:
        content = f.read()
        return content + "\n" + "-" * 40 + "\n"  # Return the content as a string

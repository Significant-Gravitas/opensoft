import pyperclip  # Ensure you've installed this library
from pass_test import print_file_content

from utils.create_more_tests_2 import MODULE

if __name__ == "__main__":
    result_str = """
User:
Build a battleship game.
Assistant:
"""
    result_str += print_file_content(f"{MODULE}/product_requirements.txt")
    result_str += """
User:
"""

    result_str += print_file_content(f"{MODULE}/vague_requirement.txt")
    result_str += """
Assistant:
"""

    pyperclip.copy(result_str)

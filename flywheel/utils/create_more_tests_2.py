import pyperclip  # Ensure you've installed this library
from util.common import print_file_content

if __name__ == "__main__":
    result_str = print_file_content(f"{MODULE}/product_requirements.txt")
    result_str += print_file_content(f"{MODULE}/user_stories.txt")
    result_str += print_file_content(f"{MODULE}/conftest.py")
    result_str += print_file_content(f"{MODULE}/test_implementation.py")
    result_str += """
INSTRUCTIONS:What are some tests you could write ? Please write them.
ASSISTANT:
Here is a few tests that are missing:
"""
    # Copy the content to the clipboard
    pyperclip.copy(result_str)

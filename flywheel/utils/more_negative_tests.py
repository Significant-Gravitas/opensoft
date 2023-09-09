import pyperclip  # Ensure you've installed this library

from utils.common import MODULE, print_file_content

if __name__ == "__main__":
    result_str = print_file_content(f"{MODULE}/abstract_class.py")
    result_str += print_file_content(f"{MODULE}/tests/conftest.py")
    result_str += print_file_content(f"{MODULE}/tests/test_negative.py")
    result_str += """
INSTRUCTIONS:
What are some tests you could write ? Please write them.
Only include negative tests
ASSISTANT:
Ok here is a few negative tests that are missing:
"""
# Copy the content to the clipboard
pyperclip.copy(result_str)

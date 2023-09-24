import pyperclip
from utils.common import MODULE, print_file_content

if __name__ == "__main__":
    result_str = print_file_content(f"{MODULE}/abstract_class.py")
    result_str += print_file_content(f"{MODULE}/tests/conftest.py")
    result_str += print_file_content(f"{MODULE}/tests/test_implementation.py")
    result_str += """
INSTRUCTIONS:
What are some tests you could write ? Please write them.
Do not include negative tests, they're already covered in another folder.
ASSISTANT:
Ok I won't include negative tests, here is a few tests that are misssing:
"""

pyperclip.copy(result_str)

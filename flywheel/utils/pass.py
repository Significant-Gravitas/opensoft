import sys

import pyperclip
from utils.common import (
    IMPLEMENTATION_NUMBER,
    MODULE,
    get_nth_failure,
    print_file_content,
    result_only,
)

failures = []

if __name__ == "__main__":
    no_stdout_arg = "no_stdout"

    if len(sys.argv) < 2:
        print(
            "Usage: python utils/pass_test.py <failure_number> [result_only|no_stdout]"
        )
        sys.exit(1)

    n = int(sys.argv[1])

    include_stdout = no_stdout_arg not in sys.argv

    if len(sys.argv) >= 3 and sys.argv[2] == "result_only":
        result_str = result_only(n)
    else:
        result_str = print_file_content(
            f"{MODULE}/implementations/{MODULE}_{IMPLEMENTATION_NUMBER}.py"
        )
        result_str += print_file_content(f"{MODULE}/tests/conftest.py")
        result_str += get_nth_failure(n, include_stdout)
        result_str += """
User:
Modify the class or the test in order for the test to pass.
Assistant:
Here is my suggestion and code for the test to pass
"""

    pyperclip.copy(result_str)

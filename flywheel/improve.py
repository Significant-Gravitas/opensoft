import sys

import click
import pyperclip

from flywheel.utils.common import IMPLEMENTATION_NUMBER, print_file_content
from flywheel.utils.pytest_failure import get_nth_failure

failures = []


@click.command()
@click.argument("module")
@click.argument("command")
@click.option("--pick_item", "-o", default=None, help="This is an optional argument")
@click.option("--result_only", "-o", is_flag=None, help="This is an optional argument")
def run(module, command, pick_item, result_only):
    no_stdout_arg = "no_stdout"

    n = int(pick_item) if pick_item else 0

    include_stdout = no_stdout_arg not in sys.argv

    if result_only:
        result_str = result_only(n)
    else:
        result_str = print_file_content(f"flywheel/{module}/abstract_class.py")
        result_str += print_file_content(
            f"flywheel/{module}/implementations/{module}_{IMPLEMENTATION_NUMBER}.py"
        )
        result_str += print_file_content(f"flywheel/{module}/tests/conftest.py")
        result_str += get_nth_failure(n, include_stdout)
        result_str += """
User:
Modify the class in order for the test to pass.
Assistant:
Here is my suggestion to modify the class + the code that comes with it.
I won't modify the tests or the abstract class or add any attributes to the existing classes
"""

    from dotenv import load_dotenv

    load_dotenv()

    pyperclip.copy(result_str)


if __name__ == "__main__":
    run()

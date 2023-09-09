import click
import sys
import pyperclip

from flywheel.runner_pytest.implementations.runner_pytest_1 import RunnerPytest1
from flywheel.utils.common import print_file_content, IMPLEMENTATION_NUMBER

failures = []

@click.command()
@click.argument('module')
@click.argument('command')
@click.option('--pick_item', '-o', default=None, help='This is an optional argument')
@click.option('--result_only', '-o', is_flag=None, help='This is an optional argument')
def run(module, command, pick_item, result_only):
    no_stdout_arg = "no_stdout"

    n = int(pick_item) if pick_item else 1

    include_stdout = no_stdout_arg not in sys.argv

    if result_only:
        result_str = result_only(n)
    else:
        result_str = print_file_content(f"flywheel/{module}/abstract_class.py")
        result_str += print_file_content(
            f"flywheel/{module}/implementations/{module}_{1}.py"
        )
        result_str += print_file_content(f"flywheel/{module}/conftest.py")
        result_str += RunnerPytest1().get_pytest_failure(n=n, path=f"flywheel/{module}")[0]
        result_str += """
User:
Modify the class in order for the test to pass.
Assistant:
Here is my suggestion to modify the class + the code that comes with it.
I won't modify the tests or the abstract class or add any attributes to the existing classes
"""
    # Copy the content to the clipboard
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    pyperclip.copy(result_str)



if __name__ == '__main__':
    run()

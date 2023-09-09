import click
import sys
import pyperclip

from flywheel.runner_pytest.implementations.runner_pytest_1 import RunnerPytest1
from flywheel.utils.common import print_file_content, IMPLEMENTATION_NUMBER

failures = []
IMPLEMENTATION_NUMBER = 4
@click.command()
@click.argument('module')
@click.argument('command')
@click.option('--pick_item', '-o', default=None, help='This is an optional argument')
@click.option('--result_only', '-o', is_flag=None, help='This is an optional argument')
def run(module, command, pick_item, result_only):
    n = int(pick_item) if pick_item else 0
    if command == 'improve':
        abstract_class = print_file_content(f"flywheel/{module}/abstract_class.py")
        implementation = print_file_content(
            f"flywheel/{module}/implementations/{module}_{IMPLEMENTATION_NUMBER}.py"
        )
        fixtures = print_file_content(f"flywheel/{module}/conftest.py")
        pytest_failure = RunnerPytest1().get_pytest_failure(n=n, path=f"flywheel/{module}")
        if pytest_failure[0] is None:
            # throw error
            raise Exception("No failure found")
        instructions = """
    User:
    Modify the class in order for the test to pass.
    Assistant:
    Here is my suggestion to modify the class + the code that comes with it.
    I won't modify the tests or the abstract class or add any attributes to the existing classes
    """
        result_str = abstract_class + implementation + fixtures + pytest_failure[0] + instructions
        print("Full Prompt:", len(result_str))

        if len(result_str) > 12000:
            result_str = implementation + fixtures + pytest_failure[0] + instructions
            print("Reduced Prompt:", len(result_str))
        # Copy the content to the clipboard
        from dotenv import load_dotenv

        # Load environment variables from .env file
        load_dotenv()

    pyperclip.copy(result_str)



if __name__ == '__main__':
    run()

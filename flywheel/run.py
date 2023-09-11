import click
import pyperclip
from flywheel.runner_pytest.implementations.runner_pytest_1 import RunnerPytest1
from flywheel.utils.common import print_file_content

failures = []
IMPLEMENTATION_NUMBER = 1

def load_content_for_improve(module, pick_item):
    abstract_class = print_file_content(f"flywheel/{module}/abstract_class.py")
    implementation = print_file_content(f"flywheel/{module}/implementations/{module}_{IMPLEMENTATION_NUMBER}.py")
    fixtures = print_file_content(f"flywheel/{module}/conftest.py")
    pytest_failure = RunnerPytest1().get_pytest_failure(n=int(pick_item), path=f"flywheel/{module}")

    if pytest_failure[0] is None:
        raise Exception("No failure found")

    instructions = """
User:
Modify the class in order for the test to pass.
Assistant:
Here is my suggestion to modify the class + the code that comes with it.
I won't modify the tests or the abstract class or add any attributes to the existing classes
"""
    result_str = abstract_class + implementation + fixtures + pytest_failure[0] + instructions

    if len(result_str) > 12000:
        result_str = implementation + fixtures + pytest_failure[0] + instructions

    return result_str


def load_content_for_test(module):
    product_requirements = print_file_content(f"flywheel/{module}/product_requirements.txt")
    user_stories = print_file_content(f"flywheel/{module}/user_stories.txt")
    abstract_class = print_file_content(f"flywheel/{module}/abstract_class.py")
    fixtures = print_file_content(f"flywheel/{module}/conftest.py")
    instructions = """
INSTRUCTIONS:
What are some tests you could write? Please write them.
Do not include negative tests, they're already covered in another folder.
ASSISTANT:
Ok I won't include negative tests, here are a few tests that are missing:
"""
    result_str = product_requirements + user_stories + abstract_class + fixtures + instructions

    return result_str

@click.command()
@click.argument('module')
@click.argument('command')
@click.option('--pick_item', '-o', default=None, help='This is an optional argument')
@click.option('--result_only', '-o', is_flag=True, default=False, help='This is an optional argument')
def run(module, command, pick_item, result_only):
    if command == 'improve':
        result_str = load_content_for_improve(module, 0)
    elif command == 'test':
        result_str = load_content_for_test(module)
    else:
        raise ValueError("Unknown command")

    print("Prompt Length:", len(result_str))
    pyperclip.copy(result_str)


if __name__ == '__main__':
    run()

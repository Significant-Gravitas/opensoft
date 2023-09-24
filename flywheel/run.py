import random
import re

import click
import pyperclip

from flywheel.runner_pytest.implementations.runner_pytest_1 import RunnerPytest1
from flywheel.utils.common import print_file_content

failures = []
IMPLEMENTATION_NUMBER = 1


def load_content_for_pass_tests_strict(module, pick_item):
    db_engine = print_file_content(f"flywheel/engine.py")
    db_hint = "To use the db:\n with Session(engine) as session:\n    pass"
    abstract_class = print_file_content(f"flywheel/{module}/abstract_class.py")
    implementation = print_file_content(
        f"flywheel/{module}/implementations/{module}_{IMPLEMENTATION_NUMBER}.py"
    )
    fixtures = print_file_content(f"flywheel/{module}/conftest.py")
    pytest_failure = RunnerPytest1().get_pytest_failure(
        n=int(pick_item), path=f"flywheel/{module}"
    )

    if pytest_failure[0] is None:
        print("No failure found")
        pytest_failure = [""]

    instructions = """
User:
Modify the class in order for the test to pass.
Assistant:
Here is my suggestion to modify the class + the code that comes with it.
I won't modify the tests or the abstract class or add any attributes to the existing classes
"""
    result_str = (
        db_engine + db_hint + abstract_class + implementation + fixtures + pytest_failure[0] + instructions
    )

    if len(result_str) > 12000:
        result_str = db_engine + db_hint + implementation + fixtures + pytest_failure[0] + instructions

    return result_str


def load_content_for_pass_tests(module, pick_item):
    db_engine = print_file_content(f"flywheel/engine.py")
    db_hint = "To use the db:\n with Session(engine) as session:\n    pass"
    abstract_class = print_file_content(f"flywheel/{module}/abstract_class.py")
    implementation = print_file_content(
        f"flywheel/{module}/implementations/{module}_{IMPLEMENTATION_NUMBER}.py"
    )
    fixtures = print_file_content(f"flywheel/{module}/conftest.py")
    pytest_failure = RunnerPytest1().get_pytest_failure(
        n=int(pick_item), path=f"flywheel/{module}"
    )

    if pytest_failure[0] is None:
        print("No failure found")
        pytest_failure = [""]

    instructions = """
User:
Modify the class or the tests in order for the test to pass, depending on whether the test makes sense or not.
Assistant:
"""
    result_str = (
        db_engine + db_hint + db_engine + abstract_class + implementation + fixtures + pytest_failure[0] + instructions
    )

    if len(result_str) > 12000:
        result_str = db_engine + db_hint + implementation + fixtures + pytest_failure[0] + instructions

    return result_str


def load_content_for_remove_first_test(module, pick_item):

    test_failure, test_code = RunnerPytest1().get_pytest_failure(
        n=int(pick_item), path=f"flywheel/{module}"
    )
    print(f"You're saying you want to remove this test ?:{test_code}")
    return test_code


def load_content_for_add_tests(module, only_gherkin=True):
    product_requirements = print_file_content(
        f"flywheel/{module}/product_requirements.txt"
    )
    user_stories = print_file_content(f"flywheel/{module}/user_stories.txt")
    abstract_class = print_file_content(f"flywheel/{module}/abstract_class.py")
    fixtures = print_file_content(f"flywheel/{module}/conftest.py")
    tests = print_file_content(f"flywheel/{module}/tests/test_{module}.py")
    if only_gherkin:
        prefix = """Pick the first Gherkin scenario not implemented and write a test for it. It should be named exactly like the scenario but snake_case. (e.g. "As a user I want to be able to add a product to my cart" -> "test_as_a_user_i_want_to_be_able_to_add_a_product_to_my_cart")"""
    else:
        prefix = """Write more tests"""

    instructions= f"""
INSTRUCTIONS: {prefix}
ASSISTANT:
Here is the test you should be writing, using pytest:
"""
    result_str = (
        product_requirements
        + user_stories
        + abstract_class
        + fixtures
        + tests
        + instructions
    )

    if len(result_str) > 12000:
        tests_implemented = (
            "these tests are already implemented, do not implement them again: \n"
            + extract_function_names(tests)
        )
        result_str = (
            product_requirements
            + user_stories
            + abstract_class
            + fixtures
            + take_percentage_of_string(tests, 0.5)
            + tests_implemented
            + instructions
        )
        if len(result_str) > 12000:
            tests_implemented = (
                "these tests are already implemented, do not implement them again: \n"
                + extract_function_names(tests)
            )
            result_str = (
                product_requirements
                + user_stories
                + abstract_class
                + fixtures
                + take_percentage_of_string(tests, 0.2)
                + tests_implemented
                + instructions
            )
            if len(result_str) > 12000:
                raise Exception("Prompt too long")
    return result_str




def load_content_for_remove_tests(module):
    product_requirements = print_file_content(
        f"flywheel/{module}/product_requirements.txt"
    )
    user_stories = print_file_content(f"flywheel/{module}/user_stories.txt")
    abstract_class = print_file_content(f"flywheel/{module}/abstract_class.py")
    fixtures = print_file_content(f"flywheel/{module}/conftest.py")
    test_positive = print_file_content(f"flywheel/{module}/tests/test_{module}.py")
    instructions = """
INSTRUCTIONS:
What are some tests you think don't make sense ? Please remove them
ASSISTANT:
Here are the tests you should be removing and why:
"""
    result_str = (
        product_requirements
        + user_stories
        + abstract_class
        + fixtures
        + test_positive
        + instructions
    )

    if len(result_str) > 12000:
        print("Prompt Length Before:", len(result_str))
        result_str = (
            user_stories + abstract_class + fixtures + test_positive + instructions
        )
        if len(result_str) > 12000:
            raise Exception("Prompt too long")

    return result_str


def load_content_for_compress_tests(module):
    abstract_class = print_file_content(f"flywheel/{module}/abstract_class.py")
    fixtures = print_file_content(f"flywheel/{module}/conftest.py")
    test_positive = print_file_content(f"flywheel/{module}/tests/test_{module}.py")
    instructions = """
INSTRUCTIONS:
Can you make these tests shorter by adding fixtures ? Also try to reuse the same fixtures
"""
    result_str = abstract_class + fixtures + test_positive + instructions

    return result_str


@click.command()
@click.argument("module")
@click.argument("command")
@click.option("--pick_item", "-o", default=None, help="This is an optional argument")
@click.option(
    "--result_only",
    "-o",
    is_flag=True,
    default=False,
    help="This is an optional argument",
)
def run(module, command, pick_item, result_only):
    if command == "pass_tests_strict":
        result_str = load_content_for_pass_tests_strict(module, 0)
    elif command == "pass_tests":
        result_str = load_content_for_pass_tests(module, 0)
    elif command == "add_tests":
        result_str = load_content_for_add_tests(module)
    elif command == "add_more_tests":
        result_str = load_content_for_add_tests(module, only_gherkin=False)
    elif command == "remove_tests":
        result_str = load_content_for_remove_tests(module)
    elif command == "remove_first_test":
        result_str = load_content_for_remove_first_test(module, 0)
    elif command == "compress_tests":
        result_str = load_content_for_compress_tests(module)
    else:
        raise ValueError("Unknown command")

    print("Prompt Length:", len(result_str))
    pyperclip.copy(result_str)


def take_percentage_of_string(s: str, percentage: float) -> str:

    if not (0 <= percentage <= 1):
        raise ValueError("Percentage must be between 0 and 1")

    length = len(s)
    part_length = int(length * percentage)

    start_index = random.randint(0, length - part_length)

    return s[start_index : start_index + part_length]


def extract_function_names(text):
    pattern = re.compile(r"def test_(.*?)\(", re.DOTALL)
    matches = pattern.findall(text)
    return ", ".join(matches)


if __name__ == "__main__":
    run()

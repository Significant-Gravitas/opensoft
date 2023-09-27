import asyncio
import random
import re

import click
import pyperclip
from fastapi import requests

from deprecated.utils.common import print_file_content
from src.client import get_client
from src.runner_pytest.v1.b1.endpoint import RunnerPytest1

failures = []
IMPLEMENTATION_NUMBER = 1


async def load_content_for_pass_tests_strict(module, pick_item):
    db_engine = print_file_content(f"src/engine.py")
    db_hint = "To use the db:\n with Session(engine) as session:\n    pass"
    models = print_file_content(f"src/{module}/models.py")
    implementation = print_file_content(
        f"src/{module}/implementations/{module}_{IMPLEMENTATION_NUMBER}.py"
    )
    fixtures = print_file_content(f"src/{module}/conftest.py")
    pytest_failure = RunnerPytest1().get_pytest_failure(
        n=int(pick_item), path=f"src/{module}"
    )

    if pytest_failure is None:
        print("No failure found")
        pytest_failure = ""

    instructions = """
User:
Modify the class in order for the test to pass.
Assistant:
Here is my suggestion to modify the class + the code that comes with it.
I won't modify the tests or the abstract class or add any attributes to the existing classes
"""
    result_str = (
        db_engine + db_hint + models + implementation + fixtures + pytest_failure + instructions
    )

    if len(result_str) > 12000:
        result_str = db_engine + db_hint + implementation + fixtures + pytest_failure + instructions

    return result_str


async def load_content_for_pass_tests(module, pick_item):
    parts = module.rsplit('/', 1)
    module = parts[0]
    backend = parts[1]
    db_engine = print_file_content(f"src/engine.py")
    db_hint = "To use the db:\n with Session(engine) as session:\n    pass"
    models = print_file_content(f"src/{module}/models.py")
    implementation = print_file_content(
        f"src/{module}/{backend}/endpoint.py"
    )
    fixtures = ""

    parts = module.rsplit('/', 1)
    module_name = parts[0]
    query_parameters = {
        'n': 0,
        'path': f"src/{module_name}",
    }
    client = get_client("http://localhost:8000")
    response = await client.get(
        "v1/b1/pytest_failures/",
        params=query_parameters
    )
    first_run = response.json()

    pytest_failure = RunnerPytest1().get_pytest_failure(
        n=int(pick_item), path=f"src/{module}"
    )

    if pytest_failure is None:
        print("No failure found")
        pytest_failure = ""

    instructions = """
User:
Modify the class or the tests in order for the test to pass, depending on whether the test makes sense or not.
Assistant:
"""
    result_str = (
        db_engine + db_hint + db_engine + models + implementation + fixtures + pytest_failure + instructions
    )

    if len(result_str) > 12000:
        result_str = db_engine + db_hint + implementation + fixtures + pytest_failure + instructions

    return result_str


async def load_content_for_remove_first_test(module, pick_item):

    test_failure, test_code = RunnerPytest1().get_pytest_failure(
        n=int(pick_item), path=f"src/{module}"
    )
    print(f"You're saying you want to remove this test ?:{test_code}")
    return test_code


async def load_content_for_add_tests(module, only_gherkin=True):
    product_requirements = print_file_content(
        f"src/{module}/product_requirements.txt"
    )
    user_stories = print_file_content(f"src/{module}/user_stories.txt")
    models = print_file_content(f"src/{module}/models.py")
    fixtures = print_file_content(f"src/{module}/conftest.py")
    tests = print_file_content(f"src/{module}/tests/test_{module}.py")
    if only_gherkin:
        prefix = """Pick the first Gherkin scenario not implemented and write a test for it. It should be named exactly like the scenario but snake_case. (e.g. "As a user I want to be able to add a product to my cart" -> "test_as_a_user_i_want_to_be_able_to_add_a_product_to_my_cart")"""
    else:
        prefix = """Write more tests"""

    instructions= f"""
INSTRUCTIONS: {prefix}
ASSISTANT:
This gherkin scenario is not implemented yet. I will name it test_{{scenario_name_in_snake_case}} and implement the test:
"""
    result_str = (
        product_requirements
        + user_stories
        + models
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
            + models
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
                + models
                + fixtures
                + take_percentage_of_string(tests, 0.2)
                + tests_implemented
                + instructions
            )
            if len(result_str) > 12000:
                raise Exception("Prompt too long")
    return result_str




async def load_content_for_remove_tests(module):
    product_requirements = print_file_content(
        f"src/{module}/product_requirements.txt"
    )
    user_stories = print_file_content(f"src/{module}/user_stories.txt")
    models = print_file_content(f"src/{module}/models.py")
    fixtures = print_file_content(f"src/{module}/conftest.py")
    test_positive = print_file_content(f"src/{module}/tests/test_{module}.py")
    instructions = """
INSTRUCTIONS:
What are some tests you think don't make sense ? Please remove them
ASSISTANT:
Here are the tests you should be removing and why:
"""
    result_str = (
        product_requirements
        + user_stories
        + models
        + fixtures
        + test_positive
        + instructions
    )

    if len(result_str) > 12000:
        print("Prompt Length Before:", len(result_str))
        result_str = (
            user_stories + models + fixtures + test_positive + instructions
        )
        if len(result_str) > 12000:
            raise Exception("Prompt too long")

    return result_str


async def load_content_for_compress_tests(module):
    models = print_file_content(f"src/{module}/models.py")
    fixtures = print_file_content(f"src/{module}/conftest.py")
    test_positive = print_file_content(f"src/{module}/tests/test_{module}.py")
    instructions = """
INSTRUCTIONS:
Can you make these tests shorter by adding fixtures ? Also try to reuse the same fixtures
"""
    result_str = models + fixtures + test_positive + instructions

    return result_str


async def load_content_for_fix_frontend(module):
    app = print_file_content(f"src/App.js")

    module_frontends = print_file_content(f"src/{module}/UserFeedbackV2.js")

    result_str = app + module_frontends

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
    loop = asyncio.get_event_loop()

    if command == "pass_tests_strict":
        result_str = loop.run_until_complete(load_content_for_pass_tests_strict(module, 0))
    elif command == "pass_tests":
        result_str = loop.run_until_complete(load_content_for_pass_tests(module, 0))
    elif command == "add_tests":
        result_str = loop.run_until_complete(load_content_for_add_tests(module))
    elif command == "add_more_tests":
        result_str = loop.run_until_complete(load_content_for_add_tests(module, only_gherkin=False))
    elif command == "remove_tests":
        result_str = loop.run_until_complete(load_content_for_remove_tests(module))
    elif command == "remove_first_test":
        result_str = loop.run_until_complete(load_content_for_remove_first_test(module, 0))
    elif command == "compress_tests":
        result_str = loop.run_until_complete(load_content_for_compress_tests(module))
    elif command == "fix_frontend":
        result_str = loop.run_until_complete(load_content_for_fix_frontend(module))
    else:
        raise ValueError("Unknown command")

    print("Prompt Length:", len(result_str))
    pyperclip.copy(result_str)



async def take_percentage_of_string(s: str, percentage: float) -> str:

    if not (0 <= percentage <= 1):
        raise ValueError("Percentage must be between 0 and 1")

    length = len(s)
    part_length = int(length * percentage)

    start_index = random.randint(0, length - part_length)

    return s[start_index : start_index + part_length]


async def extract_function_names(text):
    pattern = re.compile(r"def test_(.*?)\(", re.DOTALL)
    matches = pattern.findall(text)
    return ", ".join(matches)


# if __name__ == "__main__":
#     asyncio.run(run())

from flywheel.python_injector.implementations.python_injector_1 import Pythoninjector1


def test_single_method_injection():
    initial_content = """
class TestClass:
    def single_method(self):
        return "This is from initial."
"""

    suggestion_content = """
class TestClass:
    def single_method(self):
        return "This is from suggestion."
"""

    expected_output = """
class TestClass:
    def single_method(self):
        return "This is from suggestion."
"""

    injector = Pythoninjector1()
    output = injector.inject_functions(initial_content, suggestion_content)
    assert output.strip() == expected_output.strip()


def test_method_injection():
    initial_content = """
class TestClass:
    def method_one(self):
        return "This is method one from initial."
    def method_two(self):
        return "This is method two from initial."
"""

    suggestion_content = """
class TestClass:
    def method_one(self):
        return "This is method one from suggestion."
"""

    expected_output = """
class TestClass:
    def method_one(self):
        return "This is method one from suggestion."
    def method_two(self):
        return "This is method two from initial."
"""

    injector = Pythoninjector1()
    output = injector.inject_functions(initial_content, suggestion_content)
    assert output.strip() == expected_output.strip()


def test_new_method_injection():
    initial_content = """
class TestClass:
    def method_one(self):
        return "This is method one from initial."
"""

    suggestion_content = """
class TestClass:
    def method_two(self):
        return "This is method two from suggestion."
"""

    expected_output = """
class TestClass:
    def method_one(self):
        return "This is method one from initial."
    def method_two(self):
        return "This is method two from suggestion."
"""

    injector = Pythoninjector1()
    output = injector.inject_functions(initial_content, suggestion_content)
    assert output.strip() == expected_output.strip()


def test_single_function_injection():
    initial_content = """
def standalone_function():
    return "This is a function from initial."
"""

    suggestion_content = """
def standalone_function():
    return "This is a function from suggestion."
"""

    expected_output = """
def standalone_function():
    return "This is a function from suggestion."
"""

    injector = Pythoninjector1()
    output = injector.inject_functions(initial_content, suggestion_content)
    assert output.strip() == expected_output.strip()


def test_multiple_standalone_function_injection():
    initial_content = """
def function_one():
    return "Function one from initial."
"""

    suggestion_content = """
def function_two():
    return "Function two from suggestion."
def function_three():
    return "Function three from suggestion."
"""

    expected_output = """
def function_one():
    return "Function one from initial."
def function_two():
    return "Function two from suggestion."
def function_three():
    return "Function three from suggestion."
"""

    injector = Pythoninjector1()
    output = injector.inject_functions(initial_content, suggestion_content)
    assert output.strip() == expected_output.strip()


def test_import_injection():
    initial_content = """
def simple_function():
    return "This function does not use any external libraries."
"""

    suggestion_content = """
import math

def simple_function():
    result = math.sqrt(16)
    return f"The square root of 16 is {result}."
"""

    expected_output = """
import math

def simple_function():
    result = math.sqrt(16)
    return f"The square root of 16 is {result}."
"""

    injector = Pythoninjector1()
    output = injector.inject_functions(initial_content, suggestion_content)
    assert output.strip() == expected_output.strip()

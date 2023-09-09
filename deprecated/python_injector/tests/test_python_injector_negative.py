import ast

import pytest


def test_empty_file_content_extraction(injector):
    with pytest.raises(ValueError):
        injector.extract_functions("")


def test_non_python_code_extraction(injector):
    with pytest.raises(SyntaxError):
        injector.extract_functions("This is not a Python code.")


def test_invalid_file_content_injection(injector):
    with pytest.raises(ValueError):
        injector.inject_functions("", "def func(): pass")


def test_invalid_suggestion_injection(injector):
    with pytest.raises(SyntaxError):
        injector.inject_functions("def initial_func(): pass", "Not valid Python code")


def test_invalid_source_for_parsing(injector):
    with pytest.raises(SyntaxError):
        injector.get_parsed_source("Not a Python code.")


def test_non_dict_suggestion_functions(injector):
    initial = "def func_one(): pass"
    initial_ast = injector.get_parsed_source(initial)

    with pytest.raises(TypeError):
        injector.get_updated_source(initial_ast, "not a dict")


def test_none_file_content_extraction(injector):
    with pytest.raises(ValueError):
        injector.extract_functions(None)


def test_none_source_for_parsing(injector):
    with pytest.raises(ValueError):
        injector.get_parsed_source(None)


def test_empty_dict_suggestion_functions(injector):
    initial = "def func_one(): pass"
    initial_ast = injector.get_parsed_source(initial)

    with pytest.raises(ValueError):
        injector.get_updated_source(initial_ast, {})


def test_invalid_value_suggestion_functions(injector):
    initial = "def func_one(): pass"
    initial_ast = injector.get_parsed_source(initial)

    with pytest.raises(TypeError):
        injector.get_updated_source(initial_ast, {"func": 123})


def test_non_module_ast_node(injector):
    with pytest.raises(ValueError):
        injector.get_updated_source(ast.FunctionDef(), {"func": "def func(): pass"})


def test_non_string_file_content_extraction(injector):
    with pytest.raises(TypeError):
        injector.extract_functions(123)


def test_non_string_suggestion_code_for_injection(injector):
    with pytest.raises(TypeError):
        injector.inject_functions("def initial_func(): pass", 123)


def test_non_string_source_for_parsing(injector):
    with pytest.raises(TypeError):
        injector.get_parsed_source(123)


def test_non_string_keys_in_suggestion_functions(injector):
    initial = "def func_one(): pass"
    initial_ast = injector.get_parsed_source(initial)
    with pytest.raises(TypeError):  # Expecting TypeError instead of ValueError
        injector.get_updated_source(initial_ast, {123: "def func(): pass"})


def test_empty_ast_module_for_updating_source(injector):
    empty_ast = ast.Module(body=[], type_ignores=[])
    with pytest.raises(ValueError):
        injector.get_updated_source(empty_ast, {"func": "def func(): pass"})


def test_non_module_ast_node_for_parsing(injector):
    with pytest.raises(TypeError):
        injector.get_parsed_source(ast.FunctionDef())

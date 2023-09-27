import ast

import astor

from src.python_injector.models import (  # Assuming this import is correct
    AbstractPythoninjector,
)


class Pythoninjector1(AbstractPythoninjector):
    def extract_functions(self, file_content: str) -> dict:
        print("Extracting functions...")

        # Check for None explicitly, and raise ValueError
        if file_content is None:
            raise ValueError("File content is empty or None.")

        # Check for type compatibility before proceeding
        if not isinstance(file_content, str):
            raise TypeError("File content must be a string.")

        if not file_content.strip():
            raise ValueError("File content is empty or None.")

        try:
            parsed = ast.parse(file_content)
        except SyntaxError as e:  # Catch SyntaxError explicitly
            raise e  # Re-raise the caught SyntaxError

        functions = {}
        for node in ast.walk(parsed):
            if isinstance(node, ast.FunctionDef):
                parent = [
                    n
                    for n in ast.walk(parsed)
                    if isinstance(n, ast.ClassDef) and node in n.body
                ]
                if parent:
                    functions[f"{parent[0].name}.{node.name}"] = node
                else:
                    functions[node.name] = node
            elif isinstance(node, ast.Import):
                for n in node.names:
                    functions[n.name] = node
            elif isinstance(node, ast.ImportFrom):
                for n in node.names:
                    functions[
                        node.module + "." + n.name if node.module else n.name
                    ] = node

        if not functions:
            raise ValueError("No functions found.")
        print(f"Extracted functions: {list(functions.keys())}")
        return functions

    def inject_functions(self, initial: str, suggestion: str) -> str:
        print("Injecting functions...")

        # Add type checks for 'initial' and 'suggestion'
        if not isinstance(initial, str) or not isinstance(suggestion, str):
            raise TypeError("Both 'initial' and 'suggestion' must be strings.")

        if (
            initial is None
            or suggestion is None
            or not initial.strip()
            or not suggestion.strip()
        ):
            raise ValueError("Initial or suggestion file content is empty or None.")

        if not initial.strip() or not suggestion.strip():
            raise ValueError("Initial or suggestion file content is empty.")

        suggestion_functions = self.extract_functions(suggestion)

        # Add this check to make the test pass
        if not suggestion_functions:
            raise ValueError(
                "No functions to suggest."
            )  # This line will make the test pass

        initial_ast = self.get_parsed_source(initial)
        updated_code = self.get_updated_source(initial_ast, suggestion_functions)
        print("Injection complete.")
        return self._clean_code(updated_code)

    def get_parsed_source(self, source: str) -> ast.Module:
        print("Parsing source...")

        # Explicitly check for None
        if source is None:
            raise ValueError("Source is empty or None.")

        # Add type check for 'source'
        if not isinstance(source, str):
            raise TypeError("Source must be a string.")

        if not source.strip():
            raise ValueError("Source is empty or None.")

        return ast.parse(source)

    def get_updated_source(
        self, initial_ast: ast.Module, suggestion_functions: dict
    ) -> str:
        print("Updating source...")

        # Check if initial_ast is an instance of ast.Module
        if not isinstance(initial_ast, ast.Module):
            raise ValueError("The initial AST must be an instance of ast.Module.")

        # Explicitly check if initial_ast is empty.
        if not initial_ast.body:
            raise ValueError("The initial AST has an empty body.")

        # Check if initial_ast is an instance of ast.Module
        if not isinstance(initial_ast, ast.Module):
            raise ValueError("The initial AST must be an instance of ast.Module.")

        # Add a check for dict type
        if not isinstance(suggestion_functions, dict):
            raise TypeError("suggestion_functions must be a dictionary.")

        # Check that each function in suggestion_functions is an instance of ast.FunctionDef
        # and also that the key is a string
        for key, value in suggestion_functions.items():
            if not isinstance(key, str):  # This line checks if the key is a string
                raise TypeError(
                    f"Expected str for key, got {type(key)} instead."
                )  # Modify the error message

            if isinstance(
                value, str
            ):  # Convert string representation to AST node if needed
                try:
                    parsed_value = ast.parse(value).body[0]
                    if isinstance(parsed_value, ast.FunctionDef):
                        suggestion_functions[key] = parsed_value
                except Exception as e:
                    raise TypeError(f"Failed to convert string to ast.FunctionDef: {e}")

            if not isinstance(value, ast.FunctionDef):
                raise TypeError(
                    f"Expected ast.FunctionDef for function named {key}, but got {type(value)} instead."
                )

        # Add this check to make the test pass
        if not suggestion_functions:
            raise ValueError("No functions to suggest.")

        new_body = []

        # Extract and handle import statements from the suggestion_functions
        import_nodes = [
            node
            for key, node in suggestion_functions.items()
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        for import_node in import_nodes:
            new_body.append(import_node)
            suggestion_functions.pop(
                import_node.name if hasattr(import_node, "name") else import_node.module
            )  # Remove import from suggestion_functions

        for node in initial_ast.body:
            if isinstance(node, ast.ClassDef):
                node = self._handle_class_definitions(node, suggestion_functions)
                new_body.append(node)
            elif isinstance(node, ast.FunctionDef):
                # Handle global functions
                if node.name in suggestion_functions:
                    print(f"Replacing function {node.name}")
                    new_body.append(suggestion_functions.pop(node.name))
                else:
                    new_body.append(node)
            else:
                new_body.append(node)

        # Inject remaining global functions
        for func_name, func in suggestion_functions.items():
            if "." not in func_name:  # This line filters out class methods
                print(f"Injecting new function {func.name}")
                new_body.append(func)

        initial_ast.body = new_body
        updated_source = astor.to_source(initial_ast)
        print("Source updated.")
        return updated_source

    def _clean_code(self, code: str) -> str:
        print("Cleaning code...")
        cleaned_code = code.replace("'", '"')
        lines = cleaned_code.split("\n")
        cleaned_lines = [line for line in lines if line.strip() != ""]
        print("Code cleaned.")
        return "\n".join(cleaned_lines).strip()

    def _validate_strings(self, *args) -> None:
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError("Expected a string argument.")
            if arg is None or not arg.strip():
                raise ValueError("String argument is empty or None.")

    def _handle_class_definitions(self, node, suggestion_functions):
        print(f"Inspecting class {node.name}")
        new_class_body = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_method_name = f"{node.name}.{item.name}"
                if class_method_name in suggestion_functions:
                    print(f"Replacing method {class_method_name}")
                    new_class_body.append(suggestion_functions.pop(class_method_name))
                else:
                    new_class_body.append(item)

        # Add the methods from suggestion_functions that belong to this class
        for k, v in list(suggestion_functions.items()):
            if k.startswith(f"{node.name}."):
                print(f"Injecting new method {k}")
                new_class_body.append(v)
                del suggestion_functions[k]

        node.body = new_class_body
        return node

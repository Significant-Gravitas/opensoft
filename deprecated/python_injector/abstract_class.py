import ast
from abc import ABC, abstractmethod

import astor


class AbstractPythoninjector(ABC):
    @abstractmethod
    def extract_functions(self, file_content: str) -> dict:
        """
        Extracts all functions (and class methods) from the provided Python source code.
        """
        pass

    @abstractmethod
    def inject_functions(self, initial: str, suggestion: str) -> str:
        """
        Injects or replaces functions (and class methods) from the 'suggestion' Python source code
        into the 'initial' Python source code.
        """
        pass

    @abstractmethod
    def get_parsed_source(self, source: str) -> ast.Module:
        """
        Returns the parsed Abstract Syntax Tree (AST) of the provided Python source code.
        """
        pass

    @abstractmethod
    def get_updated_source(
        self, initial_ast: ast.Module, suggestion_functions: dict
    ) -> str:
        """
        Updates the 'initial' AST using the 'suggestion' functions and
        returns the new source code as a string.
        """
        pass

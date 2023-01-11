"""
AUTHOR: Ebin Paul
"""

from core.parser.nodes import Token, TokenType

from .parser.syntaxAnalyzer import Parser


class Interpreter:
    """
    Interpreter class:
    initialized with the input string.
    First instance variable tokens is initialized with gets a list of tokens from Lexer class based on the input string provided.
    The second instance variable is a root node of the AST (Abstract Syntax Tree) which is obtained as a result from Parser class.
    """

    def __init__(self, input_string):
        self.__root_node = Parser(input_string).parse()

    def execute(self):
        """
        returns the value of the root node which runs recursively to obtain the result of the expression.
        """
        if self.__root_node:
            return self.__root_node.get_node_value()

        return ""

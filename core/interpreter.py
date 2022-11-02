from core.parser.nodes import Token, TokenType


class Interpreter:
    def __init__(self, ast):
        self.__ast = ast

    def execute(self):
        return self.__ast.get_node_value()

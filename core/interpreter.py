from core.parser.nodes import Token, TokenType
from .lexer.lexicalAnalyzer import Lexer
from .parser.syntaxAnalyzer import Parser


class Interpreter:
    def __init__(self, root_node):
        self.__root_node = root_node

    def execute(self):
        return self.__root_node.get_node_value()


def main(input_string: str):
    lexer = Lexer(input_string)

    tokens = lexer.get_tokens()
    # result = lexer.get_tokens()

    parser = Parser(tokens)

    root_node = parser.parse()

    interpreter = Interpreter(root_node)

    result = interpreter.execute()

    return result

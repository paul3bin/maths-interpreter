from core.parser.nodes import Token, TokenType

from .lexer.lexicalAnalyzer import Lexer
from .parser.syntaxAnalyzer import Parser


class Interpreter:
    def __init__(self, input_string):
        self.__tokens = Lexer(input_string).get_tokens()
        self.__root_node = Parser(self.__tokens).parse()

    def execute(self):
        return self.__root_node.get_node_value()


def main(input_string: str):
    interpreter = Interpreter(input_string)

    result = interpreter.execute()

    return result

"""
Authors: Max James, Christopher Gavey, Ebin Paul, Aswin, Soniya
Program: Mathematical visualisation software interpreter
Version: 1.1
Version Date: 08/11/2022
"""
from core.interpreter import Interpreter
from core.lexer.lexicalAnalyzer import Lexer
from core.parser.syntaxAnalyzer import Parser


def main(input_string: str):
    lexer = Lexer(input_string)

    tokens = lexer.get_tokens()

    parser = Parser(tokens)

    root_node = parser.parse()

    interpreter = Interpreter(root_node)

    result = interpreter.execute()

    return result


if __name__ == "__main__":
    while True:
        input_string = input("Enter expression >> ")
        if input_string:
            print(main(input_string))

        continue

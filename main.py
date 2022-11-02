"""
Authors: Max James, Christopher Gavey, Ebin Paul, Aswin, Soniya
Program: Mathematical visualisation software interpreter
Version: 1.02
Version Date: 02/11/2022
"""
from core.interpreter import Interpreter
from core.lexer.lexicalAnalyzer import Lexer
from core.parser.syntaxAnalyzer import Parser

while True:
    input_string = input("Enter expression >> ")
    lexer = Lexer(input_string)

    tokens = lexer.get_tokens()

    parser = Parser(tokens)

    ast = parser.parse()

    print(ast)

    interpreter = Interpreter(ast)

    result = interpreter.execute()

    print(result)

"""
Authors: Max James, Christopher Gavey, Ebin Paul, Aswin, Soniya
Program: Mathematical visualisation software interpreter
Version: 1.03
Version Date: 04/11/2022
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

    interpreter = Interpreter(ast)

    result = interpreter.execute()

    print(result)

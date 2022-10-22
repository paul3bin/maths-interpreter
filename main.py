"""
Authors: Max James, Christopher Gavey, Ebin Paul, Aswin, Soniya
Program: Mathematical visualisation software interpreter
Version: 1.01
Version Date: 19/10/2022
"""
from core.lexer.lexicalAnalyzer import Lexer

while True:
    input_string = input("Enter expression >> ")
    lexer = Lexer(input_string)

    tokens = lexer.get_tokens()

    print(tokens, f"; Number of tokens: {len(tokens)}")

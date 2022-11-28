"""
AUTHOR: Ebin, Aswin
DESCRIPTION: The following classes are nodes of Abstract Syntax Tree (AST). Each class has a get_node_value method which returns,
            the value of that particular node
            
REFERENCES: https://ruslanspivak.com/lsbasi-part1/
"""


from enum import Enum


class TokenType(Enum):
    """
    TokenType class declaration
    """

    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    LEFT_PARENTHESIS = "LEFT_PARENTHESIS"
    RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"
    FLOAT = "FLOAT"
    CARET = "CARET"
    ASSIGN = "ASSIGN"
    GT = "GREATER_THAN"
    LT = "LESS_THAN"
    IDENTIFIER = "IDENTIFIER"
    END = "END"


class Token:
    """
    Token class declaration
    """

    def __init__(self, type, value=None):
        self.type: TokenType = type
        self.value: any = value

    # string representation of a token.
    def __str__(self):
        return f"Token({self.type.name}: {self.value})"

    def __repr__(self):
        return self.__str__()

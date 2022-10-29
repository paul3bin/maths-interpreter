from enum import Enum


# TokenType class declaration
class TokenType(Enum):
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LEFT_PARENTHESIS = "LEFT_PARENTHESIS"
    RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"
    FLOAT = "FLOAT"
    CARET = "CARET"
    END = "END"


# Token class declaration
class Token:
    def __init__(self, type, value=None):
        self.type: TokenType = type
        self.value: any = value

    # string representation of a token.
    def __str__(self):
        return f"Token({self.type.name}: {self.value})"

    def __repr__(self):
        return self.__str__()

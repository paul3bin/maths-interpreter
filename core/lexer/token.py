from dataclasses import dataclass
from enum import Enum


# TokenType class declaration
class TokenType(Enum):
    INTEGER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    LEFT_PARENTHESIS = 5
    RIGHT_PARENTHESIS = 6


# Token class declaration
@dataclass
class Token:
    type: TokenType
    value: any = None

    # string representation of a token.
    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()
